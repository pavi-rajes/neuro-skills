"""
Generate a self-contained HTML viewer for experiment cards.
Run: python3 build_viewer.py
Opens: autodiscovery-results/viewer.html
"""
import json, glob, os, re
from pathlib import Path

BASE = Path(__file__).parent
CARDS_DIR = BASE / "experiment-cards"
LIT_DIR = CARDS_DIR / "literature_evidence"
TRIAGE_DIR = BASE / "validation"

# ── load data ─────────────────────────────────────────────────────────────────

def load_triage():
    files = sorted(TRIAGE_DIR.glob("*_triage.json"))
    runs = []
    for f in files:
        runs.append(json.loads(f.read_text()))
    return runs

def load_cards():
    cards = {}
    for md_path in sorted(CARDS_DIR.glob("*_card.md")):
        eid = md_path.stem.replace("_card", "")
        cards[eid] = md_path.read_text()
    return cards

def extract_card_notes(cards):
    """Parse timestamped note entries from ## 7. Notes section of each card."""
    note_re = re.compile(r"<!-- note ([\d\-T:\.Z]+) -->\n([\s\S]*?)(?=\n<!-- note |\Z)")
    notes = {}
    for eid, md in cards.items():
        m = re.search(r"\n## 7\. Notes\n\n([\s\S]*?)$", md)
        if not m:
            continue
        section = m.group(1)
        entries = [{"ts": e.group(1), "text": e.group(2).rstrip()}
                   for e in note_re.finditer(section)]
        if entries:
            notes[eid] = entries
    return notes

def load_literature():
    lit = {}
    for j in sorted(LIT_DIR.glob("*_literature.json")):
        eid = j.stem.replace("_literature", "")
        lit[eid] = json.loads(j.read_text())
    return lit

def load_notes():
    notes_file = BASE / "notes.json"
    if notes_file.exists():
        return json.loads(notes_file.read_text())
    return {}

def load_favorites():
    fav_file = BASE / "favorites.json"
    if fav_file.exists():
        return json.loads(fav_file.read_text())
    return []

runs = load_triage()
cards = load_cards()
literature = load_literature()
# notes: dict of eid -> list of {ts, text} entries
_file_notes = load_notes()  # flat text notes from notes.json (legacy)
_card_notes = extract_card_notes(cards)   # structured entries from card files
# Merge: card entries take precedence; wrap legacy flat text as single entry
notes = {}
for eid in set(list(_file_notes.keys()) + list(_card_notes.keys())):
    if eid in _card_notes:
        notes[eid] = _card_notes[eid]
    elif _file_notes.get(eid):
        notes[eid] = [{"ts": "", "text": _file_notes[eid]}]

# ── build sidebar experiment list across all runs ─────────────────────────────

all_experiments = []
for run in runs:
    run_desc = run.get("run_description", "")
    run_species = run.get("species", "")
    run_task = run.get("task", "")
    for exp in run["passing"]:
        eid = exp["experiment_id"]
        all_experiments.append({
            "experiment_id": eid,
            "id_in_run": exp["id_in_run"],
            "hypothesis": exp["hypothesis"],
            "mechanistic_score": exp.get("mechanistic_score", 0),
            "novelty_tier": literature.get(eid, {}).get("novelty_tier"),
            "verdict": "PASS",
            "surprise": exp.get("surprise", 0),
            "prior": exp.get("prior", 0),
            "posterior": exp.get("posterior", 0),
            "flags": exp.get("flags", []),
            "n_subjects": exp.get("n_subjects"),
            "run_id": run["run_id"],
            "run_name": run.get("run_name", run["run_id"][:8]),
            "run_description": run_desc,
            "species": run_species,
            "task": run_task,
            "has_card": eid in cards,
        })
    for exp in run["flagged"]:
        eid = exp["experiment_id"]
        all_experiments.append({
            "experiment_id": eid,
            "id_in_run": exp["id_in_run"],
            "hypothesis": exp["hypothesis"],
            "mechanistic_score": exp.get("mechanistic_score", 0),
            "novelty_tier": literature.get(eid, {}).get("novelty_tier"),
            "verdict": "FLAG",
            "surprise": exp.get("surprise", 0),
            "prior": exp.get("prior", 0),
            "posterior": exp.get("posterior", 0),
            "flags": exp.get("flags", []),
            "n_subjects": exp.get("n_subjects"),
            "run_id": run["run_id"],
            "run_name": run.get("run_name", run["run_id"][:8]),
            "run_description": run_desc,
            "species": run_species,
            "task": run_task,
            "has_card": eid in cards,
        })

# Sort: PASS first, then by mech score desc
all_experiments.sort(key=lambda e: (0 if e["verdict"] == "PASS" else 1, -e["mechanistic_score"], e["surprise"]))

data_js = json.dumps({
    "runs": runs,
    "experiments": all_experiments,
    "cards": cards,
    "literature": literature,
    "notes": notes,
    "favorites": load_favorites(),
}, ensure_ascii=False)

# ── HTML ──────────────────────────────────────────────────────────────────────

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Experiment Card Viewer — AIND × Ai2</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  :root {
    /* Asta dark teal-green base */
    --bg: #05110E;
    --surface: #0A1C18;
    --surface2: #0E2520;
    --surface3: #122C26;
    --border: #1A3830;
    --border-light: #24503F;
    /* text */
    --text: #e4f5ef;
    --text-muted: #5fa888;
    --text-dim: #2e6650;
    /* Ai2 pink — primary accent */
    --pink: #f0529c;
    --pink-dim: #3d1428;
    --pink-mid: #7a2050;
    /* AIND teal — secondary accent */
    --teal: #0fb8a8;
    --teal-dim: #042e28;
    --teal-mid: #086b5e;
    /* Status */
    --pass: #0fb8a8;
    --pass-dim: #041e1b;
    --flag: #f5a623;
    --flag-dim: #2e1e04;
    --fail: #f05252;
    /* Mech score */
    --mech5: #f0529c;
    --mech4: #0fb8a8;
    --mech3: #60a5fa;
    /* Novelty tier */
    --tier1: #f0529c;
    --tier2: #fb923c;
    --tier3: #a3e635;
    --tier4: #5fa888;
    /* Evidence types */
    --sup: #0fb8a8;
    --opp: #f05252;
    --ctx: #60a5fa;
    /* Header gradient */
    --grad: linear-gradient(90deg, #f0529c 0%, #7b3fa8 50%, #0fb8a8 100%);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 14px;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  /* ── header ── */
  .header-accent { height: 3px; background: var(--grad); flex-shrink: 0; }
  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 11px 20px;
    display: flex; align-items: center; gap: 16px; flex-shrink: 0;
  }
  .header-logo { display: flex; flex-direction: column; gap: 0px; }
  .header-logo-primary { font-size: 15px; font-weight: 700; letter-spacing: -0.01em; color: var(--text); }
  .header-logo-primary span { color: var(--pink); }
  .header-logo-sub { font-size: 10px; font-weight: 500; color: var(--text-muted); letter-spacing: 0.06em; text-transform: uppercase; }
  .header-divider { width: 1px; height: 28px; background: var(--border); }
  .stat { display: flex; gap: 6px; align-items: center; font-size: 12px; }
  .stat-pass { color: var(--pass); font-weight: 600; }
  .stat-flag { color: var(--flag); font-weight: 600; }
  .stat-fail { color: var(--fail); }
  header .spacer { flex: 1; }
  .filter-row { display: flex; gap: 8px; align-items: center; }
  .filter-row select, .filter-row input {
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); border-radius: 8px; padding: 5px 10px; font-size: 12px;
    font-family: inherit; outline: none; transition: border-color 0.15s;
  }
  .filter-row select:focus, .filter-row input:focus { border-color: var(--pink); }
  .filter-row input::placeholder { color: var(--text-dim); }

  /* ── layout ── */
  .layout { display: flex; flex: 1; overflow: hidden; }

  /* ── sidebar ── */
  aside {
    width: 300px; flex-shrink: 0;
    border-right: 1px solid var(--border);
    display: flex; flex-direction: column; overflow: hidden;
    background: var(--surface);
  }
  .sidebar-scroll { flex: 1; overflow-y: auto; padding: 8px 6px; }
  .exp-item {
    border-radius: 10px; padding: 10px 12px; cursor: pointer;
    border: 1px solid transparent; margin-bottom: 3px; transition: all 0.12s;
  }
  .exp-item:hover { background: var(--surface2); border-color: var(--border); }
  .exp-item.active { background: var(--surface2); border-color: var(--pink-mid); box-shadow: 0 0 0 1px var(--pink-mid); }
  .exp-item.no-card { opacity: 0.45; }
  .exp-item-top { display: flex; align-items: center; gap: 5px; margin-bottom: 5px; }
  .verdict-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
  .verdict-dot.PASS { background: var(--pass); box-shadow: 0 0 4px var(--pass); }
  .verdict-dot.FLAG { background: var(--flag); box-shadow: 0 0 4px var(--flag); }
  .exp-num { font-size: 10px; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }
  .exp-id { font-size: 10px; color: var(--teal); font-family: 'JetBrains Mono', monospace; flex: 1; }
  .badge {
    font-size: 10px; border-radius: 5px; padding: 1px 6px;
    font-weight: 600; font-family: 'JetBrains Mono', monospace;
  }
  .badge.m5 { background: var(--pink-dim); color: var(--pink); border: 1px solid var(--pink-mid); }
  .badge.m4 { background: var(--teal-dim); color: var(--teal); border: 1px solid var(--teal-mid); }
  .badge.m3 { background: #0a1e30; color: #60a5fa; border: 1px solid #1a3a5c; }
  .badge.t1 { background: var(--pink-dim); color: var(--pink); }
  .badge.t2 { background: #2e1a06; color: #fb923c; }
  .badge.t3 { background: #152206; color: #a3e635; }
  .badge.t4 { background: #141e26; color: var(--text-dim); }
  .exp-hyp {
    font-size: 11.5px; color: var(--text-muted); line-height: 1.45;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  }
  .sidebar-section {
    font-size: 10px; font-weight: 700; color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 10px 12px 4px; display: flex; align-items: center; gap: 8px;
  }
  .sidebar-section::after { content: ''; flex: 1; height: 1px; background: var(--border); }

  /* ── main ── */
  main { flex: 1; overflow-y: auto; padding: 28px 40px; max-width: 900px; }
  .empty-state {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; height: 100%; color: var(--text-dim); gap: 14px;
  }
  .empty-state svg { opacity: 0.2; }
  .empty-state p { font-size: 13px; }

  /* ── card header ── */
  .card-header { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
  .card-eyebrow { font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--pink); margin-bottom: 6px; font-family: 'JetBrains Mono', monospace; }
  .card-title { font-size: 20px; font-weight: 700; margin-bottom: 14px; letter-spacing: -0.02em; line-height: 1.3; }
  .card-meta { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 14px; }
  .meta-pill {
    display: flex; align-items: center; gap: 5px;
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 20px; padding: 4px 12px; font-size: 11.5px;
  }
  .meta-pill .label { color: var(--text-dim); }
  .belief-row { display: flex; align-items: center; gap: 10px; font-size: 12px; color: var(--text-muted); }
  .belief-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; }
  .bar-track { height: 5px; width: 100px; background: var(--surface3); border-radius: 3px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 3px; transition: width 0.4s; }
  .surprise-val { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-dim); }

  /* ── sections ── */
  .section { margin-bottom: 34px; }
  .section-title {
    font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--text-dim); margin-bottom: 14px;
    display: flex; align-items: center; gap: 10px;
  }
  .section-title .sec-num {
    color: var(--pink); font-family: 'JetBrains Mono', monospace; font-size: 11px;
  }
  .section-title::after { content: ''; flex: 1; height: 1px; background: var(--border); }
  .hypothesis-text {
    font-size: 14.5px; line-height: 1.75; color: var(--text);
    background: var(--surface2); border-left: 3px solid var(--pink);
    border-radius: 0 10px 10px 0; padding: 16px 20px;
    font-weight: 400;
  }
  .limitations {
    margin-top: 10px; font-size: 12px; color: var(--flag);
    background: var(--flag-dim); border: 1px solid #4a3000;
    border-radius: 8px; padding: 9px 14px;
    display: flex; align-items: flex-start; gap: 8px;
  }

  /* ── tabs ── */
  .tabs { display: flex; gap: 2px; margin-bottom: 0; border-bottom: 1px solid var(--border); padding-bottom: 0; }
  .tab {
    padding: 8px 16px; font-size: 12px; font-weight: 500; cursor: pointer;
    border-radius: 8px 8px 0 0; color: var(--text-muted);
    border: 1px solid transparent; border-bottom: none; transition: all 0.12s;
    position: relative; bottom: -1px;
  }
  .tab:hover { color: var(--text); background: var(--surface2); }
  .tab.active {
    color: var(--text); background: var(--surface2);
    border-color: var(--border); border-bottom-color: var(--surface2);
  }
  .tab.active::after {
    content: ''; position: absolute; bottom: -1px; left: 0; right: 0;
    height: 2px; background: var(--pink); border-radius: 2px 2px 0 0;
  }
  .tab-badge {
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 16px; height: 16px; border-radius: 8px;
    font-size: 10px; font-weight: 700; margin-left: 5px; padding: 0 4px;
    font-family: 'JetBrains Mono', monospace;
  }
  .tab-badge.sup { background: var(--pass-dim); color: var(--sup); }
  .tab-badge.opp { background: #2e0a0a; color: var(--opp); }
  .tab-badge.ctx { background: #0a1e30; color: var(--ctx); }
  .tabs-body { background: var(--surface2); border: 1px solid var(--border); border-top: none; border-radius: 0 0 10px 10px; padding: 16px; }
  .tab-content { display: none; } .tab-content.active { display: block; }

  /* ── paper cards ── */
  .paper-list { display: flex; flex-direction: column; gap: 8px; }
  .paper-card {
    background: var(--surface3); border: 1px solid var(--border);
    border-radius: 8px; padding: 12px 14px; transition: border-color 0.12s;
  }
  .paper-card:hover { border-color: var(--border-light); }
  .paper-top { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 5px; }
  .paper-type { flex-shrink: 0; width: 7px; height: 7px; border-radius: 50%; margin-top: 5px; }
  .paper-type.sup { background: var(--sup); box-shadow: 0 0 4px var(--sup); }
  .paper-type.opp { background: var(--opp); box-shadow: 0 0 4px var(--opp); }
  .paper-type.ctx { background: var(--ctx); box-shadow: 0 0 4px var(--ctx); }
  .paper-title { font-size: 13px; font-weight: 600; line-height: 1.4; flex: 1; color: var(--text); }
  .paper-meta { font-size: 11px; color: var(--text-dim); margin-bottom: 7px; font-family: 'JetBrains Mono', monospace; }
  .paper-claim {
    font-size: 12px; color: var(--text-muted); line-height: 1.55;
    border-left: 2px solid var(--border-light); padding-left: 10px;
    margin-bottom: 7px;
  }
  .paper-excerpt {
    font-size: 11.5px; color: var(--text-dim); line-height: 1.6;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 5px; padding: 8px 11px; margin-top: 7px;
    font-style: italic; position: relative;
  }
  .paper-excerpt::before {
    content: '"'; position: absolute; top: 4px; left: 7px;
    font-size: 18px; color: var(--teal); opacity: 0.4; font-style: normal; line-height: 1;
  }
  .paper-excerpt-text { padding-left: 10px; }
  .paper-excerpt-src {
    font-size: 10px; color: var(--text-dim); margin-top: 4px; padding-left: 10px;
    font-style: normal; font-family: 'JetBrains Mono', monospace;
  }
  .paper-link {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 11px; color: var(--teal); text-decoration: none;
    font-family: 'JetBrains Mono', monospace;
  }
  .paper-link:hover { text-decoration: underline; }
  .score-pill {
    font-size: 10px; background: var(--surface); border: 1px solid var(--border);
    border-radius: 4px; padding: 1px 6px; color: var(--text-dim);
    flex-shrink: 0; font-family: 'JetBrains Mono', monospace;
  }
  .empty-papers { color: var(--text-dim); font-size: 13px; font-style: italic; padding: 8px 0; }

  /* ── knowledge map ── */
  .km-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 4px; }
  .km-card { background: var(--surface3); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
  .km-card.full { grid-column: 1 / -1; border-left: 3px solid var(--pink); border-radius: 0 10px 10px 0; }
  .km-card.caveat { grid-column: 1 / -1; border-left: 3px solid var(--flag); border-radius: 0 10px 10px 0; }
  .km-title { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
  .km-title.known { color: var(--pass); }
  .km-title.unknown { color: var(--flag); }
  .km-title.sheds { color: var(--pink); }
  .km-title.caveat-title { color: var(--flag); }
  .km-list { list-style: none; display: flex; flex-direction: column; gap: 7px; }
  .km-list li { font-size: 12px; line-height: 1.5; color: var(--text-muted); padding-left: 14px; position: relative; }
  .km-list li::before { content: '—'; position: absolute; left: 0; color: var(--text-dim); }
  .km-sheds { font-size: 13px; line-height: 1.7; color: var(--text); }
  .contribution-type { display: inline-flex; align-items: center; gap: 8px; margin-bottom: 12px; }
  .ct-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-dim); }
  .ct-badge-resolution { background: #0c2e1a; border: 1px solid var(--pass); color: var(--pass); border-radius: 5px; padding: 2px 9px; font-size: 11px; font-weight: 700; }
  .ct-badge-constraint { background: #2a1e08; border: 1px solid var(--flag); color: var(--flag); border-radius: 5px; padding: 2px 9px; font-size: 11px; font-weight: 700; }
  .ct-badge-replication { background: #12213a; border: 1px solid #4a8fc7; color: #4a8fc7; border-radius: 5px; padding: 2px 9px; font-size: 11px; font-weight: 700; }
  .ct-badge-negative { background: #2a0e1a; border: 1px solid var(--pink); color: var(--pink); border-radius: 5px; padding: 2px 9px; font-size: 11px; font-weight: 700; }
  .ct-badge-unknown { background: var(--surface); border: 1px solid var(--border); color: var(--text-dim); border-radius: 5px; padding: 2px 9px; font-size: 11px; font-weight: 700; }

  /* ── plan section ── */
  .plan-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
  .plan-block { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
  .plan-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--teal); margin-bottom: 8px; }
  .plan-text { font-size: 12.5px; line-height: 1.65; color: var(--text); white-space: pre-wrap; }

  /* ── dataset context strip ── */
  .data-ctx {
    display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
    padding: 9px 14px; background: var(--surface2);
    border: 1px solid var(--border); border-radius: 8px;
    margin-bottom: 20px;
  }
  .data-ctx-item {
    display: flex; align-items: center; gap: 5px;
    font-size: 11.5px; color: var(--text-muted);
  }
  .data-ctx-item .dc-label {
    font-size: 9.5px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: var(--text-dim);
  }
  .data-ctx-item .dc-val { color: var(--text); }
  .data-ctx-item .dc-val.regions span {
    display: inline-block; background: var(--surface3); border: 1px solid var(--border);
    border-radius: 4px; padding: 1px 6px; font-size: 10.5px;
    font-family: 'JetBrains Mono', monospace; color: var(--teal);
    margin-right: 3px;
  }
  .data-ctx-sep { width: 1px; height: 16px; background: var(--border); }

  /* ── hero two-column ── */
  .card-hero {
    display: grid; grid-template-columns: 320px 1fr; gap: 0;
    border: 1px solid var(--border); border-radius: 12px; overflow: visible;
    margin-bottom: 28px;
  }
  .hero-left {
    background: var(--surface); border-right: 1px solid var(--border);
    padding: 18px 18px 16px;
    display: flex; flex-direction: column; gap: 12px;
    border-radius: 12px 0 0 12px;
  }
  .hero-right {
    background: var(--surface2);
    display: flex; flex-direction: column;
    border-radius: 0 12px 12px 0;
    overflow: hidden;
  }
  .hero-block {
    padding: 14px 18px; border-bottom: 1px solid var(--border);
    flex: none;
  }
  .hero-block:last-child { border-bottom: none; }
  .hero-block-title {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--text-dim); margin-bottom: 9px;
    display: flex; align-items: center; gap: 8px;
  }
  .hero-block-title::after { content: ''; flex: 1; height: 1px; background: var(--border); }
  .hero-hyp {
    font-size: 12.5px; line-height: 1.65; color: var(--text);
    border-left: 2px solid var(--pink); padding-left: 10px;
  }
  .hero-belief-label {
    font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;
  }
  .hero-belief-label span { color: var(--pink); }
  .prior-work-list { display: flex; flex-direction: column; gap: 7px; }
  .prior-work-item { font-size: 12px; line-height: 1.5; display: flex; gap: 8px; flex-direction: column; }
  .prior-work-item-header { display: flex; align-items: baseline; gap: 6px; }
  .prior-work-item-header::before { content: '•'; color: var(--teal); flex-shrink: 0; }
  .prior-work-item a { color: var(--teal); text-decoration: none; font-weight: 600; }
  .prior-work-item a:hover { text-decoration: underline; }
  .prior-work-claim { color: var(--text-muted); font-size: 11.5px; padding-left: 14px; line-height: 1.5; }
  .prior-work-no-claim { color: var(--text-dim); font-size: 11px; padding-left: 14px; font-style: italic; }
  .hero-method { font-size: 12.5px; line-height: 1.65; color: var(--text-muted); }
  .hero-result {
    font-size: 12.5px; line-height: 1.65; color: var(--text);
    background: var(--surface3); border-radius: 6px; padding: 10px 12px;
    border-left: 2px solid var(--teal);
  }
  .takeaway {
    font-size: 13.5px; line-height: 1.7; color: var(--text); text-align: center;
    padding: 14px 24px; background: var(--surface);
    border: 1px solid var(--border); border-top: 2px solid var(--teal);
    border-radius: 0 0 12px 12px; margin-top: -1px; margin-bottom: 28px;
    font-style: italic;
  }

  /* ── reflection ── */
  .reflection-box {
    background: var(--surface2); border: 1px solid var(--border);
    border-left: 3px solid var(--pink); border-radius: 0 10px 10px 0;
    padding: 18px 20px; font-size: 13px; line-height: 1.75; color: var(--text);
  }

  /* ── results ── */
  .results-box {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: 16px 18px; font-size: 13px;
    line-height: 1.65; color: var(--text);
  }

  /* ── no-card placeholder ── */
  .no-card-msg {
    background: var(--surface2); border: 1px dashed var(--border);
    border-radius: 10px; padding: 40px; text-align: center;
    color: var(--text-dim); font-size: 13px; line-height: 1.6;
  }
  .no-card-msg code { color: var(--teal); font-family: 'JetBrains Mono', monospace; }

  /* ── md content ── */
  .md-content { line-height: 1.7; }
  .md-content h3 { font-size: 13px; color: var(--teal); margin: 12px 0 6px; }
  .md-content p { font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }
  .md-content strong { color: var(--text); }
  .md-content code { background: var(--surface3); border-radius: 4px; padding: 1px 5px; font-size: 11.5px; font-family: 'JetBrains Mono', monospace; color: var(--teal); }

  /* ── scrollbar ── */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 2px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }

  /* ── legend dropdown ── */
  .legend-btn {
    background: var(--surface2); border: 1px solid var(--border); color: var(--text-muted);
    border-radius: 8px; padding: 5px 12px; font-size: 12px; cursor: pointer;
    font-family: inherit; transition: border-color 0.12s, color 0.12s; white-space: nowrap;
  }
  .legend-btn:hover, .legend-btn.open { border-color: var(--teal); color: var(--teal); }
  .legend-anchor { position: relative; }
  .legend-panel {
    display: none; position: absolute; top: calc(100% + 6px); right: 0;
    background: var(--surface); border: 1px solid var(--border-light);
    border-radius: 10px; padding: 14px 18px; z-index: 200;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    min-width: 520px; display: none; flex-direction: column; gap: 10px;
  }
  .legend-panel.open { display: flex; }
  .legend-group { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
  .legend-label { color: var(--text-dim); font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; font-size: 10px; min-width: 80px; flex-shrink: 0; }
  .legend-item { display: flex; align-items: center; gap: 4px; cursor: default; white-space: nowrap; }
  .legend-item span { font-family: 'JetBrains Mono', monospace; }
  .legend-desc { color: var(--text-dim); font-size: 10px; }
  .legend-sep { height: 1px; background: var(--border); margin: 2px 0; }

  /* ── favorites ── */
  .fav-btn {
    background: none; border: none; cursor: pointer; padding: 0;
    font-size: 14px; line-height: 1; color: var(--text-dim);
    transition: color 0.1s, transform 0.1s; flex-shrink: 0;
  }
  .fav-btn:hover { color: var(--flag); transform: scale(1.2); }
  .fav-btn.on { color: var(--flag); }
  .fav-btn-header {
    background: none; border: none; cursor: pointer;
    font-size: 18px; line-height: 1; color: var(--text-dim);
    transition: color 0.1s, transform 0.1s; padding: 0 4px; vertical-align: middle;
  }
  .fav-btn-header:hover { color: var(--flag); transform: scale(1.15); }
  .fav-btn-header.on { color: var(--flag); }

  /* ── claim source badges ── */
  .claim-src {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 10px; font-family: 'JetBrains Mono', monospace;
    border-radius: 4px; padding: 1px 7px; margin-bottom: 5px; font-weight: 500;
  }
  .claim-src.snippet  { background: #061a0f; border: 1px solid #1a5c2a; color: #4ade80; }
  .claim-src.abstract { background: #071824; border: 1px solid #1a4060; color: #60a5fa; }
  .claim-src.ai-summary { background: #2a1e08; border: 1px solid #60400a; color: #fb923c; }
  .claim-src.unavailable { background: #1e0a0a; border: 1px solid #4a1010; color: #f87171; }
  .claim-src.unknown  { background: var(--surface); border: 1px solid var(--border); color: var(--text-dim); }

  /* ── notes ── */
  .notes-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }
  .note-entry {
    background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 11px 14px;
  }
  .note-ts {
    font-size: 10px; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;
    margin-bottom: 5px;
  }
  .note-text { font-size: 13px; line-height: 1.65; color: var(--text); white-space: pre-wrap; }
  .notes-input-row { display: flex; flex-direction: column; gap: 8px; }
  .notes-area {
    width: 100%; background: var(--surface2); border: 1px solid var(--border);
    border-radius: 10px; padding: 12px 14px; color: var(--text);
    font-family: 'Inter', sans-serif; font-size: 13px; line-height: 1.65;
    min-height: 72px; resize: vertical; outline: none; transition: border-color 0.15s;
  }
  .notes-area:focus { border-color: var(--pink-mid); }
  .notes-submit-row { display: flex; align-items: center; gap: 10px; }
  .notes-submit-btn {
    background: var(--pink-dim); border: 1px solid var(--pink-mid); color: var(--pink);
    border-radius: 8px; padding: 6px 16px; font-size: 12px; font-weight: 600;
    cursor: pointer; font-family: inherit; transition: background 0.12s;
  }
  .notes-submit-btn:hover { background: var(--pink-mid); }
  .notes-submit-btn:disabled { opacity: 0.4; cursor: default; }
  .notes-status { font-size: 11px; color: var(--teal); height: 14px; }
  .export-notes-btn {
    background: var(--surface2); border: 1px solid var(--border); color: var(--text-muted);
    border-radius: 8px; padding: 5px 12px; font-size: 12px; cursor: pointer;
    font-family: inherit; transition: border-color 0.12s, color 0.12s;
  }
  .export-notes-btn:hover { border-color: var(--teal); color: var(--teal); }
  .claude-btn {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace;
    color: var(--pink); background: var(--pink-dim); border: 1px solid var(--pink-mid);
    border-radius: 5px; padding: 3px 9px; cursor: pointer; transition: background 0.12s, border-color 0.12s;
  }
  .claude-btn:hover { background: #4d1830; border-color: var(--pink); }
</style>
</head>
<body>

<div class="header-accent"></div>
<header>
  <div class="header-logo">
    <div class="header-logo-primary">Experiment<span>Cards</span></div>
    <div class="header-logo-sub">AIND · Ai2 · AutoDiscovery</div>
  </div>
  <div class="header-divider"></div>
  <div class="spacer"></div>
  <div class="filter-row">
    <button class="export-notes-btn" onclick="exportNotes()" title="Download notes.json">Export notes</button>
  </div>
  <div class="header-divider"></div>
  <div class="filter-row">
    <select id="filter-verdict" onchange="renderSidebar()">
      <option value="all">All verdicts</option>
      <option value="PASS">PASS only</option>
      <option value="FLAG">FLAG only</option>
    </select>
    <select id="filter-card" onchange="renderSidebar()">
      <option value="all">All experiments</option>
      <option value="card">Has card</option>
      <option value="favorites">★ Favorites</option>
    </select>
    <input id="filter-search" type="text" placeholder="Search hypothesis…" oninput="renderSidebar()">
    <div class="legend-anchor">
      <button class="legend-btn" id="legend-btn" onclick="toggleLegend(event)">Legend ▾</button>
      <div class="legend-panel" id="legend-panel">
        <div class="legend-group">
          <span class="legend-label">Verdict</span>
          <div class="legend-item"><span style="color:var(--pass)">● PASS</span><span class="legend-desc">ran successfully, clear result</span></div>
          <div class="legend-item"><span style="color:var(--flag)">● FLAG</span><span class="legend-desc">ambiguous result, small N, or methodological concerns</span></div>
        </div>
        <div class="legend-sep"></div>
        <div class="legend-group">
          <span class="legend-label">Mech</span>
          <div class="legend-item"><span class="badge m5">M5</span><span class="legend-desc">direct causal test — manipulates and measures the mechanism</span></div>
          <div class="legend-item"><span class="badge m4">M4</span><span class="legend-desc">strong correlational evidence with controls</span></div>
          <div class="legend-item"><span class="badge m3">M3</span><span class="legend-desc">observational evidence consistent with mechanism</span></div>
        </div>
        <div class="legend-sep"></div>
        <div class="legend-group">
          <span class="legend-label">Novelty</span>
          <div class="legend-item"><span class="badge t1">T1</span><span class="legend-desc">fills an explicitly flagged gap (review paper said "not yet tested")</span></div>
          <div class="legend-item"><span class="badge t2">T2</span><span class="legend-desc">predicted but unmeasured in this circuit/task/species</span></div>
          <div class="legend-item"><span class="badge t3">T3</span><span class="legend-desc">validates existing framework in a new context</span></div>
          <div class="legend-item"><span class="badge t4">T4</span><span class="legend-desc">positive control — known finding re-observed</span></div>
        </div>
        <div class="legend-sep"></div>
        <div class="legend-group">
          <span class="legend-label">Contribution</span>
          <div class="legend-item"><span class="ct-badge-resolution">Resolution</span><span class="legend-desc">closes the gap — same circuit, task, adequate N</span></div>
          <div class="legend-item"><span class="ct-badge-constraint">Constraint</span><span class="legend-desc">narrows the gap — borderline N or residual confounds remain</span></div>
          <div class="legend-item"><span class="ct-badge-replication">Replication</span><span class="legend-desc">confirms known finding in a new context</span></div>
          <div class="legend-item"><span class="ct-badge-negative">Negative</span><span class="legend-desc">null result rules out a specific model prediction</span></div>
        </div>
      </div>
    </div>
  </div>
</header>

<div class="layout">
  <aside>
    <div class="sidebar-scroll" id="sidebar"></div>
  </aside>
  <main id="main">
    <div class="empty-state">
      <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
        <path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18"/>
      </svg>
      <p>Select an experiment from the sidebar</p>
    </div>
  </main>
</div>

<script>
const DATA = """ + data_js + r""";

let activeId = null;
let activeTab = {};

function mechColor(s) { return s >= 5 ? 'm5' : s >= 4 ? 'm4' : 'm3'; }
function tierColor(t) { return t ? 't' + t : ''; }
function verdictColor(v) { return v === 'PASS' ? 'var(--pass)' : 'var(--flag)'; }
function escHtml(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

// Minimal markdown renderer: bold, italic, inline code, and paragraph breaks
function renderMd(s) {
  if (!s) return '';
  return escHtml(s)
    // Bold **text** or __text__
    .replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
    .replace(/__([^_\n]+)__/g, '<strong>$1</strong>')
    // Italic *text* or _text_ (not inside words)
    .replace(/\*([^*\n]+)\*/g, '<em>$1</em>')
    .replace(/(?<!\w)_([^_\n]+)_(?!\w)/g, '<em>$1</em>')
    // Inline code `text`
    .replace(/`([^`\n]+)`/g, '<code style="font-family:JetBrains Mono,monospace;font-size:0.9em;background:var(--surface3);padding:1px 5px;border-radius:3px">$1</code>')
    // Paragraph breaks (double newline → <br><br>)
    .replace(/\n\n+/g, '<br><br>')
    // Single newline → <br>
    .replace(/\n/g, '<br>');
}

const KNOWN_REGIONS = ['VIS','AUD','MOs','ACA','PFC','ORB','CA1','SC','LP','DG','HPC','RSP','MOp','SSp','TEa','ECT','SUB'];

function extractRegions(text) {
  const found = new Set();
  KNOWN_REGIONS.forEach(r => {
    if (new RegExp('\\b' + r + '\\b').test(text)) found.add(r);
  });
  return [...found];
}

function dataContextHtml(exp, lit) {
  const dc = lit && lit.dataset_context;
  const items = [];

  // Sessions — from literature JSON if available
  if (dc && dc.sessions && dc.sessions.length) {
    const sessStr = dc.sessions.join(', ') + (dc.n_subjects ? ` (${dc.n_subjects} subjects)` : '');
    items.push(`<div class="data-ctx-item"><span class="dc-label">Sessions</span><span class="dc-val">${escHtml(sessStr)}</span></div>`);
  } else if (exp.n_subjects != null) {
    items.push(`<div class="data-ctx-item"><span class="dc-label">Sessions</span><span class="dc-val">${exp.n_subjects} subjects</span></div>`);
  }

  // Task — from lit JSON, else from run-level task
  const task = (dc && dc.task) || exp.task || '';
  if (task) {
    if (items.length) items.push(`<div class="data-ctx-sep"></div>`);
    items.push(`<div class="data-ctx-item"><span class="dc-label">Task</span><span class="dc-val">${escHtml(task)}</span></div>`);
  }

  // Regions — from lit JSON (richer), else extract from hypothesis
  const regionChips = (regions) => regions.map(r => `<span>${r}</span>`).join('');
  if (dc && dc.regions && Object.keys(dc.regions).length) {
    const chips = Object.entries(dc.regions).map(([r, units]) =>
      `<span title="${escHtml(units)}">${r}</span>`).join('');
    if (items.length) items.push(`<div class="data-ctx-sep"></div>`);
    items.push(`<div class="data-ctx-item"><span class="dc-label">Regions</span><span class="dc-val regions">${chips}</span></div>`);
  } else {
    const regions = extractRegions(exp.hypothesis);
    if (regions.length) {
      if (items.length) items.push(`<div class="data-ctx-sep"></div>`);
      items.push(`<div class="data-ctx-item"><span class="dc-label">Regions</span><span class="dc-val regions">${regionChips(regions)}</span></div>`);
    }
  }

  return items.length ? `<div class="data-ctx">${items.join('')}</div>` : '';
}

function gaussianSvg(prior, posterior) {
  const W = 284, H = 160, pl = 16, pr = 16, pt = 32, pb = 26;
  const pw = W - pl - pr, ph = H - pt - pb;
  const sigma = 0.13;
  const gauss = (x, mu) => Math.exp(-0.5 * ((x - mu) / sigma) ** 2);
  const N = 200;
  const xs = Array.from({length: N}, (_, i) => i / (N - 1));
  const tx = x => (pl + x * pw).toFixed(1);
  const ty = y => (pt + ph - y * ph).toFixed(1);
  const polyline = (mu, color) => {
    const pts = xs.map(x => `${tx(x)},${ty(gauss(x, mu))}`).join(' ');
    return `<polyline points="${pts}" fill="none" stroke="${color}" stroke-width="2.2" opacity="0.9"/>`;
  };
  const fill = (mu, color) => {
    const pts = xs.map(x => `${tx(x)},${ty(gauss(x, mu))}`).join(' ');
    return `<polygon points="${tx(0)},${ty(0)} ${pts} ${tx(1)},${ty(0)}" fill="${color}" opacity="0.1"/>`;
  };
  const vline = (mu) => `<line x1="${tx(mu)}" y1="${pt}" x2="${tx(mu)}" y2="${pt+ph}" stroke="white" stroke-width="1" stroke-dasharray="3,3" opacity="0.25"/>`;
  const gridLines = [0.25, 0.5, 0.75].map(x =>
    `<line x1="${tx(x)}" y1="${pt}" x2="${tx(x)}" y2="${pt+ph}" stroke="white" stroke-width="0.4" opacity="0.08"/>`
  ).join('');
  const priorX = parseFloat(tx(prior)), postX = parseFloat(tx(posterior));
  const priorIsLeft = prior < posterior;
  const priorAnchor = priorIsLeft ? 'middle' : 'middle';
  const postAnchor = 'middle';
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="width:100%;height:auto;display:block;border-radius:8px">
  <rect width="${W}" height="${H}" fill="var(--surface)" rx="8"/>
  ${gridLines}
  <text x="${pl}" y="${pt-18}" fill="var(--teal)" font-size="9" font-weight="600" font-family="Inter,sans-serif">Belief Shift</text>
  ${fill(prior, '#f0529c')}${fill(posterior, '#0fb8a8')}
  ${polyline(prior, '#f0529c')}${polyline(posterior, '#0fb8a8')}
  ${vline(prior)}${vline(posterior)}
  <text x="${priorX}" y="${pt-8}" text-anchor="middle" fill="#f0529c" font-size="8.5" font-family="Inter,sans-serif">Before  ${prior.toFixed(2)}</text>
  <text x="${postX}" y="${pt-8}" text-anchor="middle" fill="#0fb8a8" font-size="8.5" font-family="Inter,sans-serif">After  ${posterior.toFixed(2)}</text>
  <line x1="${pl}" y1="${pt+ph}" x2="${W-pr}" y2="${pt+ph}" stroke="var(--border-light)" stroke-width="0.5"/>
  <text x="${pl}" y="${H-8}" fill="var(--text-dim)" font-size="8" font-family="Inter,sans-serif">Likely False</text>
  <text x="${W-pr}" y="${H-8}" fill="var(--text-dim)" font-size="8" font-family="Inter,sans-serif" text-anchor="end">Likely True</text>
</svg>`;
}

function renderSidebar() {
  const verdict = document.getElementById('filter-verdict').value;
  const cardFilter = document.getElementById('filter-card').value;
  const search = document.getElementById('filter-search').value.toLowerCase();
  const el = document.getElementById('sidebar');

  let exps = DATA.experiments.filter(e => {
    if (verdict !== 'all' && e.verdict !== verdict) return false;
    if (cardFilter === 'card' && !e.has_card) return false;
    if (cardFilter === 'favorites' && !_favorites.has(e.experiment_id)) return false;
    if (search && !e.hypothesis.toLowerCase().includes(search) && !e.experiment_id.includes(search)) return false;
    return true;
  });

  const byRun = {};
  exps.forEach(e => {
    if (!byRun[e.run_name]) byRun[e.run_name] = [];
    byRun[e.run_name].push(e);
  });

  let html = '';
  for (const [runName, runExps] of Object.entries(byRun)) {
    html += `<div class="sidebar-section">${runName}</div>`;
    runExps.forEach(e => {
      const mc = mechColor(e.mechanistic_score);
      const tc = tierColor(e.novelty_tier);
      const active = e.experiment_id === activeId ? ' active' : '';
      const noCard = e.has_card ? '' : ' no-card';
      const favOn = _favorites.has(e.experiment_id) ? ' on' : '';
      const favStar = _favorites.has(e.experiment_id) ? '★' : '☆';
      html += `<div class="exp-item${active}${noCard}" onclick="selectExp('${e.experiment_id}')">
        <div class="exp-item-top">
          <div class="verdict-dot ${e.verdict}"></div>
          <span class="exp-num">#${e.id_in_run}</span>
          <span class="exp-id">${e.experiment_id}</span>
          <span class="badge ${mc}">M${e.mechanistic_score}</span>
          ${e.novelty_tier ? `<span class="badge ${tc}">T${e.novelty_tier}</span>` : ''}
          <button class="fav-btn${favOn}" title="Toggle favorite" onclick="toggleFav('${e.experiment_id}', event)">${favStar}</button>
        </div>
        <div class="exp-hyp">${e.hypothesis}</div>
      </div>`;
    });
  }
  el.innerHTML = html;
}

function selectExp(eid) {
  activeId = eid;
  renderSidebar();
  renderCard(eid);
}

function renderCard(eid) {
  const exp = DATA.experiments.find(e => e.experiment_id === eid);
  const lit = DATA.literature[eid];
  const main = document.getElementById('main');

  if (!exp) { main.innerHTML = '<div class="empty-state">Experiment not found</div>'; return; }

  const disconfirmed = exp.posterior < exp.prior;
  const barColor = disconfirmed ? 'var(--opp)' : 'var(--pass)';
  const barWidth = Math.round(exp.posterior * 100);

  let flagHtml = '';
  if (exp.flags && exp.flags.length) {
    flagHtml = `<div class="limitations"><span>⚠</span> ${exp.flags.map(escHtml).join(' · ')}</div>`;
  }

  // Literature tabs
  let litHtml = '';
  if (lit) {
    const tabId = eid;
    if (!activeTab[tabId]) activeTab[tabId] = 'map';

    const srcLabels = { snippet: 'from snippet', abstract: 'from abstract', 'ai_summary': 'from AI summary', unavailable: 'abstract unavailable' };
    const srcClasses = { snippet: 'snippet', abstract: 'abstract', 'ai_summary': 'ai-summary', unavailable: 'unavailable' };
    const srcTitles = {
      snippet: 'Claim sourced from verbatim PDF text — highest reliability',
      abstract: 'Claim extracted from paper abstract — reliable',
      'ai_summary': 'Claim derived from AI-generated relevance summary — verify before citing',
      unavailable: 'No abstract or text available — claim not written',
    };

    const renderPapers = (papers, type) => {
      if (!papers || !papers.length) return '<div class="empty-papers">No papers found for this category.</div>';
      return '<div class="paper-list">' + papers.map(p => {
        const titleEl = p.url
          ? `<a class="paper-title paper-link" href="${escHtml(p.url)}" target="_blank" rel="noopener">${escHtml(p.title || 'Untitled')} ↗</a>`
          : `<div class="paper-title">${escHtml(p.title || 'Untitled')}</div>`;
        const excerptEl = p.excerpt
          ? `<div class="paper-excerpt"><div class="paper-excerpt-text">${escHtml(p.excerpt)}</div>${p.excerpt_section ? `<div class="paper-excerpt-src">${escHtml(p.excerpt_section)}</div>` : ''}</div>`
          : '';
        const cs = p.claim_source;
        const srcBadge = cs
          ? `<div class="claim-src ${srcClasses[cs] || 'unknown'}" title="${srcTitles[cs] || ''}">${srcLabels[cs] || cs}</div>`
          : `<div class="claim-src unknown" title="Source not recorded — card built before source tracking was added">source unknown</div>`;
        return `
        <div class="paper-card">
          <div class="paper-top">
            <div class="paper-type ${type}"></div>
            ${titleEl}
            <span class="score-pill">${p.relevanceScore?.toFixed(2) ?? '—'}</span>
          </div>
          <div class="paper-meta">${escHtml(p.authors || '')} · ${p.year || '?'} · <em>${escHtml(p.venue || '')}</em>${p.citationCount ? ` · ${p.citationCount} citations` : ''}</div>
          ${srcBadge}
          ${p.claim ? `<div class="paper-claim">${escHtml(p.claim)}</div>` : ''}
          ${excerptEl}
        </div>`;
      }).join('') + '</div>';
    };

    const tabs = [
      { id: 'map',        label: 'Knowledge Map', cls: '', papers: null },
      { id: 'supporting', label: 'Supporting', cls: 'sup', papers: lit.supporting || [] },
      { id: 'opposing',   label: 'Opposing',   cls: 'opp', papers: lit.opposing || [] },
      { id: 'contextual', label: 'Contextual', cls: 'ctx', papers: lit.contextual || [] },
    ];

    const tabBar = tabs.map(t => {
      const badge = t.papers !== null ? `<span class="tab-badge ${t.cls}">${t.papers.length}</span>` : '';
      const active = activeTab[eid] === t.id ? ' active' : '';
      return `<div class="tab${active}" onclick="switchTab('${eid}','${t.id}')">${t.label}${badge}</div>`;
    }).join('');

    const km = lit.knowledge_map || {};
    const knownList = (km.known || []).map(k => `<li>${escHtml(k)}</li>`).join('');
    const unknownList = (km.unknown || []).map(k => `<li>${escHtml(k)}</li>`).join('');

    // Contribution type badge
    const ct = (km.contribution_type || '').toLowerCase();
    const ctClass = ct.includes('resolution') ? 'ct-badge-resolution'
                  : ct.includes('constraint') && ct.includes('negative') ? 'ct-badge-negative'
                  : ct.includes('constraint') ? 'ct-badge-constraint'
                  : ct.includes('replication') ? 'ct-badge-replication'
                  : ct.includes('negative') ? 'ct-badge-negative'
                  : 'ct-badge-unknown';
    const ctLabel = km.contribution_type || 'Not classified';
    const ctTitles = {
      'ct-badge-resolution': 'Resolution: directly tests and closes the gap — same circuit, same task, adequate N',
      'ct-badge-constraint': 'Constraint: narrows the gap without closing it — related circuit/task, borderline N, or residual confounds',
      'ct-badge-replication': 'Replication: confirms a known finding in a new context (new species, region, or task)',
      'ct-badge-negative': 'Negative constraint: null result rules out a specific model prediction',
    };
    const ctBadge = `<div class="contribution-type"><span class="ct-label">Contribution</span><span class="${ctClass}" title="${ctTitles[ctClass] || ''}">${escHtml(ctLabel)}</span></div>`;

    const caveatImpact = km.caveat_impact
      ? `<div class="km-card caveat"><div class="km-title caveat-title">What the Caveats Affect</div><div class="km-sheds">${escHtml(km.caveat_impact)}</div></div>`
      : '';

    const mapHtml = `
      <div class="km-grid">
        <div class="km-card">
          <div class="km-title known">What is Known</div>
          <ul class="km-list">${knownList || '<li>No entries</li>'}</ul>
        </div>
        <div class="km-card">
          <div class="km-title unknown">Unknown / Contested</div>
          <ul class="km-list">${unknownList || '<li>No entries</li>'}</ul>
        </div>
        <div class="km-card full">
          <div class="km-title sheds">How This Hypothesis Sheds Light</div>
          ${ctBadge}
          <div class="km-sheds">${escHtml(km.how_this_sheds_light || '')}</div>
        </div>
        ${caveatImpact}
      </div>`;

    const contentPanels = tabs.map(t => {
      const active = activeTab[eid] === t.id ? ' active' : '';
      const inner = t.id === 'map' ? mapHtml : renderPapers(t.papers, t.id === 'supporting' ? 'sup' : t.id === 'opposing' ? 'opp' : 'ctx');
      return `<div class="tab-content${active}" id="tab-${eid}-${t.id}">${inner}</div>`;
    }).join('');

    litHtml = `<div class="tabs">${tabBar}</div><div class="tabs-body">${contentPanels}</div>`;
  } else {
    litHtml = '<div class="no-card-msg">No literature evidence loaded yet. Run the experiment-card skill on this experiment.</div>';
  }

  // Plan section
  let planHtml = '';
  // Plan comes from the markdown card
  const cardMd = DATA.cards[eid];
  let planObj = { objective: '', steps: '', deliverables: '', analysis: '', review: '', reflection: '' };
  if (cardMd) {
    const sections = {
      objective: /\*\*Objective:\*\*\s*([^\n]+)/.exec(cardMd),
      steps: /\*\*Steps:\*\*\n([\s\S]*?)(?=\n\*\*Deliverables|\n##)/.exec(cardMd),
      deliverables: /\*\*Deliverables:\*\*\s*([^\n]+)/.exec(cardMd),
    };
    planObj.objective = sections.objective?.[1] || '';
    planObj.steps = sections.steps?.[1]?.trim() || '';
    planObj.deliverables = sections.deliverables?.[1] || '';

    // Extract sections 5 and 6 from markdown
    const sec5 = /## 5\. Results and Findings\n([\s\S]*?)(?=\n## 6\.)/.exec(cardMd);
    const sec6 = /## 6\. Reflection\n([\s\S]*?)$/.exec(cardMd);
    planObj.analysis = sec5?.[1]?.trim() || '';
    planObj.reflection = sec6?.[1]?.trim() || '';
  }

  planHtml = `<div class="plan-grid">
    <div class="plan-block full">
      <div class="plan-label">Objective</div>
      <div class="plan-text">${planObj.objective}</div>
    </div>
    <div class="plan-block full">
      <div class="plan-label">Steps</div>
      <div class="plan-text">${planObj.steps}</div>
    </div>
    <div class="plan-block full">
      <div class="plan-label">Deliverables</div>
      <div class="plan-text">${planObj.deliverables}</div>
    </div>
  </div>`;

  const noveltyTierLabel = ['', 'Fills an explicitly flagged gap', 'Predicted but unmeasured', 'Validates existing framework', 'Positive control'];
  const tierLabel = lit ? (noveltyTierLabel[lit.novelty_tier] || '') : '';
  const tierC = lit ? tierColor(lit.novelty_tier) : '';

  // Extract N complete sentences — splits only on [.!?] followed by space+capital or end,
  // so decimal numbers (0.708) and abbreviations don't break sentences.
  function firstSentences(text, n) {
    const flat = text.replace(/\n+/g, ' ').replace(/\s+/g, ' ').trim();
    // Split on sentence-ending punctuation followed by whitespace + uppercase letter, or end
    const parts = flat.split(/(?<=[.!?])\s+(?=[A-Z("])/);
    return parts.slice(0, n).join(' ').trim() || flat.slice(0, 200);
  }

  // Build prior work bullets from top supporting papers
  const topPapers = lit ? (lit.supporting || []).slice(0, 4) : [];
  const priorWorkHtml = topPapers.length
    ? topPapers.map(p => {
        const url = p.url || `https://www.semanticscholar.org/search?q=${encodeURIComponent(p.title || '')}&sort=Relevance`;
        const authYear = p.authors ? `${p.authors.split(',')[0].trim()} et al., ${p.year || '?'}` : (p.year || '?');
        // One sentence per paper in slide view
        const claimText = p.claim ? firstSentences(p.claim, 1) : null;
        const claimEl = claimText
          ? `<div class="prior-work-claim">${escHtml(claimText)}</div>`
          : `<div class="prior-work-no-claim">claim not saved — re-run experiment-card skill</div>`;
        const titleShort = p.title ? (p.title.length > 80 ? p.title.slice(0, 80) + '…' : p.title) : '';
        return `<div class="prior-work-item"><div class="prior-work-item-header"><a href="${escHtml(url)}" target="_blank" rel="noopener">${escHtml(authYear)}</a><span style="color:var(--text-dim);font-size:11px">${escHtml(titleShort)}</span></div>${claimEl}</div>`;
      }).join('')
    : '<div style="font-size:12px;color:var(--text-dim);font-style:italic">Run experiment-card skill to load literature</div>';

  // Result: first 2 sentences of analysis
  const resultShort = planObj.analysis
    ? firstSentences(planObj.analysis, 2)
    : (exp.finding || '');

  // Method: first sentence of objective
  const methodShort = planObj.objective
    ? firstSentences(planObj.objective, 1)
    : '';

  // Takeaway: extract interpretive sentence from reflection
  // Prefer content under **Interpretation:** / **What was shown:** markers;
  // fall back to first sentence with evaluative language; last resort: triage finding
  function extractTakeaway(refl, finding) {
    if (!refl) return finding || '';
    // Try labelled sections: Interpretation, What was shown, Results did not
    const labelMatch = refl.match(/\*\*(?:Interpretation|What was shown|Part 1)[^*]*\*\*[:\s]*([\s\S]*?)(?:\n\n|\*\*|$)/i);
    if (labelMatch) return firstSentences(labelMatch[1].trim(), 1);
    // Try first sentence with interpretive language
    const flat = refl.replace(/\n+/g, ' ').replace(/\*\*[^*]+\*\*/g, '').trim();
    const sentences = flat.match(/[^.!?]+[.!?]+/g) || [];
    const interpretive = sentences.find(s =>
      /consistent with|support|suggest|rule out|did not|no significant|significant|failed to|confirmed|reject|null result|weaken|strengthen/i.test(s)
      && !/The following|conservative interpretation|grounded in/i.test(s)
    );
    if (interpretive) return interpretive.trim();
    // Fall back to triage finding field
    return finding || '';
  }
  const takeaway = extractTakeaway(planObj.reflection, exp.finding || '');

  const beliefDirection = exp.posterior > exp.prior ? 'strengthened' : 'weakened';
  const beliefWord = exp.prior >= 0.7 ? 'Likely True' : exp.prior >= 0.4 ? 'Maybe True' : 'Unlikely';

  main.innerHTML = `
    <div class="card-header">
      <div class="card-eyebrow" style="display:flex;align-items:center;gap:8px">
        <span>${exp.run_name} · #${exp.id_in_run} · ${exp.experiment_id} · <a href="https://autodiscovery.allen.ai/runs/shared/${exp.run_id}?exp=${exp.id_in_run}" target="_blank" rel="noopener" style="color:var(--teal);text-decoration:none;font-weight:700">↗ AutoDiscovery</a></span>
        <button class="fav-btn-header${_favorites.has(eid) ? ' on' : ''}" id="fav-btn-header-${eid}" title="Favorite this experiment" onclick="toggleFav('${eid}', event)">${_favorites.has(eid) ? '★' : '☆'}</button>
        <button class="claude-btn" title="Open this experiment card in Claude" onclick="openInClaude('${eid}')">Ask Claude ↗</button>
      </div>
      <div class="card-title">${escHtml(exp.hypothesis.slice(0, 160))}${exp.hypothesis.length > 160 ? '…' : ''}</div>
      <div class="card-meta">
        <div class="meta-pill" title="PASS = ran successfully with a clear result&#10;FLAG = ambiguous result, small N, or methodological concerns"><span class="label">Verdict</span><strong style="color:${verdictColor(exp.verdict)}">${exp.verdict}</strong></div>
        <div class="meta-pill" title="Mechanistic score 1–5&#10;5 = direct causal test of the mechanism&#10;4 = strong correlational evidence with controls&#10;3 = observational evidence consistent with mechanism"><span class="label">Mech</span><span class="badge ${mechColor(exp.mechanistic_score)}">${exp.mechanistic_score}/5</span></div>
        ${lit ? `<div class="meta-pill" title="Novelty tier 1–4&#10;T1 = fills an explicitly flagged gap&#10;T2 = predicted but unmeasured in this circuit/task&#10;T3 = validates framework in a new context&#10;T4 = positive control (known finding re-observed)"><span class="label">Novelty</span><span class="badge ${tierC}">Tier ${lit.novelty_tier}</span><span style="font-size:11px;color:var(--text-dim)">${tierLabel}</span></div>` : ''}
        <div class="meta-pill" title="Surprise = prior − posterior belief shift&#10;Negative = evidence weakened belief in hypothesis&#10;Positive = evidence strengthened belief"><span class="label">Surprise</span><span class="belief-label">Δ ${exp.surprise.toFixed(3)}</span></div>
      </div>
      ${flagHtml}
    </div>
    ${dataContextHtml(exp, lit)}

    <div class="card-hero">
      <div class="hero-left">
        ${gaussianSvg(exp.prior, exp.posterior)}
        <div class="hero-belief-label">Belief before: <span>${beliefWord} (${exp.prior.toFixed(3)})</span></div>
        <div class="hero-hyp">${escHtml(exp.hypothesis)}</div>
      </div>
      <div class="hero-right">
        <div class="hero-block">
          <div class="hero-block-title">Prior Work</div>
          <div class="prior-work-list">${priorWorkHtml}</div>
        </div>
        <div class="hero-block">
          <div class="hero-block-title">Method</div>
          <div class="hero-method">${escHtml(methodShort)}</div>
        </div>
        <div class="hero-block">
          <div class="hero-block-title">Result</div>
          <div class="hero-result">${escHtml(resultShort) || '<em style="color:var(--text-dim)">Run experiment-card skill to load results</em>'}</div>
        </div>
      </div>
    </div>
    ${takeaway ? `<div class="takeaway">${escHtml(takeaway)}</div>` : ''}

    <div class="section">
      <div class="section-title"><span class="sec-num">02</span> Literature Evidence</div>
      ${litHtml}
    </div>

    <div class="section">
      <div class="section-title"><span class="sec-num">03</span> Experimental Plan</div>
      ${planHtml}
    </div>

    <div class="section">
      <div class="section-title"><span class="sec-num">05</span> Results &amp; Findings</div>
      <div class="results-box">${renderMd(planObj.analysis)}</div>
    </div>

    <div class="section">
      <div class="section-title"><span class="sec-num">06</span> Reflection</div>
      <div class="reflection-box">${renderMd(planObj.reflection)}</div>
    </div>

    <div class="section">
      <div class="section-title"><span class="sec-num">07</span> Notes</div>
      <div class="notes-list" id="notes-list-${eid}">${renderNotesList(eid)}</div>
      <div class="notes-input-row">
        <textarea class="notes-area" id="notes-input-${eid}"
          placeholder="Add a note — design decisions, follow-up ideas, team comments… (Ctrl+Enter to submit)"
          onkeydown="handleNoteKey(event, '${eid}')"></textarea>
        <div class="notes-submit-row">
          <button class="notes-submit-btn" onclick="submitNote('${eid}')">Add note</button>
          <span class="notes-status" id="notes-status-${eid}"></span>
        </div>
      </div>
    </div>
  `;
}

function switchTab(eid, tabId) {
  activeTab[eid] = tabId;
  // Update tab buttons
  document.querySelectorAll(`.tab`).forEach(t => t.classList.remove('active'));
  document.querySelectorAll(`.tab-content`).forEach(t => t.classList.remove('active'));
  // Re-render just the tab area is complex; just re-render card
  renderCard(eid);
}

// ── notes ──────────────────────────────────────────────────────────────────

const _serverMode = window.location.protocol === 'http:' && window.location.hostname === 'localhost';

// ── legend ───────────────────────────────────────────────────────────────────

function toggleLegend(e) {
  e.stopPropagation();
  const panel = document.getElementById('legend-panel');
  const btn = document.getElementById('legend-btn');
  const open = panel.classList.toggle('open');
  btn.classList.toggle('open', open);
  btn.textContent = open ? 'Legend ▴' : 'Legend ▾';
}
document.addEventListener('click', () => {
  const panel = document.getElementById('legend-panel');
  const btn = document.getElementById('legend-btn');
  if (panel && panel.classList.contains('open')) {
    panel.classList.remove('open');
    if (btn) { btn.classList.remove('open'); btn.textContent = 'Legend ▾'; }
  }
});

// ── favorites ────────────────────────────────────────────────────────────────

const _favorites = new Set(DATA.favorites || []);

function toggleFav(eid, e) {
  e.stopPropagation();
  if (_favorites.has(eid)) _favorites.delete(eid); else _favorites.add(eid);
  // Update sidebar item star
  renderSidebar();
  // Update card header star if that card is open
  const btn = document.getElementById('fav-btn-header-' + eid);
  if (btn) { btn.textContent = _favorites.has(eid) ? '★' : '☆'; btn.className = 'fav-btn-header' + (_favorites.has(eid) ? ' on' : ''); }
  // Persist
  if (_serverMode) {
    fetch('/api/favorites', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify([..._favorites]),
    }).catch(() => {});
  }
}

// In-memory notes: eid -> [{ts, text}, ...]  (starts from embedded DATA.notes)
const _notes = {};
function _initNotes(eid) {
  if (_notes[eid] === undefined) {
    const embedded = (DATA.notes || {})[eid];
    _notes[eid] = embedded ? [...embedded] : [];
  }
}

function renderNotesList(eid) {
  _initNotes(eid);
  if (!_notes[eid].length) return '';
  return _notes[eid].map(e => {
    const tsDisplay = e.ts
      ? e.ts.replace('T', ' ').replace(/:\d{2}$/, '').replace(/\.\d+Z?$/, '') + ' UTC'
      : '';
    return `<div class="note-entry">
      ${tsDisplay ? `<div class="note-ts">${escHtml(tsDisplay)}</div>` : ''}
      <div class="note-text">${escHtml(e.text)}</div>
    </div>`;
  }).join('');
}

function handleNoteKey(e, eid) {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); submitNote(eid); }
}

function submitNote(eid) {
  const input = document.getElementById('notes-input-' + eid);
  const status = document.getElementById('notes-status-' + eid);
  const text = input ? input.value.trim() : '';
  if (!text) return;

  const btn = input.parentElement.querySelector('.notes-submit-btn');
  if (btn) btn.disabled = true;

  const doAdd = (entry) => {
    _initNotes(eid);
    _notes[eid].push(entry);
    const list = document.getElementById('notes-list-' + eid);
    if (list) list.innerHTML = renderNotesList(eid);
    if (input) input.value = '';
    if (btn) btn.disabled = false;
    input && input.focus();
  };

  if (_serverMode) {
    fetch('/api/notes/' + encodeURIComponent(eid), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    }).then(r => r.json()).then(data => {
      if (data.ok) {
        doAdd(data.entry);
        if (status) { status.textContent = 'Saved to card'; setTimeout(() => { if (status) status.textContent = ''; }, 2000); }
      }
    }).catch(() => {
      // Fall back to local-only
      doAdd({ ts: new Date().toISOString(), text });
      if (status) { status.textContent = 'Saved locally (server unavailable)'; setTimeout(() => { if (status) status.textContent = ''; }, 3000); }
      if (btn) btn.disabled = false;
    });
  } else {
    doAdd({ ts: new Date().toISOString(), text });
    if (status) { status.textContent = 'Saved in browser — run serve_viewer.py to persist to card'; setTimeout(() => { if (status) status.textContent = ''; }, 4000); }
  }
}

function exportNotes() {
  try {
    const blob = new Blob([JSON.stringify(_notes, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'notes.json';
    document.body.appendChild(a); a.click();
    document.body.removeChild(a); URL.revokeObjectURL(a.href);
  } catch(e) { alert('Could not export notes: ' + e.message); }
}

// ── Ask Claude ───────────────────────────────────────────────────────────────

function buildClaudePrompt(eid) {
  const exp = DATA.experiments.find(e => e.experiment_id === eid);
  const lit = DATA.literature[eid];
  const cardMd = DATA.cards[eid];
  const parts = [];

  parts.push(`## Experiment: ${exp.experiment_id} (${exp.run_name} #${exp.id_in_run})`);
  parts.push(`**Hypothesis:** ${exp.hypothesis}`);
  parts.push(`**Verdict:** ${exp.verdict} | Mechanistic score: ${exp.mechanistic_score}/5${lit ? ` | Novelty: Tier ${lit.novelty_tier}` : ''}`);
  parts.push(`**Belief update:** prior ${exp.prior.toFixed(3)} → posterior ${exp.posterior.toFixed(3)} (surprise Δ${exp.surprise.toFixed(3)})`);
  if (exp.finding) parts.push(`**Finding:** ${exp.finding}`);
  if (exp.flags && exp.flags.length) parts.push(`**Flags:** ${exp.flags.join('; ')}`);

  if (lit) {
    const km = lit.knowledge_map || {};
    if (km.known && km.known.length)
      parts.push(`\n### What is Known\n${km.known.map(k => `- ${k}`).join('\n')}`);
    if (km.unknown && km.unknown.length)
      parts.push(`\n### Unknown / Contested\n${km.unknown.map(k => `- ${k}`).join('\n')}`);
    if (km.how_this_sheds_light)
      parts.push(`\n### How This Hypothesis Contributes\n${km.how_this_sheds_light}`);
    if (km.contribution_type)
      parts.push(`**Contribution type:** ${km.contribution_type}`);

    const formatPapers = (papers) => (papers || []).slice(0, 4).map(p => {
      const authYear = p.authors ? `${p.authors.split(',')[0].trim()} et al., ${p.year || '?'}` : (p.year || '?');
      return `- **${p.title}** (${authYear})${p.claim ? `\n  "${p.claim}"` : ''}`;
    }).join('\n');

    const sup = formatPapers(lit.supporting);
    if (sup) parts.push(`\n### Supporting Literature\n${sup}`);
    const opp = formatPapers(lit.opposing);
    if (opp) parts.push(`\n### Opposing Literature\n${opp}`);
    const ctx = formatPapers(lit.contextual);
    if (ctx) parts.push(`\n### Contextual Literature\n${ctx}`);
  }

  if (cardMd) {
    const sec3 = /## 3\. Experimental Plan\n([\s\S]*?)(?=\n## \d\.|$)/.exec(cardMd);
    const sec5 = /## 5\. Results and Findings\n([\s\S]*?)(?=\n## \d\.|$)/.exec(cardMd);
    const sec6 = /## 6\. Reflection\n([\s\S]*?)$/.exec(cardMd);
    if (sec3) parts.push(`\n### Experimental Plan\n${sec3[1].trim()}`);
    if (sec5) parts.push(`\n### Results and Findings\n${sec5[1].trim()}`);
    if (sec6) parts.push(`\n### Reflection\n${sec6[1].trim()}`);
  }

  return parts.join('\n');
}

function openInClaude(eid) {
  const prompt = buildClaudePrompt(eid);
  navigator.clipboard.writeText(prompt).then(() => {
    showToast('Prompt copied — paste into Claude (⌘V)');
    window.open('https://claude.ai/new', '_blank', 'noopener,noreferrer');
  }).catch(() => {
    const ta = document.createElement('textarea');
    ta.value = prompt;
    ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('Prompt copied — paste into Claude (⌘V)');
    window.open('https://claude.ai/new', '_blank', 'noopener,noreferrer');
  });
}

function showToast(msg) {
  let t = document.getElementById('claude-toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'claude-toast';
    t.style.cssText = 'position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(12px);background:#0A1C18;border:1px solid var(--pink-mid);color:var(--text);font-size:13px;font-family:Inter,sans-serif;padding:10px 20px;border-radius:10px;box-shadow:0 4px 20px #000a;opacity:0;transition:opacity 0.2s,transform 0.2s;z-index:9999;pointer-events:none';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.opacity = '1';
  t.style.transform = 'translateX(-50%) translateY(0)';
  clearTimeout(t._timer);
  t._timer = setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(-50%) translateY(12px)';
  }, 3500);
}

// init
renderSidebar();
// Auto-select first card-having experiment
const firstCard = DATA.experiments.find(e => e.has_card);
if (firstCard) selectExp(firstCard.experiment_id);
</script>
</body>
</html>
"""

out = BASE / "viewer.html"
out.write_text(html)
print(f"Viewer written to: {out}")
print(f"Experiments: {len(all_experiments)} ({sum(1 for e in all_experiments if e['has_card'])} with cards)")
