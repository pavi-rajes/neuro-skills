---
name: paper-analysis
description: >
  Apply a neuroscience analysis from a published paper to NWB data on S3.
  Trigger when the user provides a paper (PDF path, URL, DOI, or arXiv ID) and asks
  to replicate, reproduce, or apply its analysis to their data — phrases like
  "run the analysis from this paper", "apply the method in doi:...", "replicate
  figure 3 from ...", "use the decoding approach from X et al.", "implement this
  paper's approach on our dataset", "do what they did in [paper]". Also trigger
  when the user pastes a methods section and asks to implement it.
---

# Paper Analysis

> This skill reads a paper, extracts its analysis, confirms the mapping to NWB data
> with the user, then produces a Jupyter notebook implementing the analysis on S3 NWB
> data, combining `lazynwb` + `polars` for session selection with `pynwb` + `numpy`
> for trial-aligned computation.

## The core loop

1. **Ingest** — fetch the paper and extract the analysis requirements
2. **Map** — translate paper variables to NWB fields
3. **Confirm** — show the mapping to the user and wait for sign-off ← **do not skip**
4. **Select** — find sessions meeting the paper's inclusion criteria
5. **Implement** — produce a Jupyter notebook with prose, code, and plots
6. **Flag deviations** — honest faithful / adapted / uncertain breakdown

The most common failure mode is silently guessing how paper variables map to NWB
fields. Step 3 exists to surface this before any code runs.

---

## Output folder

Create a dedicated folder for each replication task **before writing any files**.
Name it `{first_author}_{year}/` (e.g. `perich_2018/`). All outputs go here:

```
{first_author}_{year}/
├── paper.pdf                   # copy of the paper (or symlink if local path provided)
├── paper_replication_plan.md   # the mapping from Step 3 — finalized after user confirms
├── {first_author}_{year}.ipynb # generated notebook from Step 5
└── report.md                   # deviation report from Step 6
```

**`paper_replication_plan.md`** — save the confirmed Step 3 mapping table here.
Include: paper citation, target figure(s), paper→NWB variable mapping, assumptions,
open questions, and any parameter overrides the user requested.

**`report.md`** — save the Step 6 faithful/adapted/uncertain breakdown here, plus
a one-paragraph summary of what was run and any notable results.

---

## Step 1: Fetch the Paper

Resolve the input to readable text before doing anything else.

### DOI

```python
url = f"https://doi.org/{doi}"   # e.g. "10.1016/j.neuron.2019.01.023"
# Use WebFetch — most publishers redirect to the landing page
```

If the DOI resolves to a paywall, try:
- `https://www.biorxiv.org/search/{first_author}+{year}` (preprint)
- `https://arxiv.org/search/?query={title}&searchtype=all`
- PubMed Central: `https://www.ncbi.nlm.nih.gov/pmc/search/?term={doi}`

### arXiv ID

```
https://arxiv.org/abs/{id}   # HTML — faster to parse than PDF
https://arxiv.org/pdf/{id}   # PDF fallback
```

### URL or local PDF

Fetch directly with WebFetch, or use the Read tool for a local PDF path.

### What to extract

Read the **Methods** section (and supplementary methods if available — that's where
implementation details live). Extract:

| Field | What to find | Example |
|---|---|---|
| **Species / preparation** | Mouse / rat / primate, awake or anesthetized | "head-fixed mice" |
| **Data modality** | Ephys (units), LFP, calcium imaging | "Neuropixels probes" |
| **Target regions** | Brain areas analyzed | "V1 and PFC" |
| **Trial alignment event** | What time 0 is relative to | "stimulus onset" |
| **Analysis window** | Time window around the event | "−0.2 to 0.5 s" |
| **Bin size** | Spike count bin width | "50 ms bins" |
| **Unit quality threshold** | Firing rate, ISI, waveform criteria | "FR > 1 Hz" |
| **Minimum unit count** | N units per session required | "≥ 15 units per area" |
| **Normalization** | z-score, soft-normalize, divide by baseline | "z-scored to baseline" |
| **Core algorithm** | Decoding, PCA, CCA, correlations, etc. | "cross-validated LDA" |
| **Statistical test** | How significance is assessed | "permutation test, n=1000" |
| **Key figure** | What the paper shows as the main result | "Figure 3B: accuracy over time" |

After extracting, confirm with the user:
- Which analysis (if the paper has multiple)
- Which figure(s) they want to reproduce
- Any parameters they want to override from the paper's defaults

---

## Step 2: Map Paper Requirements to NWB

Translate the extracted fields to NWB tables and columns.

### Data modality mapping

| Paper says | NWB source | Load via |
|---|---|---|
| "single units", "neurons", "cells" | `units` table | `lazynwb.scan_nwb(..., "units")` |
| "multi-unit activity" | `units` table, ignore quality filter | same |
| "LFP" | `processing/ecephys/LFP` | `pynwb` direct (not lazynwb) |
| "spike times" | `units.spike_times` (ragged array) | `pynwb` direct after unit selection |
| "trials", "stimuli" | `trials` table | `lazynwb.scan_nwb(..., "trials")` |
| "task epochs" | `intervals/epochs` | `lazynwb.scan_nwb(..., "epochs")` |

### Population sampling — resolve this before writing any code

Extract from the paper:

| Question | Where to look | What to record |
|---|---|---|
| Which brain region(s)? | Methods, Figure captions | Exact names the paper uses |
| Same population or co-recorded? | Methods ("simultaneously recorded", "same session") | Joint vs. independent |
| Cell-type specific? | "putative pyramidal", "fast-spiking", layer designation | Any subtype filter |
| N neurons required? | Inclusion criteria, footnotes | Minimum per session/area |

Then **immediately check what the dataset actually contains** before presenting the mapping to the user:

```python
import lazynwb, polars as pl
from upath import UPath

nwb_paths = list(UPath("s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/").glob("**/*.nwb"))
lf = lazynwb.scan_nwb(nwb_paths, "electrodes", ignore_errors=True)
available_regions = (
    lf.select("location").unique()
      .filter(pl.col("location").is_not_null())
      .collect()["location"].to_list()
)
print(sorted(available_regions))
```

Use this to answer three questions for the user in Step 3:
1. Does the dataset have the paper's exact region?
2. If not, what's the closest available region, and how confident is the homology?
3. Does the user want to use the homolog, pick a different region, or analyze both?

**Never silently substitute a region.** A primate PMd → mouse MOs mapping is a scientific choice the user must make, not a lookup.

### Region normalization

Map paper region names to NWB `location` values (use `str.starts_with`, not exact match):

| Paper says | Query prefix | Notes |
|---|---|---|
| "V1", "primary visual cortex" | `VISp` | |
| "visual cortex" (general) | `VIS` | |
| "PFC", "prefrontal" | `ACA`, `ORB`, `PFC` | no single mouse homolog — ask user |
| "motor cortex" (general) | `MOs`, `MOp` | |
| "M1", "primary motor cortex" | `MOp` | |
| "premotor cortex", "PMd", "PMv" | `MOs` | approximate — flag, ask user |
| "ACC", "anterior cingulate" | `ACA` | |
| "hippocampus", "CA1" | `CA1` | |
| "auditory cortex" | `AUD` | |
| "thalamus" | `LP`, `LGd` | |

Entries marked "ask user" or "approximate" must be surfaced in Step 3 — do not silently apply them.

---

## Step 3: Confirm the Mapping — do not skip

Before writing any analysis code, write out the mapping in prose or a table and
show it to the user. Wait for explicit confirmation or corrections.

The confirmation must include a **population sampling section** as a separate block.
This is the most common source of silent errors — always make it explicit.

Example format:

> **Mapping plan — please confirm before I proceed:**
>
> **Population sampling:**
> | Paper population | Dataset region available | Match quality | Your choice? |
> |---|---|---|---|
> | M1 (primate primary motor) | `MOp` | approximate homolog | ✓ / use different? |
> | PMd (primate dorsal premotor) | `MOs` | rough analog — not identical | ✓ / use different? |
>
> Paper requires co-recorded M1+PMd pairs: **X of Y sessions** in this dataset have both MOp and MOs with ≥ N units. Want to require simultaneous recording, or analyze each region independently across all eligible sessions?
>
> **Variable mapping:**
> | Paper variable | NWB field | Notes |
> |---|---|---|
> | "spike trains binned at 50 ms" | `units.spike_times`, binned to 50 ms grid | spike_times are in seconds |
> | "stimulus-aligned activity" | aligned to `trials.start_time` | assuming start_time = stim onset |
> | "V1 population" | units where `location.starts_with("VISp")` | you have ~N units; paper used ~M |
> | "correct vs. error trials" | `trials.is_hit` boolean | |
> | "vis-context vs aud-context" | `trials.context_name` | switches mid-session — will segment by block |
>
> **Assumptions I'm making:**
> - Spike times are in seconds (standard for this dataset)
> - Baseline window is −0.5 to 0 s relative to trial start
>
> **Gaps / open questions:**
> - Paper requires N ≥ 50 units; user's sessions average M — flagging this as a caveat
>
> Anything wrong? Anything you'd change?

If the mapping has significant gaps — paper uses a condition the user's data doesn't
have, or a required column is absent — raise it as an open question, not a silent
substitution.

---

## Step 4: Select Sessions

Use `lazynwb` + `polars` to find sessions meeting the paper's inclusion criteria.
Run this before opening any files for spike times.

```python
import lazynwb
import polars as pl
from upath import UPath

nwb_paths = list(UPath("s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/").glob("**/*.nwb"))

target_region = "VISp"   # per paper
min_units     = 15        # paper's inclusion criterion

lf = lazynwb.scan_nwb(nwb_paths, "units")
eligible = (
    lf
    .filter(
        pl.col("location").str.starts_with(target_region),
        pl.col("default_qc") == True,
    )
    .group_by("_nwb_path")
    .agg(pl.len().alias("n_units"))
    .filter(pl.col("n_units") >= min_units)
    .sort("n_units", descending=True)
    .collect()
)
print(f"{len(eligible)} / {len(nwb_paths)} sessions pass inclusion criteria")
selected_paths = eligible["_nwb_path"].to_list()
```

For **multiple co-recorded regions**:

```python
regions = ["VISp", "ACA"]

regions_df = (
    lazynwb.scan_nwb(nwb_paths, "units")
    .filter(pl.col("default_qc") == True)
    .select("_nwb_path", "location")
    .unique()
    .collect()
)

selected_paths = [
    s for s in regions_df["_nwb_path"].unique()
    if all(
        regions_df.filter(pl.col("_nwb_path") == s)["location"]
        .str.starts_with(r).any()
        for r in regions
    )
]
print(f"{len(selected_paths)} sessions with {' + '.join(regions)}")
```

---

## Step 5: Implement as a Notebook

Produce a Jupyter notebook (`.ipynb`). Always write a `.py` file with `# %%` cell
markers first, then convert with `jupytext --to ipynb file.py`. The `.py` source is
easier to write correctly; jupytext handles the JSON. Delete the `.py` after
successful conversion — the `.ipynb` is the deliverable.

```bash
jupytext --to ipynb {first_author}_{year}/{first_author}_{year}.py
rm {first_author}_{year}/{first_author}_{year}.py
```

**Notebook structure:**

1. **Title + citation** (markdown): paper title, authors, year, DOI. Which analysis is being reproduced.
2. **Imports + data loading** (code)
3. **Quick data inspection** (code): shapes, schema, a `.head()` — confirms loading and documents what the data looks like
4. **Preprocessing** (markdown + code, one cell pair per step): filter → align → bin → exclude → normalize. Explain *why* each step matches the paper.
5. **Core analysis** (markdown + code): the method itself. Quote or cite equations from the paper where helpful.
6. **Results / plots** (markdown + code, one pair per figure): mirror the paper's figure style — same axis labels, same comparison groups, same statistical annotation.
7. **Deviations** (markdown): faithful / adapted / uncertain breakdown (see Step 6).

**Notebook conventions:**
- Mark cells that take > 1 minute as `# ⚠️ long-running (~X min)` with a time estimate.
- Save expensive intermediates (binned spike matrices, PCA fits) to disk so the user can iterate on later cells without rerunning everything.
- Set `np.random.seed(42)` (or equivalent) for any stochastic step; note it.
- Every plot axis needs a label and unit. No bare `plt.xlabel("0")` — say what it means.

### Load spike times (pynwb)

⚠️ Only run after Step 4 — only on sessions that passed inclusion, only for units
and time windows you actually need. Warn before running across many sessions.

```python
import numpy as np
import fsspec
from pynwb import NWBHDF5IO

def load_session(nwb_path: str, target_region: str, qc_col: str = "default_qc"):
    """
    Returns:
        spike_times: list of 1D np.ndarray, one per unit
        trials:      dict of column_name → np.ndarray from trials table
        unit_ids:    list of unit IDs
    """
    fs = fsspec.filesystem("s3", anon=True)
    with NWBHDF5IO(fs.open(nwb_path, "rb"), "r", load_namespaces=True) as io:
        nwb = io.read()
        units_df = nwb.units.to_dataframe()
        mask = (
            units_df["location"].str.startswith(target_region) &
            units_df[qc_col].astype(bool)
        )
        units_df = units_df[mask]
        spike_times = [np.array(nwb.units["spike_times"][i]) for i in units_df.index]
        unit_ids    = units_df.index.tolist()
        trials_df   = nwb.trials.to_dataframe()
        trials      = {col: trials_df[col].values for col in trials_df.columns}
    return spike_times, trials, unit_ids
```

> For private buckets: change `anon=True` → `anon=False` and configure AWS credentials.

### Trial-aligned spike counts

```python
def spike_counts_in_window(
    spike_times_list: list[np.ndarray],
    event_times: np.ndarray,
    t_start: float,
    t_end: float,
    bin_size: float | None = None,
) -> np.ndarray:
    """
    Returns:
        bin_size is None  → (n_units, n_trials)
        bin_size given    → (n_units, n_trials, n_bins)
    """
    n_units, n_trials = len(spike_times_list), len(event_times)
    if bin_size is None:
        counts = np.zeros((n_units, n_trials))
        for u, st in enumerate(spike_times_list):
            for t, t0 in enumerate(event_times):
                counts[u, t] = np.sum((st >= t0 + t_start) & (st < t0 + t_end))
        return counts
    bins   = np.arange(t_start, t_end + bin_size, bin_size)
    n_bins = len(bins) - 1
    counts = np.zeros((n_units, n_trials, n_bins))
    for u, st in enumerate(spike_times_list):
        for t, t0 in enumerate(event_times):
            counts[u, t, :], _ = np.histogram(st - t0, bins=bins)
    return counts
```

### Normalize to baseline

```python
def zscore_to_baseline(counts: np.ndarray, baseline_bins: slice) -> np.ndarray:
    # counts: (n_units, n_trials, n_bins)
    baseline = counts[:, :, baseline_bins]
    mu    = baseline.mean(axis=(1, 2), keepdims=True)
    sigma = baseline.std(axis=(1, 2), keepdims=True) + 1e-8
    return (counts - mu) / sigma
```

### Analysis templates

Pick the template matching the paper's core method. Never invent parameter values —
if the paper is unclear, ask the user.

#### Linear decoding

**Phrases:** "cross-validated decoding", "LDA", "logistic regression", "SVM",
"above-chance accuracy"

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

def decode_variable(X, y, n_splits=5, C=1.0, seed=42):
    cv   = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    accs = []
    for train, test in cv.split(X, y):
        sc  = StandardScaler().fit(X[train])
        clf = LogisticRegression(C=C, max_iter=1000).fit(sc.transform(X[train]), y[train])
        accs.append(clf.score(sc.transform(X[test]), y[test]))
    return float(np.mean(accs)), np.array(accs)

# Decode over time — ⚠️ long-running for many bins × sessions
acc_time = np.array([decode_variable(counts[:, :, b].T, labels)[0]
                     for b in range(counts.shape[2])])

# Permutation baseline (n=1000)
np.random.seed(42)
perm_acc = np.array([[decode_variable(counts[:, :, b].T,
                                      np.random.permutation(labels))[0]
                      for b in range(counts.shape[2])]
                     for _ in range(1000)])
chance, sig_thresh = perm_acc.mean(0), np.percentile(perm_acc, 95, axis=0)
```

#### PCA / manifold trajectories

**Phrases:** "population trajectory", "neural manifold", "PCA", "variance explained",
"UMAP"

```python
from sklearn.decomposition import PCA

# Condition-average, then concatenate across time
cond_labels = np.unique(labels)
X_by_cond   = np.stack([counts[:, labels == c, :].mean(axis=1) for c in cond_labels])
# (n_cond, n_units, n_bins) → reshape to (n_cond*n_bins, n_units) for PCA
n_cond, n_units, n_bins = X_by_cond.shape
X_pca = X_by_cond.transpose(1, 0, 2).reshape(n_units, -1).T

pca          = PCA(n_components=10, random_state=42)
X_proj       = pca.fit_transform(X_pca)
var_explained = pca.explained_variance_ratio_
trajectories  = X_proj.reshape(n_cond, n_bins, -1)   # (n_cond, n_bins, n_pcs)
print(f"Top 3 PCs: {var_explained[:3].sum():.1%} variance explained")
```

#### PSTH / population-average response

**Phrases:** "peristimulus time histogram", "trial-averaged response", "mean firing rate"

```python
bin_size_s = 0.05   # match the paper
rates      = counts / bin_size_s   # (n_units, n_trials, n_bins) → Hz
psth       = rates.mean(axis=1)    # (n_units, n_bins) — trial average
# Condition-specific:
for cond in np.unique(labels):
    pop_mean = rates[:, labels == cond, :].mean(axis=(0, 1))   # (n_bins,)
```

#### Communication subspace (reduced-rank regression)

**Phrases:** "communication subspace", "RRR", "predictive subspace", "cross-area
communication", "reduced-rank regression"

```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold

def reduced_rank_regression(X, Y, rank, alpha=1.0, seed=42):
    ridge     = Ridge(alpha=alpha).fit(X, Y)
    B         = ridge.coef_.T
    U, s, Vt  = np.linalg.svd(B, full_matrices=False)
    cv        = KFold(n_splits=5, shuffle=True, random_state=seed)
    r2s = []
    for train, test in cv.split(X):
        ridge_cv      = Ridge(alpha=alpha).fit(X[train], Y[train])
        U_cv, s_cv, Vt_cv = np.linalg.svd(ridge_cv.coef_.T, full_matrices=False)
        B_rr          = U_cv[:, :rank] @ np.diag(s_cv[:rank]) @ Vt_cv[:rank, :]
        Y_pred        = X[test] @ B_rr
        ss_res        = np.sum((Y[test] - Y_pred) ** 2)
        ss_tot        = np.sum((Y[test] - Y[test].mean(0)) ** 2)
        r2s.append(1 - ss_res / ss_tot)
    return U[:, :rank], float(np.mean(r2s))
```

#### Noise and signal correlations

**Phrases:** "noise correlations", "signal correlations", "rsc", "pairwise
correlations", "trial-to-trial variability"

```python
def compute_correlations(counts, labels):
    # counts: (n_units, n_trials)
    conds       = np.unique(labels)
    means       = np.stack([counts[:, labels == c].mean(1) for c in conds])
    signal_corr = np.corrcoef(means.T)
    residuals   = counts.copy().astype(float)
    for c in conds:
        m = labels == c
        residuals[:, m] -= residuals[:, m].mean(1, keepdims=True)
    noise_corr = np.corrcoef(residuals)
    triu = np.triu_indices(counts.shape[0], k=1)
    return signal_corr[triu], noise_corr[triu]
```

### Saving to file

Save the notebook to `{first_author}_{year}/{first_author}_{year}.ipynb`.

**File paths inside the notebook:** nbconvert executes notebooks with cwd set to the
notebook's own directory. Use bare filenames for outputs — `stability.png`, not
`{first_author}_{year}/stability.png`. The latter resolves to a nonexistent subdirectory
and raises `FileNotFoundError`.
If a local PDF was provided, copy or symlink it to `{first_author}_{year}/paper.pdf`.
After the user confirms the Step 3 mapping, write `paper_replication_plan.md` immediately
— don't wait until the notebook is done. Write `report.md` last, after Step 6.

---

## Step 6: Flag Deviations

End the notebook (and the chat response) with this three-way breakdown. Do not bury it.

> **Faithful** — what exactly follows the paper:
> - bin size, window, normalization match paper exactly
> - same decoder class / statistical test
>
> **Adapted** — what was changed to fit the user's data, and why:
> - paper's species / task differs from Dynamic Routing dataset
> - used `default_qc` as a proxy for paper's ISI-based quality filter
> - fewer sessions than paper (N=X vs. paper's N=Y)
>
> **Uncertain** — anywhere you had to guess:
> - parameter not stated in paper (e.g., regularization C)
> - method depends on a cited prior paper that wasn't accessible
> - ambiguous preprocessing step in the Methods text

---

## Gotchas

**Never:**
- Load `spike_times` without first filtering to a specific unit set
- Run fleet-wide spike loading without warning the user — it's slow
- Assume paper region names match NWB `location` — always verify first
- Silently substitute a missing condition with something else — flag it in Step 3
- Load raw TimeSeries (LFP, continuous ephys) unless the paper analyzes LFP

**Always:**
- Show the mapping and get confirmation (Step 3) before writing analysis code
- Report sessions passed vs. failed inclusion criteria
- Match the paper's bin size, window, and normalization exactly — these matter
- Inspect `trials` schema on one file before assuming which columns exist
- Note when the data doesn't match the paper's conditions (different task, species, etc.)

**Common mismatches:**
- Paper uses calcium imaging; NWB has ephys — methods don't transfer directly
- Paper reports "z-scored to baseline"; baseline bins must be before event onset (negative `t_start`)
- Paper uses LDA; don't swap in logistic regression without noting the change
- Paper normalizes per-unit then averages, or averages then normalizes — order matters, check Methods

**pynwb reminders:**
- `nwb.units["spike_times"][i]` returns a VectorData — wrap in `np.array()`
- `nwb.trials.to_dataframe()` can be slow — select only needed columns
- Always open with `load_namespaces=True`

---

## When not to use this skill

- User wants to **understand** the paper, not apply it → discuss directly, no notebook needed
- User wants a **from-scratch** analysis on their data, not tied to a specific paper → different workflow
- User wants to **write up** results in paper style → writing task, not this

---

## Allen Institute Dynamic Routing Dataset

When applying analyses to `s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/`:

**Task:** Context-dependent multisensory decision-making. Mice report stimulus
detection (visual grating or auditory tone). Context block determines which modality
is rewarded and switches multiple times per session (~3–5 blocks).

**Brain region column — schema-version dependent:**
- **Older sessions (2023, e.g. `686176_2023-12-04`):** `location` (and `structure`) exist directly in the `units` table
- **Newer sessions (2024+, e.g. `733780_2024-08-27`):** `location` is **not** in `units`; it is only in `general/extracellular_ephys/electrodes`

For mixed-version fleets, scan `electrodes` to get region coverage — it works for all sessions and is faster than `units`:
```python
import lazynwb, polars as pl
lazynwb.config.use_obstore = False
lazynwb.config.fsspec_storage_options = {"anon": True}
lf = lazynwb.scan_nwb(nwb_paths, "electrodes", ignore_errors=True)
sessions_with_visp = (
    lf.select("_nwb_path", "location")
      .filter(pl.col("location").str.starts_with("VISp"))
      .select("_nwb_path").unique().collect()
)
```
When loading spike times per region for analysis, always use `peak_electrode` (units table) joined against `electrodes.location` for 2024+ sessions, or `units.location` directly for 2023 sessions.

**Trials are at `intervals/trials` (not a top-level `trials` group).** Key columns:
- `rewarded_modality` — context: which modality is rewarded this block
- `stim_name` — stimulus identity string
- `is_vis_stim`, `is_aud_stim` — boolean: stimulus type this trial
- `is_vis_target`, `is_aud_target` — boolean: whether this was the target
- `is_vis_rewarded`, `is_aud_rewarded` — boolean: context flags
- `block_index` — block number (context switches between blocks)
- `is_hit`, `is_false_alarm`, `is_correct_reject`, `is_miss` — behavioral outcome
- `response_time` — reaction time in seconds
- `start_time`, `stim_start_time`, `stim_stop_time`, `stop_time` — timing

**Common analysis entry points:**
- Decode `is_vis_stim` / `is_aud_stim` from VISp or AUD units across time
- Decode `rewarded_modality` (context) from ACA, PFC, or MOs units
- Communication subspace between VISp ↔ ACA or VISp ↔ MOs
- Noise correlations within VISp or ACA during hit vs. miss trials
- PCA population trajectories: vis-rewarded blocks vs. aud-rewarded blocks

**Gotcha:** Context (`rewarded_modality`) switches mid-session at `block_index`
boundaries — always segment trials by block when the paper's analysis assumes a
stationary context.

**Loading trials via h5py** (since they're in `intervals/trials`, not pynwb
`nwb.trials`):
```python
trials_grp = f["intervals"]["trials"]
trial_cols  = {col: trials_grp[col][:] for col in trials_grp.keys()
               if col not in ("id",)}
```
