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

## Example Queries

Once deployed, try asking your agent:

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
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md >> CLAUDE.md
```

The VS Code Claude extension (Claude Code for VS Code) uses the same `CLAUDE.md` mechanism — no extra steps needed.

---

### Claude.ai Projects

1. Open [SKILL.md](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/nwb-s3-browser/SKILL.md) and copy its contents
2. Go to your Project → **Project Knowledge** → **Add content** and paste

Active for all conversations in that project.

---

### Cursor

Cursor reads agent rules from `.cursor/rules/*.mdc` files. The SKILL.md frontmatter is compatible with the `.mdc` format.

**Project-scoped** (active only in this repo):

```bash
mkdir -p .cursor/rules
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md -o .cursor/rules/nwb-s3-browser.mdc
```

**Global** (active in every Cursor project):

```bash
mkdir -p ~/.cursor/rules
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md -o ~/.cursor/rules/nwb-s3-browser.mdc
```

The `description` in the frontmatter tells the Cursor agent when to activate the skill (e.g. when you mention an `s3://` path with `.nwb` files).

---

### GitHub Copilot in VS Code

**Workspace instructions** (VS Code 1.96+, active in this repo):

```bash
mkdir -p .github
curl -sL https://raw.githubusercontent.com/pavi-rajes/neuro-skills/main/skills/nwb-s3-browser/SKILL.md -o .github/copilot-instructions.md
```

Copilot Chat automatically includes `.github/copilot-instructions.md` for all requests in the workspace.

**User-level instructions** (global, all workspaces):

1. Open VS Code Settings (`Cmd+,`) and search for `copilot instructions`
2. Under **GitHub Copilot › Chat: Code Generation Instructions**, click **Add Item**
3. Paste the contents of [SKILL.md](https://github.com/pavi-rajes/neuro-skills/blob/main/skills/nwb-s3-browser/SKILL.md)
