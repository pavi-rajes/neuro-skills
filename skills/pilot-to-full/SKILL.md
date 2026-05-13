---
name: pilot-to-full
description: >
  Scale a confirmed AutoDiscovery finding from the 5-session NWB pilot to the full
  ~114-session S3 cohort. Use when the user wants to run a pilot experiment on more
  sessions — phrases like "scale this to the full dataset", "run on all sessions",
  "does this hold at full N", "pilot-to-full", "load new sessions", "run on the full
  cohort", "expand to all NWB files". Takes a run ID and experiment ID; loads the
  AutoDiscovery-generated NWB code, finds all matching sessions on S3, and reruns
  the analysis at scale.
argument-hint: <runid> <experiment_id>
user-invocable: true
---

# Pilot-to-Full

Loads the NWB-based code from an AutoDiscovery experiment, finds all sessions in the
full S3 fleet that match the same regions and task conditions, and reruns the analysis
at scale. A PASS/FLAG finding at N=5 is a **Constraint**. This skill tests whether
it upgrades to a **Resolution**.

---

## The core loop

1. **Load** — fetch the experiment code and identify regions from the AutoDiscovery run
2. **Enumerate** — scan the full S3 fleet for sessions matching those regions
3. **Confirm** — show session count and coverage; wait for sign-off
4. **Patch** — replace the local `datasets` list with filenames; inject a configurable path resolver that accepts either an S3 base URL or a local `DATA_DIR` (e.g. a Code Ocean data asset mount)
5. **Run** — execute the patched analysis in a notebook across all eligible sessions
6. **Report** — per-session results, group statistics, and Constraint/Resolution verdict

---

## Output folder

```
autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/
├── session_manifest.csv     # eligible sessions with region unit counts
├── pilot_to_full.ipynb      # patched analysis notebook
└── replication_report.md    # verdict + per-session summary
```

---

## Step 1 — Load the Experiment Code

```bash
asta autodiscovery experiments <runid> --format json
```

Parse the JSON array and find the target experiment by `experiment_id`:

```python
import json, subprocess

result = subprocess.run(
    ["asta", "autodiscovery", "experiments", "<runid>", "--format", "json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
experiments = data if isinstance(data, list) else data.get("experiments", [])

exp = next(e for e in experiments if e["experiment_id"] == "<experiment_id>")
code     = exp["code"]
analysis = exp["analysis"]
review   = exp["review"]
```

If no experiment_id is specified, list all SUCCEEDED experiments and ask the user
which one to scale.

---

## Step 2 — Extract Regions from the Code

The AutoDiscovery code embeds region filters as string-match patterns. Extract them
before doing anything else — they define which sessions are eligible.

Scan the code for these patterns:

| Pattern | Example | What to extract |
|---|---|---|
| `str.contains('...')` | `'CA1\|CA2\|CA3\|DG'` | split on `\|`, strip quotes |
| `str.startswith('...')` | `'VISp'` | take the prefix string |
| `region_substructures = [...]` | `['PL', 'ILA', 'ACAd']` | take the list |
| `REGIONS_MAP = {...}` | `{'PFC': ['PL','ILA'], 'MOs': ['MOs']}` | flatten all values |
| string literals near `'structure'` | `units[units['structure'] == 'MOs']` | take the value |

```python
import re

region_patterns = []

# Pattern: str.contains('A|B|C')
for m in re.finditer(r"str\.contains\(['\"]([^'\"]+)['\"]", code):
    region_patterns += [p.strip() for p in m.group(1).split("|")]

# Pattern: startswith('X')
for m in re.finditer(r"startswith\(['\"]([^'\"]+)['\"]", code):
    region_patterns.append(m.group(1).strip())

# Pattern: list literal assigned near 'structure' or 'region'
for m in re.finditer(r"(?:structure|region)[^\[]*\[([^\]]+)\]", code):
    for item in re.findall(r"['\"]([^'\"]+)['\"]", m.group(1)):
        region_patterns.append(item)

region_patterns = sorted(set(r for r in region_patterns if len(r) >= 2))
print("Extracted regions:", region_patterns)
```

Review the extracted list before proceeding. If extraction misses regions
(e.g., they are computed dynamically), read the `analysis` field — it usually
mentions which regions were actually used (e.g., "CA1 units", "VISp and MOs").
Ask the user to confirm if uncertain.

---

## Step 3 — Enumerate Eligible Sessions and Write Manifest

Two-tier scan: `electrodes` table first (fast, works for ALL session versions
including 2024+) to narrow candidates, then `/units` on candidates only for QC
unit counts. **Never use `map_elements` with a lambda** — it defeats polars lazy
evaluation, forces eager row-by-row Python execution, and requires `cloudpickle`.
Use native `str.contains()` expressions instead; they compile to Rust and are
evaluated lazily.

> **Why `electrodes` not `units` for Tier 1?**  
> `electrodes` is a small table (one row per probe channel) with no spike data.  
> `units` carries `spike_times` arrays. Even with column projection, lazynwb must
> open each file header for `/units` which is ~3× slower.  
> More critically: 2024+ NWB sessions do **not** store `location` in `/units` —
> only in `electrodes`. Using `/units` for region presence misses those sessions.

### 3a. List S3 paths

```python
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import lazynwb
import lazynwb.file_io as fio
import polars as pl

fio.config.anon = True   # must be set before any scan_nwb call

s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(
    Bucket="aind-scratch-data",
    Prefix="dynamic-routing/cache/nwb/v0.0.273/"
)
all_paths = [
    f"s3://aind-scratch-data/{o['Key']}"
    for page in pages
    for o in page.get("Contents", [])
    if o["Key"].endswith(".nwb")
]

# region_groups maps a display label → substrings from the pilot code
# e.g. {"PFC": ["ACA","PL","ILA","ORB"], "visual": ["VIS"]}
region_groups = { ... }   # populated from Step 2 extraction
min_units = 5             # read from pilot code (MIN_UNITS or equivalent); fall back to 5
all_patterns = [p for patterns in region_groups.values() for p in patterns]
```

### 3b. Tier 1 — region presence via `electrodes` (fast)

```python
# Build filter using native str.contains — no lambda, no map_elements
region_filter = pl.lit(False)
for p in all_patterns:
    region_filter = region_filter | pl.col("location").str.contains(p)

lf = lazynwb.scan_nwb(all_paths, "electrodes", raise_on_missing=False)
tier1_df = (
    lf
    .select("_nwb_path", "location")
    .filter(pl.col("location").is_not_null())
    .filter(region_filter)
    .unique()
    .collect()
)
candidate_paths = tier1_df["_nwb_path"].unique().to_list()
print(f"Candidate sessions (electrodes Tier 1): {len(candidate_paths)}")
```

### 3c. Tier 2 — QC unit counts from `/units` on candidates only

```python
lf2 = lazynwb.scan_nwb(candidate_paths, "/units", raise_on_missing=False)
units_df = (
    lf2
    .filter(pl.col("default_qc") == True)
    .filter(pl.col("location").is_not_null())
    .filter(region_filter)
    .select("_nwb_path", "location")
    .collect()
)
```

### 3d. Build per-session unit counts and filter

```python
rows = []
for path in units_df["_nwb_path"].unique().to_list():
    locs = units_df.filter(pl.col("_nwb_path") == path)["location"].to_list()

    group_counts = {
        f"n_{label}": sum(1 for loc in locs if any(p in loc for p in patterns))
        for label, patterns in region_groups.items()
    }

    # Only keep sessions that meet min_units for every required group
    if all(v >= min_units for v in group_counts.values()):
        rows.append({
            "nwb_path":        path,
            "filename":        path.split("/")[-1],
            "regions_present": ",".join(sorted(set(locs))),
            **group_counts,
        })

print(f"Sessions with required regions (≥{min_units} units/group): {len(rows)}")
```

### 3f. Save the manifest

```python
import pandas as pd

manifest = pd.DataFrame(rows)
manifest.to_csv(
    f"autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/session_manifest.csv",
    index=False
)
print(manifest.to_string(index=False))
```

The manifest columns are:

| Column | Content |
|---|---|
| `filename` | Bare filename (e.g. `664851_2023-11-16.nwb`) — primary key for path resolution |
| `nwb_path` | Full `s3://` path at enumeration time — retained for reference only |
| `regions_present` | Comma-separated list of all QC-passing locations in this session |
| `n_<group>` | QC unit count for each region group from the pilot code |

The manifest is the single source of truth for Steps 4–6. All subsequent steps
resolve paths from `filename` via the configurable path resolver (see Step 4).

---

## Step 4 — Confirm Before Running

Do not proceed without explicit user confirmation. Present:

> **Scaling plan — please confirm:**
>
> **Pilot:** N=5 sessions (`664851`, `668755`, `713655`, `742903`, `759434`)
> **Regions extracted from code:** `<region_patterns>`
> **Full fleet:** `<len(nwb_paths)>` sessions total
> **Eligible (regions present):** `<len(eligible)>` sessions
> **Passing unit threshold:** `<len(selected_paths)>` sessions
>
> I'll patch the `datasets` list in the pilot code to use bare filenames and
> inject a path resolver. Set `S3_BASE` to load from S3, or set `DATA_DIR`
> to a local mount (e.g. a Code Ocean data asset at `/data/dr-nwb/`).
> The analysis logic is unchanged.
>
> Estimated runtime: ~`<N × seconds_per_session>` minutes
>
> Ready to run?

If fewer than 10 sessions pass after filtering, flag it:
*"Only N sessions pass — the full-cohort test may remain underpowered. Want to
relax the unit threshold or proceed?"*

---

## Step 5 — Patch the Code

Three minimal changes to the pilot code. The goal is to keep filenames as the
stable identifier and let the user switch between S3 and a local data directory
(e.g. Code Ocean data asset) by changing a single config variable.

### 5a. Inject the data-source config block

Prepend this block to the notebook. The user changes exactly one line to switch
between S3 and a local mount:

```python
DATA_SOURCE_CONFIG = """
import os

# ── data source ───────────────────────────────────────────────────────────────
# Set DATA_DIR to a local directory (e.g. Code Ocean data asset) to load files
# from disk.  Leave it as None to load from S3 via the S3_BASE URL instead.
#
# Examples:
#   DATA_DIR = "/data/dr-nwb/"           # Code Ocean mounted asset
#   DATA_DIR = None                       # use S3
#
S3_BASE  = "s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/"
DATA_DIR = None

def _resolve_path(filename):
    if DATA_DIR is not None:
        return os.path.join(DATA_DIR, filename)
    return S3_BASE + filename

"""
```

Inject this at the very top of the patched code (before any imports).

### 5b. Replace the `datasets` list with filenames

Find the hardcoded list (named `datasets`, `FILES`, `NWB_FILES`, or similar) and
replace it with bare filenames from the manifest:

```python
import re

# filenames is a list of bare filenames: ['664851_2023-11-15.nwb', ...]
filename_list_str = "[\n" + ",\n".join(f'    "{fn}"' for fn in filenames) + "\n]"

# Replace any assignment that looks like: varname = ['...nwb', ...]
patched_code = re.sub(
    r"(datasets|FILES|NWB_FILES|file_list|nwb_files|nwb_paths)\s*=\s*\[[^\]]*\]",
    rf"\1 = {filename_list_str}",
    code,
    flags=re.DOTALL
)
```

Then replace every use of the list variable in the loop with `_resolve_path(filename)`:

```python
# If the pilot iterates: for path in datasets:
#   replace loop body's open call with _resolve_path(path)
# This is handled automatically by 5c below since _open_nwb calls _resolve_path.
```

### 5c. Patch the file-open call

The pilot opens files locally with `NWBHDF5IO(path, 'r')`. Replace with an
`_open_nwb` helper that calls `_resolve_path` and handles both S3 (via fsspec)
and local paths transparently:

```python
OPEN_NWB_HELPER = """
import fsspec as _fsspec

def _open_nwb(filename):
    path = _resolve_path(filename)
    if path.startswith("s3://"):
        _fs = _fsspec.filesystem("s3", anon=True)
        return NWBHDF5IO(_fs.open(path, "rb"), "r", load_namespaces=True)
    return NWBHDF5IO(path, "r", load_namespaces=True)

"""

# Inject after the last pynwb import line
patched_code = re.sub(
    r"(from pynwb import NWBHDF5IO\n)",
    r"\1" + OPEN_NWB_HELPER,
    patched_code,
    count=1
)

# Replace all NWBHDF5IO(var, 'r') open calls with _open_nwb(var)
patched_code = re.sub(
    r"(?:pynwb\.)?NWBHDF5IO\((\w+),\s*['\"]r['\"]\)",
    r"_open_nwb(\1)",
    patched_code
)
```

### 5d. Handle `nwb.trials` for newer sessions

Some 2024+ NWB files put trials in `intervals/trials`, not `nwb.trials`.
Add a compatibility shim after the open call if the code uses `nwb.trials`:

```python
TRIALS_SHIM = """
    # Compatibility: newer sessions store trials in intervals/trials
    if nwb.trials is None and 'trials' in nwb.intervals:
        import types
        _mock = types.SimpleNamespace()
        _mock.to_dataframe = lambda: nwb.intervals['trials'].to_dataframe()
        nwb = types.SimpleNamespace(**{k: getattr(nwb, k) for k in dir(nwb) if not k.startswith('_')})
        nwb.trials = _mock
"""
```

Insert the shim on the line after `nwb = io.read()`.

---

## Step 6 — Build and Run the Notebook

### 6a. Create the artifacts folder

```bash
mkdir -p autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/artifacts
```

### 6b. Patch figure-save calls to write into artifacts/

Before writing the notebook, redirect all figure output in the pilot code to
`artifacts/`. The pilot code typically calls `plt.savefig(...)` or `plt.show()`.

```python
import re, os

artifacts_dir = "autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/artifacts"

# Redirect existing plt.savefig(...) calls to artifacts/
def redirect_savefig(code, artifacts_dir):
    def replace_path(m):
        orig = m.group(1)
        fname = os.path.basename(orig.strip("'\""))
        return f"plt.savefig('{artifacts_dir}/{fname}'"
    return re.sub(r"plt\.savefig\(([^)]+)", replace_path, code)

patched_code = redirect_savefig(patched_code, artifacts_dir)

# Replace bare plt.show() with savefig + show so figures are always saved
fig_counter = [0]
def replace_show(m):
    fig_counter[0] += 1
    return (
        f"plt.savefig('{artifacts_dir}/figure_{fig_counter[0]:02d}.png', "
        f"dpi=150, bbox_inches='tight')\n"
        f"plt.show()"
    )

patched_code = re.sub(r"plt\.show\(\)", replace_show, patched_code)
```

### 6c. Write, convert, and execute

```python
notebook_py = f"""# %%
# pilot-to-full: <experiment_id>
# Original run: <runid>  |  Hypothesis: <hypothesis[:80]>...
# Scaled from N=5 pilot to N=<N> sessions

{patched_code}
"""

py_path = "autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/pilot_to_full.py"
with open(py_path, "w") as f:
    f.write(notebook_py)
```

```bash
jupytext --to ipynb autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/pilot_to_full.py
rm autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/pilot_to_full.py
```

Execute and save the output notebook (use `python3 -m nbconvert` — the `jupyter`
CLI alias may not be installed):

```bash
python3 -m nbconvert --to notebook --execute \
    --ExecutePreprocessor.timeout=7200 \
    --output pilot_to_full_executed.ipynb \
    --output-dir autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/ \
    autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/pilot_to_full.ipynb
```

The output folder now contains:

```
autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/
├── session_manifest.csv
├── pilot_to_full.ipynb             # source notebook (no outputs)
├── pilot_to_full_executed.ipynb    # executed notebook with all cell outputs
├── artifacts/
│   ├── figure_01.png               # figures saved by the analysis
│   ├── figure_02.png
│   └── ...
└── replication_report.md           # written in Step 7
```

If execution fails, read the traceback from the failed cell in
`pilot_to_full_executed.ipynb` and diagnose.
Common issues:

| Error | Fix |
|---|---|
| `nwb.trials is None` | trials shim not applied — add manually |
| `'structure' not in units.columns` | 2024+ sessions use `location` column — patch region filter |
| `FileNotFoundError` on S3 path | wrong path format — re-run nwb-s3-browser to verify paths |
| `fsspec` S3 timeout | add `requester_pays=False` to fsspec options |
| Memory error | process sessions in batches of 20 |

---

## Step 7 — Write the Replication Report

Save to `autodiscovery-runs/<run_name>/pilot-to-full/<experiment_id>/replication_report.md`.

Extract the key result from the notebook output cells and write:

```markdown
# Replication Report: <experiment_id>

**Date:** <YYYY-MM-DD>
**Original run:** <runid>
**Hypothesis:** <full text>
**Pilot finding:** <one sentence from analysis field>
**Verdict:** RESOLUTION / CONSTRAINT / REVERSAL / FAIL TO REPLICATE

---

## Session coverage

| | Pilot | Full cohort |
|---|---|---|
| Sessions attempted | 5 | <N_selected> |
| Sessions succeeded | 5 | <N_ok> |
| Sessions skipped/failed | 0 | <N_fail> |

**Regions:** <region_patterns>

---

## Result

<Paste the key quantitative result from notebook output — effect sizes, p-values,
per-session breakdown. Do not paraphrase; copy the printed output.>

---

## Verdict

Apply this decision tree:

- **RESOLUTION** — effect replicates (p < 0.05, consistent direction across majority of sessions)
- **CONSTRAINT** — direction consistent but not significant, or significant in subset only
- **REVERSAL** — significant but opposite direction to pilot
- **FAIL TO REPLICATE** — effect absent in majority of sessions

State the verdict in one sentence, then connect it to the pilot's contribution type:
"This finding [upgrades from Constraint to Resolution / remains a Constraint / reverses]
at N=<full_N> sessions."
```

---

## Behavior notes

- **Do not rewrite the analysis** — patch only the file list and open call. Method
  drift is indistinguishable from biology drift when comparing pilot vs. full N.
- **Patch minimally** — three injections (config block, filename list, open helper).
  If the code resists clean patching, show the user the specific lines to change and
  ask them to confirm before proceeding.
- **Filename is the stable identifier** — the manifest stores `filename` as the primary
  key. `nwb_path` is retained for reference but not used at runtime. The notebook
  resolves the full path via `_resolve_path(filename)` at load time, so switching
  from S3 to Code Ocean requires only changing `DATA_DIR` in the config cell.
- **Code Ocean data asset** — on Code Ocean, NWB files in a data asset are typically
  mounted at `/data/<asset-name>/`. Set `DATA_DIR = "/data/<asset-name>/"` in the
  config cell. The `filename` column in the manifest must match the filenames in the
  mounted directory exactly.
- **`structure` vs `location`** — the pilot code filters on `units['structure']`. In
  2024+ NWB sessions this column may be absent; `units['location']` is the equivalent.
  Check the first session before running the full fleet and add a column alias if needed:
  ```python
  if 'structure' not in units_df.columns and 'location' in units_df.columns:
      units_df['structure'] = units_df['location']
  ```
- **Warn before long runs** — if N > 30 sessions, estimate runtime and tell the user
  before starting execution.
- **Sessions that skip are not failures** — the pilot code already handles
  missing regions with `continue`. Sessions that skip due to missing regions are
  expected and normal; report them as "skipped" not "failed".
