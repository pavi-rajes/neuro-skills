# neuro-skills

Agent skills for neuroscience data workflows. Drop these into your AI coding assistant to give it domain-specific knowledge for exploring NWB datasets on S3 and working with [AutoDiscovery](https://autodiscovery.allen.ai) findings.

---

## Skills

### `nwb-s3-browser`

Browse and query NWB (Neurodata Without Borders) datasets stored on public or private S3 buckets — without downloading files. Uses `lazynwb` + `polars` for fast, selective multi-file queries over S3.

**Default bucket:** `s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/` — used automatically when no S3 path is specified.

**Capabilities:**
- List bucket contents: file counts, sizes, subjects, date ranges
- Filter sessions by subject, date, or session count from filenames alone (no file I/O)
- Query NWB content: brain regions, unit counts, quality metrics, epoch tags, trial structure
- Optimizes query speed (fast metadata → medium electrode/trial tables → slow unit scans)

**Runtime dependencies:**
```
boto3  botocore  lazynwb  polars  upath  fsspec  h5py
```

---

### `paper-analysis`

Apply a neuroscience analysis from a published paper to NWB data on S3. Accepts a paper PDF path, URL, DOI, or arXiv ID, extracts the analysis from the Methods section, and implements it against an NWB dataset.

**Capabilities:**
- Fetch papers from DOIs, URLs, arXiv IDs, or local PDFs
- Extract analysis requirements: regions, trial windows, bin sizes, normalization, quality thresholds
- Select sessions from S3 that meet the paper's inclusion criteria (via `lazynwb`)
- Templates for common analyses: linear decoding, PCA/trajectories, PSTH, communication subspace (RRR), noise/signal correlations

**Runtime dependencies:**
```
boto3  botocore  lazynwb  polars  upath  fsspec  h5py  pynwb  numpy  scikit-learn  matplotlib
```

---

### `experiment-triage`

Triage AutoDiscovery experiments for scientific rigor and mechanistic value. Takes a run ID, fetches the experiment list, and scores each hypothesis for methodological validity, mechanistic depth, and confound risk.

**Capabilities:**
- Filter experiments by verdict (PASS / FLAG), mechanistic score, and novelty
- Identify methodological red flags (small N, confounds, circular logic)
- Rank hypotheses by prior belief, surprise factor, and interpretability
- Output a structured triage JSON consumed by the downstream card skills

---

### `experiment-card`

Build a structured experiment card for a hypothesis from AutoDiscovery. Takes a run ID + experiment ID and produces a card with literature evidence, knowledge map, novelty score, experimental plan, and conservative interpretation.

**Capabilities:**
- Semantic Scholar literature search — supporting, opposing, and contextual papers
- Knowledge map: what is known, what is contested, how this hypothesis contributes
- Novelty tier (T1–T4) and contribution type classification
- Experimental plan with objective, steps, and deliverables

---

### `pilot-to-full`

Scale a confirmed AutoDiscovery finding from the 5-session NWB pilot to the full ~114-session S3 cohort. Takes a run ID and experiment ID, loads the pilot notebook, and re-executes the analysis at full N.

**Capabilities:**
- Loads pilot code from `autodiscovery-results/pilot-to-full/`
- Discovers all available sessions in the S3 cohort via `lazynwb`
- Re-runs the analysis with proper statistical power and saves results

---

### `experiment-card-viewer`

Build or rebuild the self-contained HTML experiment card viewer from triage and card artifacts. The viewer is a single `viewer.html` file — no server required.

**Capabilities:**
- Renders all experiment cards from a triage run in a browsable sidebar
- Knowledge map, literature tabs (supporting / opposing / contextual), belief update chart
- Per-card notes (persisted to disk when served via `serve_viewer.py`)
- "Ask Claude" button — copies the full card context to clipboard and opens `claude.ai/new`

---

## AutoDiscovery Workflow

The skills chain together into a full analysis pipeline:

```
AutoDiscovery run
      │
      ▼
experiment-triage     → scores all experiments, produces triage JSON
      │
      ▼
experiment-card       → builds card per experiment (literature, plan, novelty)
      │
      ├──▶ pilot-to-full       → scales confirmed findings to full cohort
      │
      └──▶ experiment-card-viewer  → renders everything into viewer.html
```

---

## Example Queries

### NWB data exploration

```
"Summarize the dataset at s3://my-bucket/nwb/"
"Which sessions have VISp and CA1 co-recorded?"
"Find sessions with at least 50 good units in motor cortex"
"Apply the decoding analysis from doi:10.1016/j.neuron.2019.01.023 to our dataset"
```

### AutoDiscovery

```
"Triage the experiments from run c003951b"
"Build an experiment card for node_2_2 from run c003951b"
"Scale node_2_2 to the full cohort"
"Rebuild the experiment card viewer"
```

---

## Deployment

Each skill is a single `SKILL.md` file. The commands below append it to your project's instruction file.

### Claude Code

```bash
# Individual skills
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md >> CLAUDE.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/paper-analysis/SKILL.md >> CLAUDE.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/experiment-triage/SKILL.md >> CLAUDE.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/experiment-card/SKILL.md >> CLAUDE.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/pilot-to-full/SKILL.md >> CLAUDE.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/experiment-card-viewer/SKILL.md >> CLAUDE.md
```

### Cursor

```bash
mkdir -p .cursor/rules
for skill in nwb-s3-browser paper-analysis experiment-triage experiment-card pilot-to-full experiment-card-viewer; do
  curl -sL "https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/$skill/SKILL.md" \
    -o ".cursor/rules/$skill.mdc"
done
```

### Claude.ai Projects

Add skill files to **Project Knowledge** → **Add content**:
- [nwb-s3-browser](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/nwb-s3-browser/SKILL.md)
- [paper-analysis](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/paper-analysis/SKILL.md)
- [experiment-triage](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/experiment-triage/SKILL.md)
- [experiment-card](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/experiment-card/SKILL.md)
- [pilot-to-full](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/pilot-to-full/SKILL.md)
- [experiment-card-viewer](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/experiment-card-viewer/SKILL.md)

### GitHub Copilot (VS Code)

```bash
mkdir -p .github
for skill in nwb-s3-browser paper-analysis experiment-triage experiment-card pilot-to-full experiment-card-viewer; do
  curl -sL "https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/$skill/SKILL.md" \
    >> .github/copilot-instructions.md
done
```
