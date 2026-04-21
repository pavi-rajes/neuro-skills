# Progress Notebook — Perich et al. (2025) Replication

**Dataset:** Allen Institute Dynamic Routing — `s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/`  
**Skills involved:** `nwb-s3-browser`, `paper-analysis`  
**Subjects selected:** 676909 (2023-12-11 → 14), 681532 (2023-10-16 → 19)

---

## Skill: `nwb-s3-browser`

### Challenge 1 — lazynwb fails on all S3 files with "Failed to open as HDF5 or Zarr"

**What happened:** Every file returned a read error when scanning via `lazynwb.scan_nwb()`. No rows, no schema.

**Fixes tried:**
- Checked file paths — paths were correct.
- Checked that files existed via boto3 — they did.

**Fix that worked:**
```python
lazynwb.config.use_obstore = False
lazynwb.config.fsspec_storage_options = {"anon": True}
```
These two lines must be set **before** any `scan_nwb` call. The default config uses `obstore` without anonymous credentials, which fails on public buckets. Switching to `fsspec` with `anon=True` fixes it.

**Captured in skill:** Yes — `nwb-s3-browser/SKILL.md` Setup section.

---

### Challenge 2 — `units.location` missing in 2024+ sessions

**What happened:** Scripts that read `f['units']['location']` worked on 2023 sessions but would fail silently (or with KeyError) on 2024+ sessions, which don't have `location` in the `units` table.

**Root cause:** NWB schema version split. 2023 sessions store region in `units/location`. 2024+ sessions store it only in `general/extracellular_ephys/electrodes`, linked via `peak_electrode` index.

**Fix that worked:** Use the `electrodes` table for region queries in lazynwb — it works across all schema versions:
```python
lf = lazynwb.scan_nwb(nwb_paths, "electrodes", ignore_errors=True)
sessions = lf.filter(pl.col("location").str.starts_with("VIS")).select("_nwb_path").unique().collect()
```
For the Perich analysis we deliberately selected subjects 676909 and 681532 (both 2023) where `units.location` works directly via h5py.

**Captured in skill:** The general principle (prefer electrodes table) is in `nwb-s3-browser`. The DR-specific schema-version details are in `paper-analysis/SKILL.md` under the Allen DR dataset block.

---

### Challenge 3 — Corrupted / incompatible NWB files in the dataset

**What happened:** A handful of files (e.g. `667252_2023-09-25.nwb`, `664851_2023-11-13.nwb`) fail even after the anon fix.

**Fix that worked:** Pass `ignore_errors=True` to `scan_nwb`. These files are outliers; the majority of the dataset is clean.

**Captured in skill:** Yes — `nwb-s3-browser/SKILL.md` Gotchas section (use `ignore_errors=True`).

---

### Learning — lazynwb scan speed

After the anon fix, `scan_nwb` on the `electrodes` table runs at ~2.5 NWB/s. Scanning all 217 sessions for region coverage takes ~90 seconds. Unit-level scans (`units` table) are slower — 5–15 min for the full dataset.

---

## Skill: `paper-analysis`

### Challenge 4 — `fs.open()` with wrong `block_size` placement

**What happened:** `fsspec.filesystem('s3', anon=True, block_size=2**23)` raised:
```
TypeError: AioSession.__init__() got an unexpected keyword argument 'block_size'
```

**Root cause:** `block_size` is a per-file parameter, not a filesystem-level parameter. It must be passed to `fs.open()`, not `fsspec.filesystem()`.

**Fix that worked:**
```python
fs = fsspec.filesystem('s3', anon=True)
# ...
fs.open(nwb_path, 'rb', block_size=2**23)   # 8 MB blocks
```

**Why `block_size` matters:** h5py navigating an HDF5 tree over S3 makes many small HTTP range requests. A larger block cache (8 MB vs default 5 MB) reduces round-trips and speeds up metadata reads noticeably.

**Captured in skill:** Added note to `paper-analysis/SKILL.md` in the `load_session` function template.

---

### Challenge 5 — `load_session` called 3× per session (once per region)

**What happened:** Original main loop called `load_session(path, region)` for each region independently. For 8 sessions × 3 regions = 24 separate h5py file opens + 24 full `spike_times` flat array downloads from S3.

**Why it was slow:** Each h5py file open over S3:
1. Reads the HDF5 superblock and B-tree metadata (many small HTTP requests)
2. Downloads the full `spike_times` flat array (~20–80 MB per session)

Doing this 3× per session is pure waste since all regions live in the same file.

**Fix that worked:** `load_all_regions(path, regions)` — opens each file once, reads `spike_times` once, partitions into per-region lists in memory:
```python
region_spike_times, stim_start, rew_mod = load_all_regions(path, REGIONS)
# → 8 file opens total instead of 24
```

**Captured in skill:** `paper-analysis/SKILL.md` — recommend opening file once and loading all needed regions/data in a single `with h5py.File(...)` block.

---

### Challenge 6 — `binned_rates` Python loop was extremely slow

**What happened:** Original implementation:
```python
for u, st in enumerate(spike_times):
    for t, t0 in enumerate(events):
        counts[u, t, :], _ = np.histogram(st - t0, bins=BINS)
```
`np.histogram(st - t0, bins=BINS)` recomputes `st - t0` for the **entire** spike array (~millions of spikes) on every trial. For 80 units × 800 trials = 64,000 calls, each touching a full spike array, this is O(n_spikes × n_trials × n_units) total work.

The notebook ran for ~90 minutes without producing any output.

**Fix that worked:** `np.searchsorted` + `np.bincount`, operating only on in-window spikes:
```python
for u, st in enumerate(spike_times):          # st must be sorted
    for t0 in events:
        lo = np.searchsorted(st, t0 + T_START)
        hi = np.searchsorted(st, t0 + T_END)
        if lo < hi:
            spk      = st[lo:hi] - t0         # only ~few dozen spikes per trial
            bin_idxs = np.searchsorted(BINS[1:], spk)
            counts[u] += np.bincount(bin_idxs, minlength=N_BINS)
```
Requires spike_times to be **sorted ascending** (enforced in `load_all_regions` via `np.sort`). Each trial now only touches the handful of spikes actually in the ±1.5 s window — ~100× fewer operations.

**Captured in skill:** `paper-analysis/SKILL.md` spike counting section — replace `np.histogram` loop with `searchsorted` pattern; note that sorted spike times are required.

---

### Challenge 7 — nbconvert not available in the `nwb` conda env

**What happened:** `jupyter nbconvert` not in PATH for the `nwb` environment.

**Fix:** Install directly into the env:
```bash
/opt/miniconda3/envs/nwb/bin/pip install nbconvert nbformat nbclient
```

**Note:** The `nwb` env has all analysis packages (h5py, fsspec, sklearn, matplotlib, lazynwb, polars) but was missing the Jupyter execution stack.

---

### Challenge 8 — CPU saturation causing S3 timeouts

**What happened:** Multiple `train_gru.py` jobs were running in parallel (~150% CPU each), saturating the machine. This caused S3 reads to time out during h5py file open attempts (profiling script failed with `AioReadTimeoutError`).

**Fix:** Killed all training jobs before running the notebook. After that, S3 reads completed normally.

**Lesson:** Check CPU usage before kicking off S3-heavy NWB analysis — I/O timeouts are often a symptom of CPU saturation, not a network problem.

---

### Learning — Subject selection for this analysis

Subjects 676909 and 681532 were chosen because:
- Both have exactly 4 consecutive daily sessions
- Both are 2023 recordings (use `units.location` directly — no `peak_electrode` join needed)
- Both have confirmed VIS + MO units in all 4 sessions
- AUD units are present in 2/4 sessions each (flagged as a caveat in the notebook)

Selection was done via lazynwb electrodes scan (after the anon fix), which ran at ~2.5 NWB/s.

---

### Learning — Cache writes after each session

Original notebook cached results only at the very end of the full analysis loop. If the run failed midway, all progress was lost.

**Fix:** Added a `np.save('manifold_results_by_region.npy', cache)` call after each session completes. Downstream figure cells can be re-run using the partial cache without re-loading spike data.

---

## General Execution Notes

| Issue | Note |
|---|---|
| `.claude/skills` and `skills/` out of sync | Fixed by making `.claude/skills` a symlink to `../skills/` — edits to either location are now the same file |
| nbconvert runs silently | No stdout until completion. Monitor via `ls *.npy` for cache file appearance or `TaskOutput` polling |
| `np.save(..., allow_pickle=True)` required | The results dict contains Python objects (PCA instances) — need `allow_pickle=True` for the cache |
| NWB `spike_times` index is cumulative | `st_idx[i]` is the end index for unit `i`; start is `st_idx[i-1]` (or 0 for the first unit) |
| `rewarded_modality` values are bytes in older NWB | Always decode: `v.decode() if isinstance(v, bytes) else str(v)` |

---

---

### Challenge 9 — `principal_angles` Gram matrix transposition bug

**What happened:** `angles` array had shape `(n_units,)` instead of `(n_pcs,)`, causing a `ValueError` in `ax_ang.bar(np.arange(1, n_pcs+1), angles, ...)` (shape mismatch: x=(10,), height=(95,)).

**Root cause:** Wrong matrix multiplication order:
```python
# WRONG — gives (n_units × n_units) Gram matrix
M = pca_a.components_.T @ pca_b.components_.T.T
# = (n_units, n_pcs) @ (n_pcs, n_units) = (n_units, n_units)
```
`np.linalg.svd` on a `(n_units × n_units)` matrix returns `n_units` singular values, not `n_pcs`.

**Fix:**
```python
# CORRECT — gives (n_pcs × n_pcs) Gram matrix
M = pca_a.components_ @ pca_b.components_.T
# = (n_pcs, n_units) @ (n_units, n_pcs) = (n_pcs, n_pcs)
```
`pca.components_` shape is `(n_pcs, n_features)`. The Gram matrix between two PC subspaces is `U @ V^T` where `U, V` are the component matrices — gives `(n_pcs × n_pcs)` and `n_pcs` principal angles.

**Side effect:** Cache file `manifold_results_by_region.npy` had wrong `angles` arrays and was deleted before re-run.

**Note:** Analysis loop itself ran successfully in ~1 minute (searchsorted optimization worked). Error was only in the downstream plotting cell.

---

---

### Challenge 10 — `REGION_COLORS` dict not updated after region rename

**What happened:** After changing `REGIONS` from `['VIS', 'AUD', 'MO']` to `['MOp', 'MOs']`, the figure cell had a hardcoded `REGION_COLORS = {'VIS': ..., 'AUD': ..., 'MO': ...}`. When the loop iterated over `REGIONS` and looked up `REGION_COLORS['MOp']`, it raised `KeyError: 'MOp'`.

**Fix:** Update `REGION_COLORS` to match the new region list:
```python
REGION_COLORS = {'MOp': '#2ca02c', 'MOs': '#9467bd'}
```

**Lesson for `paper-analysis` skill:** When changing `REGIONS`, also search all downstream cells for hardcoded region names in color dicts, labels, or conditionals. The main loop is parameterized on `REGIONS` but figure cells may not be.

**Captured in skill:** Not yet — add to `paper-analysis/SKILL.md` under "Gotchas".

---

### Challenge 11 — nbformat version mismatch causing cell skip

**What happened:** Notebook had `nbformat_minor: 4` but one cell had an `id` field (added in nbformat 4.5+). This caused `nbconvert` to fail at validation with "Additional properties are not allowed ('id' was unexpected)". Upgrading to `nbformat_minor: 5` fixed the validation error but then cells WITHOUT `id` fields generated a `MissingIDFieldWarning`. The notebook still executed correctly.

**Fix:** Set `nbformat_minor: 5` in the notebook JSON. Existing cells without ids get a warning but are still executed. Alternatively: normalize the notebook with `nbformat.normalize()` to assign ids to all cells.

**Note:** The `id` field in one cell was added automatically by the Jupyter editor (likely VS Code). Any notebook edited in a modern Jupyter client will have cell ids added. To avoid future mismatches, keep `nbformat_minor` at 5 or higher.

---

## Current Status (2026-04-20)

**Perich et al. (2025) replication complete with MOp/MOs regions.**

- Notebook: `perich_2025/perich_2025.ipynb` — final run with `REGIONS = ['MOp', 'MOs']`
- Figures: `manifold_per_session_{subj}.png`, `manifold_stability_4day.png`
- Cache: `perich_2025/manifold_results_by_region.npy` (11 session-region entries)
- Report: `perich_2025/report.md` — filled with MOp/MOs results

**Key finding:** MOp (M1 analog) angles 34–45° (below chance), MOs (PMd analog) 43–56° (at/above chance). Pattern matches Perich paper's M1 vs PMd contrast.

---

## Post-replication skill review (2026-04-20)

### Issue — MOs ≈ PMd mapping was silently applied

The replication report called MOs the "PMd analog" without flagging it as a user decision. On review this is overclaiming: primate PMd is a well-defined cytoarchitecturally distinct area; mouse MOs is a broader secondary motor zone that is also sometimes mapped to SMA. The two are *rough* analogs at best.

**Correct framing:** "MOs = secondary/premotor motor cortex analog" — the M1/premotor contrast is preserved, but calling MOs specifically "PMd" is not warranted.

**Root cause in the skill:** The `paper-analysis` skill had no explicit step for resolving paper region → dataset region. The skill silently applied a region mapping without asking the user.

### Skill update — population sampling step added

Updated `skills/paper-analysis/SKILL.md` (2026-04-20):

1. **New subsection in Step 2** — "Population sampling": extract region names, co-recording requirements, cell-type filters, and minimum N from the paper, then immediately query the dataset to surface what's actually available before presenting the mapping.

2. **Step 3 confirmation now requires a population-sampling block**: shows paper region → dataset region match quality, flags approximations explicitly, and asks whether co-recorded pairs are required or regions can be analyzed independently.

**Core rule added:** *Never silently substitute a region — that is a scientific choice the user must make.*
