---
name: nwb-s3-browser
description: >
  Browse and query NWB neuroscience datasets stored on S3. Trigger when the user provides a public
  s3:// path containing .nwb files and wants to know what's in the bucket, how many sessions,
  which subjects, file sizes, or wants to query NWB content (brain regions, unit counts, quality
  metrics, trial structure). Also trigger on phrases like "tell me about the files in s3://...",
  "what sessions are in this bucket", "explore this NWB dataset", "find recordings with VISp".
  If no S3 path is provided but the question is about NWB sessions, subjects, brain regions,
  units, or epochs, use the default bucket: s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/
---

# NWB S3 Browser

> This skill uses `lazynwb` + `polars` for fast, selective, multi-file table workflows.
> Best suited for **ecephys datasets** (units, electrodes, trials) stored as NWB on public S3.

## Purpose

Given an S3 path containing NWB files:
1. **List** — what files exist, how many, sizes, subjects, date ranges
2. **Find by filename** — locate sessions by subject or date without opening any files
3. **Query NWB** — open files to inspect structure, find by brain region / unit quality / epochs / task variables

---

## Step 1: List the Bucket (boto3, no NWB reading)

> **Note:** This skill assumes a **public S3 bucket** accessed with anonymous (unsigned) credentials.

Always start here. Use `boto3` with anonymous access for public buckets.

```python
import boto3
from botocore import UNSIGNED
from botocore.config import Config

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket='bucket-name', Prefix='path/to/prefix/')
objs = [obj for page in pages for obj in page.get('Contents', [])]
```

If the bucket is private and the user has credentials, omit the `Config(signature_version=UNSIGNED)` — boto3 will pick up credentials from `~/.aws/` or environment variables automatically.

### Parse filenames and report

NWB files in neuroscience datasets are typically named `{subject_id}_{date}.nwb`. Parse these to summarize:

```python
from collections import defaultdict

subjects = defaultdict(lambda: {'dates': [], 'sizes': []})
for o in objs:
    fname = o['Key'].split('/')[-1].replace('.nwb', '')
    parts = fname.split('_')
    if len(parts) == 2:
        subj, date = parts
        subjects[subj]['dates'].append(date)
        subjects[subj]['sizes'].append(o['Size'])

total_size = sum(o['Size'] for o in objs)
print(f"Total: {len(objs)} files, {total_size/1e9:.1f} GB, {len(subjects)} subjects")
for subj in sorted(subjects):
    dates = sorted(subjects[subj]['dates'])
    gb = sum(subjects[subj]['sizes']) / 1e9
    print(f"  {subj}: {len(dates)} sessions, {dates[0]} to {dates[-1]}, {gb:.1f} GB")
```

**Always report:**
- Total file count and size
- Number of unique subjects
- Per-subject: session count, date range, total size
- File size range (min/max/avg) — flag outliers

---

## Step 2: Find by Filename (instant, no NWB reading)

Use the `objs` and `subjects` dicts from Step 1. No files are opened.

**Triggers:** "find sessions for mouse X", "which subjects have at least N sessions", "sessions from October 2024"

```python
# All sessions for a subject
target = "366122"
matching = [o for o in objs if target in o['Key'].split('/')[-1]]
print(f"{len(matching)} sessions for subject {target}")

# Subjects with at least N sessions
min_sessions = 3
for subj, info in sorted(subjects.items()):
    if len(info['dates']) >= min_sessions:
        print(f"  {subj}: {len(info['dates'])} sessions")

# Sessions in a date range
from_date, to_date = "2024-10-01", "2024-10-31"
for o in objs:
    fname = o['Key'].split('/')[-1].replace('.nwb', '')
    parts = fname.split('_')
    if len(parts) == 2 and from_date <= parts[1] <= to_date:
        print(f"  {fname}")
```

---

## Step 3: Query NWB Content (opens files via lazynwb)

Everything in this step reads NWB file contents over S3. Always try the fastest sufficient query.

### Speed tiers

| Tier | Data source | Speed | Use for |
|------|-------------|-------|---------|
| **Fast** | `epochs`, `session` | Seconds–low minutes | Epoch filtering, session metadata, experiment description |
| **Medium** | `electrodes`, `trials` | Minutes | Region presence, trial conditions |
| **Slow** | `units` | Minutes–tens of minutes | Unit counts, quality filtering, firing rates, co-recording |

⚠️ **Before running Medium or Slow queries across many sessions on S3, warn the user about expected time.**

### Setup

> **Anonymous access:** Set `anon=True` in the lazynwb config **before** any `scan_nwb` call. Without it, lazy table loading fails with "Failed to open as HDF5 or Zarr" on every file.

```python
import lazynwb
import polars as pl
from upath import UPath

lazynwb.config.use_obstore = False
lazynwb.config.fsspec_storage_options = {"anon": True}  # must be set before scan_nwb

nwb_paths = list(UPath("s3://bucket/prefix/").glob("**/*.nwb"))
```

> **Private buckets:** omit `anon: True` — boto3/fsspec will pick up `~/.aws/` credentials automatically.

### Brain region column location

**Prefer scanning `electrodes` for region-based selection** — it is the most reliable source across datasets, faster than `units`, and works even when `location` is absent from the units table:

```python
lf = lazynwb.scan_nwb(nwb_paths, "electrodes", ignore_errors=True)
sessions_with_region = (
    lf
    .select("_nwb_path", "location")
    .filter(pl.col("location").str.starts_with("VISp"))
    .select("_nwb_path").unique()
    .collect()
)
```

**Which table answers which question:**
- `electrodes` — "what brain structure did each recording site pass through?" (per-channel, anatomical trajectory)
- `units` — "what structure is each neuron assigned to?" (per-unit, spike-sorted assignment); `location` may or may not be present depending on the dataset version — always verify on one file first

### Region name normalization

Always normalize user language before querying. Then verify against actual values in the data.

| User says | Query for |
|-----------|-----------|
| "hippocampus" | `CA1`, `CA3`, `DG` |
| "visual cortex" / "V1" | `VISp`, `VISl`, `VISrl`, `VISam`, `VISpm` |
| "motor cortex" | `MOs`, `MOp` |
| "prefrontal" | `ACA`, `ORB`, `PFC` |
| "auditory" | `AUD` |
| "thalamus" | `LP`, `LGd` (check what's present) |
| "ACC" | `ACA` |

**Important:** NWB region names often include layer suffixes (`VISp2/3`, `VISp5`).
Use `str.starts_with("VISp")`, never exact equality, unless the user specifies a layer.

---

### 3.1 Discover tables (Fast — always do this first on one file)

```python
import h5py, fsspec

fs = fsspec.filesystem("s3", anon=True)  # drop anon=True for private buckets
with h5py.File(fs.open(nwb_paths[0], "rb"), "r") as f:
    f.visititems(lambda name, obj: print(name))
```

Common tables: `units`, `electrodes`, `trials`, `intervals/*`, `session`

---

### 3.2 Session metadata (Fast)

```python
lf_session = lazynwb.scan_nwb(nwb_paths, "session")
print(lf_session.schema)
print(lf_session.collect())
```

---

### 3.3 Find by epoch (Fast)

Epochs (`/intervals/epochs`) is a lightweight session-level table — one row per epoch with `start_time`, `stop_time`, and typically `tags` or custom columns. Scanning it across files is fast.

**Triggers:** "which sessions have optotagging", "find subjects with a visual context block", "how many sessions have this task phase"

```python
# First: check what the epochs table looks like on one file
lf_epochs = lazynwb.scan_nwb(nwb_paths[:1], "epochs")
print(lf_epochs.schema)
print(lf_epochs.limit(5).collect())

# Then: find sessions with a specific epoch tag
# (adjust column name and filter based on actual schema)
lf_epochs = lazynwb.scan_nwb(nwb_paths, "epochs")
sessions_with_epoch = (
    lf_epochs
    .filter(pl.col("tags").str.contains("optotagging"))
    .select("_nwb_path")
    .unique()
    .collect()
)
print(f"{len(sessions_with_epoch)} sessions with optotagging epoch")
```

> **Note:** The epoch schema varies across datasets. Always inspect on one file first. If `epochs` doesn't exist, fall back to `trials` or `intervals/*`.

---

### 3.4 Find by brain region — presence (Medium)

**Triggers:** "which sessions have VISp", "find recordings with hippocampus", "sessions that include auditory cortex"

```python
# Option A: electrodes table (faster — no quality filtering)
lf_elec = lazynwb.scan_nwb(nwb_paths, "electrodes")
sessions_with_region = (
    lf_elec
    .select("_nwb_path", "location")
    .unique()
    .filter(pl.col("location").str.starts_with("VISp"))
    .select("_nwb_path")
    .unique()
    .collect()
)

# Option B: units table (slower — reflects actual sorted units)
lf_units = lazynwb.scan_nwb(nwb_paths, "units")
sessions_with_region = (
    lf_units
    .select("_nwb_path", "location")
    .unique()
    .filter(pl.col("location").str.starts_with("VISp"))
    .select("_nwb_path")
    .unique()
    .collect()
)
```

---

### 3.5 Find by co-recorded regions (Medium)

Sessions where region A AND region B are both recorded.

**Triggers:** "sessions with both VISp and CA1", "find recordings with visual and hippocampal areas simultaneously"

```python
target_regions = ["VISp", "CA1"]

lf = lazynwb.scan_nwb(nwb_paths, "units")
regions_per_session = (
    lf
    .select("_nwb_path", "location")
    .unique()
    .collect()
)

matching_sessions = []
for session in regions_per_session["_nwb_path"].unique():
    session_regions = (
        regions_per_session
        .filter(pl.col("_nwb_path") == session)
        ["location"]
        .to_list()
    )
    if all(
        any(r.startswith(target) for r in session_regions)
        for target in target_regions
    ):
        matching_sessions.append(session)

print(f"{len(matching_sessions)} sessions with both {' and '.join(target_regions)}")
```

---

### 3.6 Find by task variable (Medium–Slow)

**Triggers:** "sessions with auditory trials", "find sessions with context switching", "which sessions have visual gratings"

```python
# First: check trial schema on one file
lf_trials = lazynwb.scan_nwb(nwb_paths[:1], "trials")
print(lf_trials.schema)

# Then: filter by task variable (adjust column names based on schema)
lf_trials = lazynwb.scan_nwb(nwb_paths, "trials")
sessions_with_condition = (
    lf_trials
    .filter(pl.col("stimulus_type") == "auditory")
    .select("_nwb_path")
    .unique()
    .collect()
)
print(f"{len(sessions_with_condition)} sessions with auditory trials")
```

---

### 3.7 Find by unit count and quality (Slow)

**Triggers:** "sessions with at least 50 good units in VISp", "which sessions have enough CA1 neurons for decoding"

```python
min_units = 50
target_region = "VISp"

lf = lazynwb.scan_nwb(nwb_paths, "units")
high_yield = (
    lf
    .filter(
        pl.col("location").str.starts_with(target_region),
        pl.col("default_qc") == True,
    )
    .group_by("_nwb_path")
    .agg(pl.len().alias("n_good_units"))
    .filter(pl.col("n_good_units") >= min_units)
    .sort("n_good_units", descending=True)
    .collect()
)
print(f"{len(high_yield)} sessions with >= {min_units} good {target_region} units")
print(high_yield)
```

---

### 3.8 Find by unit properties (Slow)

**Triggers:** "find units with high firing rates in motor cortex", "sessions with presence_ratio > 0.95"

```python
lf = lazynwb.scan_nwb(nwb_paths, "units")
matching_units = (
    lf
    .filter(
        pl.col("location").str.starts_with("MOs"),
        pl.col("default_qc") == True,
        pl.col("firing_rate") > 5.0,
        pl.col("presence_ratio") > 0.95,
    )
    .select("_nwb_path", "unit_id", "location", "firing_rate", "presence_ratio")
    .collect()
)
print(f"{len(matching_units)} units matching criteria")

per_session = (
    matching_units
    .group_by("_nwb_path")
    .agg(pl.len().alias("n_matching"))
    .sort("n_matching", descending=True)
)
print(per_session)
```

---

### 3.9 Region summary across dataset (Slow)

```python
lf = lazynwb.scan_nwb(nwb_paths, "units")
region_summary = (
    lf
    .filter(pl.col("default_qc") == True)
    .group_by("location")
    .agg(pl.len().alias("n_units"))
    .sort("n_units", descending=True)
    .collect()
)
print(region_summary)
```

---

## Gotchas

**Never:**
- Scan raw TimeSeries tables (LFP, raw ephys — sampled at 30kHz+)
- Load `spike_times` without first filtering to specific units
- Load all columns from `units` — always project to the columns you need
- Assume region naming — always check actual values with `SELECT DISTINCT location` first

**Always:**
- Use `_nwb_path` to group results per session in multi-file queries
- Apply `default_qc == True` when reporting "good" units (unless user asks for all)
- Use `.limit()` on exploratory queries
- Use `str.starts_with("VISp")` not exact equality — NWB often has layer suffixes (`VISp2/3`, `VISp5`)
- Inspect schema on one file before querying across all files

**Polars reminders:**
- `group_by` not `groupby`
- No `.apply()` — use expressions
- `.collect()` materializes a LazyFrame

**Warn before slow queries:** Unit-level scans across many large sessions on S3 can take minutes. Tell the user before running.

---

## Allen Institute Dynamic Routing Dataset

When the S3 path is `s3://aind-scratch-data/dynamic-routing/cache/nwb/`:

**Known dataset size (v0.0.273):** 217 sessions, ~1.16 TB, 66 subjects, Aug 2023 – Oct 2025.
Most subjects have 4 consecutive daily sessions. File sizes range from ~4 MB to ~16 GB.

**Task:** Mice respond to multimodal stimuli (visual gratings, auditory tones).
Context block determines which modality is rewarded. Context switches within session.

**Key regions:** VISp, VISl, AUD, MOs, ACA, PFC, ORB, CA1
(typically 5–7 per session across 2 Neuropixels 2.0 probes)

**Epoch tags seen in the wild:** `task`, `rewards`, `mapping`, `spontaneous`, `optotagging`, `opto_control`

**Trial columns to highlight:** stimulus modality, context block, response (lick/no-lick), reward, reaction_time

**Common analysis entry points:**
- Communication subspaces between region pairs (VISp↔MOs, ACA↔VISp)
- Context-dependent gain modulation of sensory responses
- Cross-region decoding of task variables across context switches
