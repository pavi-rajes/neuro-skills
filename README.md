# neuro-skills

Agent skills for neuroscience data workflows. Drop these into your AI coding assistant to give it domain-specific knowledge for exploring and analyzing NWB datasets on S3.

---

## Skills

### `nwb-s3-browser`

Browse and query NWB (Neurodata Without Borders) datasets stored on public or private S3 buckets — without downloading files. Uses `lazynwb` + `polars` for fast, selective multi-file queries over S3.

**Default bucket:** `s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/` — used automatically when no S3 path is specified. To change it, update the `description` field in `SKILL.md` before deploying.

**Capabilities:**
- List bucket contents: file counts, sizes, subjects, date ranges
- Filter sessions by subject, date, or session count from filenames alone (no file I/O)
- Query NWB content: brain regions, unit counts, quality metrics, epoch tags, trial structure
- Optimizes query speed (fast metadata → medium electrode/trial tables → slow unit scans)
- Built-in support for the Allen Institute Dynamic Routing dataset

**Runtime dependencies:**

```
boto3
botocore
lazynwb      # https://pypi.org/project/lazynwb/
polars
upath
fsspec
h5py
```

---

### `paper-analysis`

Apply a neuroscience analysis from a published paper to NWB data on S3. Accepts a paper PDF path, URL, DOI, or arXiv ID, extracts the analysis from the Methods section, and implements it against an NWB dataset.

**Capabilities:**
- Fetch papers from DOIs, URLs, arXiv IDs, or local PDFs
- Extract analysis requirements: regions, trial windows, bin sizes, normalization, quality thresholds
- Select sessions from S3 that meet the paper's inclusion criteria (via `lazynwb`)
- Load spike times for selected units via `pynwb`
- Templates for common analyses: linear decoding, PCA/trajectories, PSTH, communication subspace (RRR), noise/signal correlations
- Built-in support for the Allen Institute Dynamic Routing dataset

**Runtime dependencies:**

```
boto3
botocore
lazynwb
polars
upath
fsspec
h5py
pynwb
numpy
scikit-learn
matplotlib
```

---

## Example Queries

Once deployed, try asking your agent. You can tell it your bucket once per session and skip the path in follow-up questions:

```
"Remember s3://my-bucket/nwb/ as my default dataset"
"Which subjects have at least 4 sessions?"
"Which sessions have an optotagging epoch?"
"Find sessions with VISp and CA1 co-recorded"
```

Or include the path explicitly each time:


**Bucket exploration:**
- `"What's in s3://my-bucket/data/ ?"`
- `"How many sessions and subjects are in this bucket? s3://my-bucket/nwb/"`
- `"Summarize the dataset at s3://my-bucket/data/ — file count, size, subjects, date range"`

**Session filtering (fast, no file reads):**
- `"Find all sessions for subject 366122 in s3://my-bucket/nwb/"`
- `"Which subjects have at least 5 sessions?"`
- `"List sessions recorded in October 2024"`

**Brain region queries:**
- `"Which sessions in s3://my-bucket/nwb/ have recordings in visual cortex?"`
- `"Find all NWB files with hippocampus recordings at s3://my-bucket/nwb/"`
- `"Which sessions in s3://my-bucket/nwb/ recorded both VISp and CA1 simultaneously?"`
- `"What brain regions are covered across s3://my-bucket/nwb/?"`

**Unit quality and counts:**
- `"Which sessions in s3://my-bucket/nwb/ have at least 50 good units in VISp?"`
- `"Find sessions in s3://my-bucket/nwb/ with enough CA1 neurons for decoding (>30 good units)"`
- `"Show me high-firing-rate units in motor cortex with presence_ratio > 0.95 in s3://my-bucket/nwb/"`

**Paper analysis:**
- `"Apply the decoding analysis from doi:10.1016/j.neuron.2019.01.023 to s3://my-bucket/nwb/"`
- `"Replicate figure 3 from https://arxiv.org/abs/2310.12345 on our dataset"`
- `"Use the communication subspace method from Semedo et al. 2019 on VISp and ACA"`
- `"Run the noise correlation analysis from this PDF: /path/to/paper.pdf"`

**Allen Dynamic Routing specific:**
- `"Summarize the dataset at s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/"`
- `"How many sessions have both visual context block as the first block?"`
- `"Find sessions suitable for VISp↔MOs communication subspace analysis in s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/"`

---

## Deployment

The skill is a single file. Run the commands below from your project root — they download `SKILL.md` directly from GitHub.

### Claude Code (CLI or VS Code extension)

Claude Code reads `CLAUDE.md` automatically at the start of every session.

```bash
# nwb-s3-browser only
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md >> CLAUDE.md

# paper-analysis only
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/paper-analysis/SKILL.md >> CLAUDE.md

# both skills
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md >> CLAUDE.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/paper-analysis/SKILL.md >> CLAUDE.md
```

The VS Code Claude extension (Claude Code for VS Code) uses the same `CLAUDE.md` mechanism — no extra steps needed.

---

### Claude.ai Projects

Add one or both skills to your Project Knowledge:
- [nwb-s3-browser SKILL.md](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/nwb-s3-browser/SKILL.md)
- [paper-analysis SKILL.md](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/paper-analysis/SKILL.md)

Open the file, copy its contents, then go to your Project → **Project Knowledge** → **Add content** and paste.

Active for all conversations in that project.

---

### Cursor

Cursor reads agent rules from `.cursor/rules/*.mdc` files. The SKILL.md frontmatter is compatible with the `.mdc` format.

**Project-scoped** (active only in this repo):

```bash
mkdir -p .cursor/rules
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md -o .cursor/rules/nwb-s3-browser.mdc
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/paper-analysis/SKILL.md -o .cursor/rules/paper-analysis.mdc
```

**Global** (active in every Cursor project):

```bash
mkdir -p ~/.cursor/rules
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md -o ~/.cursor/rules/nwb-s3-browser.mdc
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/paper-analysis/SKILL.md -o ~/.cursor/rules/paper-analysis.mdc
```

The `description` in the frontmatter tells the Cursor agent when to activate the skill (e.g. when you mention an `s3://` path with `.nwb` files).

---

### GitHub Copilot in VS Code

**Workspace instructions** (VS Code 1.96+, active in this repo):

```bash
mkdir -p .github
# Concatenate both skills into a single instructions file
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md > .github/copilot-instructions.md
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/paper-analysis/SKILL.md >> .github/copilot-instructions.md
```

Copilot Chat automatically includes `.github/copilot-instructions.md` for all requests in the workspace.

**User-level instructions** (global, all workspaces):

1. Open VS Code Settings (`Cmd+,`) and search for `copilot instructions`
2. Under **GitHub Copilot › Chat: Code Generation Instructions**, click **Add Item**
3. Paste the contents of [SKILL.md](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/nwb-s3-browser/SKILL.md)
