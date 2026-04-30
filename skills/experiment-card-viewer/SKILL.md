---
name: experiment-card-viewer
description: >
  Build or rebuild the self-contained HTML experiment card viewer from triage and card artifacts.
  Use when the user asks to "rebuild the viewer", "update the viewer", "refresh the HTML",
  "show me all experiments", "regenerate the viewer", "open the experiment card viewer", or
  after any change to triage JSONs, literature JSONs, or card markdowns. Also use when adding
  a new run or new experiment cards.
argument-hint: [optional: path to build_viewer.py]
user-invocable: true
---

# Experiment Card Viewer

Generates a self-contained `viewer.html` from all triage, literature, and card artifacts in
`autodiscovery-results/`. The viewer is a single HTML file — no server required, opens in any
browser.

---

## What the Viewer Shows

The viewer has two panes:

**Sidebar** — all PASS and FLAG experiments across all triage runs, sorted by mechanistic
score descending. Each row shows: verdict badge, mech score, surprise delta, experiment ID,
hypothesis preview. Experiments with cards are visually distinguished from those without.

**Main panel** — clicking an experiment loads its card, which has:
- **Header** — run name, experiment ID, AutoDiscovery link, verdict/mech/novelty pills
- **Dataset context strip** — sessions, regions, task extracted from code_output
- **Hero (slide view)** — two-column layout: Gaussian belief shift chart + Prior Work / Method / Result
- **Takeaway strip** — one interpretive sentence extracted from the reflection
- **Section 02 — Literature Evidence** — tabbed: Supporting / Opposing / Contextual / Knowledge Map
- **Section 03 — Experimental Plan** — objective, steps, deliverables
- **Section 05 — Results & Findings** — full analysis text (markdown rendered)
- **Section 06 — Reflection** — full reflection (markdown rendered)

Experiments without cards show a placeholder in the main panel.

---

## Step 1 — Verify Artifacts Exist

The viewer reads from three artifact types:

| Artifact | Location | Required |
|---|---|---|
| Triage JSON | `autodiscovery-results/validation/<runid>_triage.json` | Yes — sidebar won't populate without it |
| Literature JSON | `autodiscovery-results/experiment-cards/literature_evidence/<eid>_literature.json` | No — card renders without it but Prior Work / Knowledge Map will be empty |
| Card markdown | `autodiscovery-results/experiment-cards/<eid>_card.md` | No — sections 03/05/06 will be empty |

Check what's present:

```bash
ls autodiscovery-results/validation/
ls autodiscovery-results/experiment-cards/literature_evidence/
ls autodiscovery-results/experiment-cards/*_card.md 2>/dev/null
```

If triage JSON is missing, run the `experiment-triage` skill first.
If literature JSONs or card markdowns are missing, run the `experiment-card` skill first.

---

## Step 2 — Run the Builder

```bash
cd autodiscovery-results
python3 build_viewer.py
```

Expected output:
```
Viewer written to: /path/to/autodiscovery-results/viewer.html
Experiments: N (M with cards)
```

Open the result:
```bash
open autodiscovery-results/viewer.html
```

---

## Step 3 — Verify Output

After rebuilding, confirm:

1. **Sidebar** populates with PASS and FLAG experiments — if empty, check that triage JSON
   has `passing` and `flagged` arrays.
2. **Experiments with cards** show the hero layout (Gaussian chart + Prior Work / Method /
   Result) — if blank, check that the card markdown has sections `## 5.` and `## 6.`.
3. **Knowledge map tab** shows the contribution type badge and "What the Caveats Affect"
   panel — if missing, check that `knowledge_map` in the literature JSON has
   `contribution_type` and `caveat_impact` fields.
4. **AutoDiscovery links** use the format
   `https://autodiscovery.allen.ai/runs/shared/<run_id>?exp=<id_in_run>`.

---

## What build_viewer.py Does

`autodiscovery-results/build_viewer.py` is the single source of truth for the viewer.
It is a ~1000-line Python script that generates a fully self-contained HTML file with
all data embedded as a JS constant. No external dependencies.

**Python side (lines 1–100):**
- Loads all `*_triage.json` files from `validation/`
- Loads all `*_card.md` files from `experiment-cards/`
- Loads all `*_literature.json` files from `experiment-cards/literature_evidence/`
- Builds `all_experiments` list sorted by verdict (PASS first), then mech score desc
- Serializes everything into a single `DATA` JS constant embedded in the HTML

**JavaScript side (inline in the HTML):**

| Function | What it does |
|---|---|
| `renderSidebar()` | Builds the left-panel experiment list from `DATA.experiments` |
| `selectExp(eid)` | Called on click; triggers `renderCard(eid)` |
| `renderCard(eid)` | Full card render — hero, tabs, sections |
| `gaussianSvg(prior, posterior)` | Inline SVG of Gaussian belief shift (pink=prior, teal=posterior) |
| `dataContextHtml(exp, lit)` | Dataset context strip from `lit.dataset_context` or hypothesis regex |
| `renderPapers(papers, type)` | Renders a paper list with claim, excerpt, and links |
| `renderMd(s)` | Minimal markdown renderer: **bold**, *italic*, `code`, paragraph breaks |
| `firstSentences(text, n)` | Sentence-aware extractor (handles decimals, abbreviations) |
| `extractTakeaway(refl, finding)` | Finds interpretive sentence from reflection for the takeaway strip |
| `switchTab(eid, tabId)` | Tab switching in the literature section |

---

## When to Rebuild

Rebuild any time:
- A new triage JSON is added (`experiment-triage` skill ran on a new run)
- A new literature JSON is added (`experiment-card` skill ran on an experiment)
- A new card markdown is added or updated
- The `build_viewer.py` script itself is modified

The viewer is fully static — it embeds a snapshot of all data at build time. It does not
auto-update when files change.

---

## Modifying the Viewer

All viewer logic lives in `autodiscovery-results/build_viewer.py`. The file is structured
as a Python script that writes one long HTML string.

**Key customization points:**

| What to change | Where in build_viewer.py |
|---|---|
| Color palette (CSS variables) | `--bg`, `--surface*`, `--border*`, `--teal`, `--pink` near top of HTML string |
| Hero layout (slide view) | `.card-hero`, `.hero-left`, `.hero-right`, `.hero-block` CSS; `renderCard()` hero HTML |
| Paper excerpt display | `.paper-excerpt` CSS; `renderPapers()` function |
| Knowledge map layout | `.km-grid`, `.km-card`, contribution type badges CSS; `mapHtml` in `renderCard()` |
| Dataset context strip | `.data-ctx*` CSS; `dataContextHtml()` function |
| Sidebar sort order | `all_experiments.sort(...)` in Python section |
| AutoDiscovery link format | `href="https://autodiscovery.allen.ai/runs/shared/..."` in `renderCard()` eyebrow |
| Takeaway extraction logic | `extractTakeaway()` function |

After any edit to `build_viewer.py`, run `python3 build_viewer.py` and reload the browser.

---

## Adding a New Run

When a new AutoDiscovery run is triaged and its `<runid>_triage.json` is saved:

1. The triage JSON must include top-level fields `run_id`, `run_name`, `species`, `task`,
   and `run_description` — these populate the sidebar and card headers.
2. Run `python3 build_viewer.py` — the new run's experiments will appear in the sidebar.
3. Run `experiment-card` on any passing experiments to populate the card panels.
4. Rebuild viewer again after cards are created.

---

## Behavior Notes

- The viewer is a single `.html` file with no external dependencies — it can be shared,
  emailed, or opened offline.
- All data is embedded at build time. Rebuilding is instant (< 1 second).
- Missing artifacts degrade gracefully — experiments without cards show a placeholder;
  cards without literature show empty Prior Work and Knowledge Map tabs.
- The hero slide view uses sentence-level extraction (`firstSentences`, `extractTakeaway`)
  to keep text concise — it does NOT truncate at character count.
- Markdown in `analysis` and `reflection` fields is rendered (`**bold**`, `*italic*`,
  `` `code` ``, newlines → `<br>`) via the inline `renderMd()` function.
