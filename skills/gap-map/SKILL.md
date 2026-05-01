---
name: gap-map
description: >
  Build an interactive 2D embedding map of literature gaps vs AutoDiscovery hypotheses.
  Use when the user asks to "build the gap map", "show where gaps are", "visualize hypothesis
  coverage", "where are the unexplored gaps", "which hypotheses address known gaps",
  "embedding map", or "gap × hypothesis map". Produces gap_map.html — a self-contained
  interactive Plotly visualization.
argument-hint: [optional: path to build_gap_map.py]
user-invocable: true
---

# Gap Map

Embeds all literature gaps ("Unknown / Contested" items from experiment card knowledge maps)
and all AutoDiscovery hypotheses into a shared semantic space, reduces to 2D with UMAP, and
renders an interactive scatter plot. Shows which hypotheses are addressing known gaps and which
gaps remain uncovered.

---

## What the Map Shows

| Element | Shape | Color | Meaning |
|---|---|---|---|
| Literature gap | Circle (●) | Orange | An "Unknown / Contested" item from a knowledge map |
| Hypothesis · PASS | Filled diamond (◆) | Light→dark blue | Passed AutoDiscovery run; color = mechanistic score (M1–M5) |
| Hypothesis · FLAG | Open diamond (◇) | Light→dark blue | Flagged with caveats; color = mechanistic score |
| KDE contour (orange) | Filled region | Orange tint | Density of literature gaps |
| KDE contour (blue) | Filled region | Blue tint | Density of hypotheses |

**Overlap zone** — where orange and blue KDE contours overlap: hypotheses are directly
targeting known literature gaps.

**Orange-only zone** — gaps with no nearby hypotheses: unexplored territory.

**Blue-only zone** — hypotheses probing areas not yet flagged as gaps in the literature
(either novel territory or the literature evidence for those experiments wasn't retrieved).

**Annotations** — the 7 gap points most isolated from any hypothesis are labelled with
arrow annotations pointing outward from the plot centre.

Hover any point to see the full text. Scroll to zoom, drag to pan.

---

## Step 1 — Verify Artifacts Exist

The script reads from:

| Artifact | Location | Required |
|---|---|---|
| Triage JSON | `autodiscovery-runs/<run_name>/triage.json` | Yes |
| Literature JSONs | `autodiscovery-runs/<run_name>/experiment-cards/literature_evidence/*_literature.json` | Yes — at least one needed for gaps |

```bash
ls autodiscovery-runs/<run_name>/
ls autodiscovery-runs/<run_name>/experiment-cards/literature_evidence/
```

If triage JSON is missing, run the `experiment-triage` skill first.
If no literature JSONs exist, run the `experiment-card` skill on passing experiments first.

---

## Step 2 — Install Dependencies

```bash
pip install sentence-transformers umap-learn plotly scipy
```

All four must be present. `numpy` and `scipy` are usually already installed.

---

## Step 3 — Run the Builder

```bash
cd autodiscovery-runs/<run_name>
python3 build_gap_map.py
```

Expected output:
```
Loaded N hypotheses, M gaps
Loading sentence-transformers model (all-MiniLM-L6-v2)…
Embedding N hypotheses…
Embedding M gaps…
Running UMAP…
Gap map written to: /path/to/autodiscovery-runs/<run_name>/gap_map.html
  M gaps  ·  N hypotheses  ·  UMAP 2D
```

The first run downloads `all-MiniLM-L6-v2` (~90MB) from HuggingFace. Subsequent runs use
the cached model and take ~5–10 seconds.

Open the result:
```bash
open autodiscovery-runs/<run_name>/gap_map.html
```

---

## Step 4 — Verify Output

After building, confirm:

1. **Gap circles** appear in orange — count should match the total "Unknown / Contested"
   items across all literature JSONs.
2. **Hypothesis diamonds** appear in blue shades — filled = PASS, open = FLAG.
3. **Colorbar** (right edge) shows M1–M5 from light to dark blue.
4. **KDE contours** are visible as faint tinted regions.
5. **Annotations** on 7 isolated gap points — arrows should point outward, text wrapped
   to ~50 chars per line.
6. Hovering any point shows full text.

---

## What build_gap_map.py Does

`autodiscovery-runs/<run_name>/build_gap_map.py` runs in 5 stages:

| Stage | What |
|---|---|
| 1. Load | Reads triage JSON (hypotheses + metadata) and all literature JSONs (gaps from `knowledge_map.unknown`) |
| 2. Embed | Encodes all texts with `all-MiniLM-L6-v2` (384-dim cosine-normalised vectors) |
| 3. UMAP | Reduces joint embedding to 2D (`n_neighbors=12`, `min_dist=0.15`, cosine metric, `random_state=42`) |
| 4. Render | Builds Plotly figure: KDE contours, gap circles, PASS/FLAG diamond traces with shared Blues coloraxis |
| 5. Annotate | Finds 7 gap points most isolated from hypotheses; draws outward arrows with wrapped text |

**Tuning UMAP:**

| Parameter | Effect | Default |
|---|---|---|
| `n_neighbors` | Higher = more global structure | 12 |
| `min_dist` | Higher = more spread out | 0.15 |
| `random_state` | Fix for reproducibility | 42 |

**Changing the number of annotations:** edit `[-7:]` in the `top_isolated` line.

**Adding a new run:** add the new triage JSON path to the load section and rebuild.

---

## When to Rebuild

Rebuild when:
- New literature JSONs are added (`experiment-card` skill ran on more experiments)
- A new triage run is added
- UMAP parameters are tuned