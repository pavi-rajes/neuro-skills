---
name: experiment-card
description: >
  Build an experiment card for a hypothesis from AutoDiscovery. Use when the user asks to
  "build an experiment card", "write up an experiment", "document this hypothesis", "create a
  card for experiment X", or "what does the literature say about this hypothesis". Takes a run
  ID + experiment ID, or a hypothesis loaded from a triage JSON. Produces a structured card
  with literature evidence, knowledge map, novelty score, and a conservative interpretation
  of findings. Saves to autodiscovery-runs/<runid>/experiment-cards/.
argument-hint: <runid> <experiment_id>
user-invocable: true
---

# Experiment Card

Builds a structured experiment card for a single AutoDiscovery hypothesis. The card has seven
components; this skill implements **Component 2: Literature Evidence** and the
**Knowledge Map** in full. Other components pull directly from AutoDiscovery fields.

---

## Step 1 — Load the Hypothesis

### Option A: From triage JSON

```python
import json

with open("autodiscovery-runs/<runid>/triage.json") as f:
    triage = json.load(f)

# Find the experiment
exp = next(
    e for e in triage["passing"] + triage["flagged"]
    if e["experiment_id"] == "<experiment_id>"
)
hypothesis = exp["hypothesis"]
caveats    = exp.get("caveats", [])  # Load caveats — used in Steps 4 and 5
```

### Option B: From AutoDiscovery directly

```bash
asta autodiscovery experiments <runid> --format json
```

Find the experiment by `experiment_id` and extract:
- `hypothesis`
- `experiment_plan` (`objective`, `steps`, `deliverables`)
- `analysis`
- `review`
- `code_output`
- `surprise`, `prior`, `posterior`

Also load dataset context from the triage JSON (used in Component 0):
```python
run_description = triage.get("run_description", "")
species         = triage.get("species", "")
task            = triage.get("task", "")
caveats         = exp.get("caveats", [])  # list of strings
```

If neither a triage JSON nor a run ID is provided, ask the user to paste the hypothesis text.

---

## Step 2 — Decompose into Search Queries

Before searching, decompose the hypothesis into **8–10 targeted queries** covering
different angles. Do not use the hypothesis text verbatim as a query — it is too specific.
Each query should target one facet of the claim. More queries = better coverage; err on the
side of more.

**Write queries as natural language questions or descriptive phrases, not keyword dumps.**
Good: `"How does attention route information between visual and motor cortex?"`
Bad: `"attention routing visual motor cortex subspace alignment"`

The `asta literature find` tool uses AI-powered semantic search — full sentences retrieve
better results than keyword lists. Each query should read like a sentence a scientist would
type when searching for that topic.

**Decomposition strategy:**

| Facet | What to query | Example (natural language) |
|---|---|---|
| **Core mechanism** | The causal claim as a question | "Does attention change the geometry of sensory-to-motor communication subspaces?" |
| **Brain regions** | The specific circuit as a research question | "How does secondary motor cortex receive visual context signals from VIS?" |
| **Computational framework** | The method as a literature search | "Reduced rank regression for measuring inter-areal communication in neural populations" |
| **Behavioral context** | The task as a research topic | "Neural basis of context-dependent action selection in visual auditory switching tasks" |
| **Opposing account** | The alternative as an explicit search | "Gain modulation explains attention effects in sensory cortex without changing subspace geometry" |
| **Foundational theory** | The seminal theory by name and concept | "Kaufman null space potent space preparatory activity and movement suppression motor cortex" |
| **Species/region transfer** | Analogous work in other systems | "Communication subspace between cortical areas changes with cognitive context in primates" |
| **Methodological precedent** | Same analysis in other datasets | "Partial least squares or reduced rank regression applied to visual cortical populations" |
| **Methodological skeptic** | Limitations or confounds of the method itself | "Confounds and limitations of reduced-rank regression for inter-areal communication estimation" |
| **Recent advances** | Current state of the field (last 3 years) | "Communication subspace reconfiguration during cognitive flexibility 2022 2023 2024" |

**Required query constraints:**
- The **opposing account** query must search for papers that *challenge* the hypothesis — not
  just papers on the same topic. Frame it as: "What is the strongest alternative explanation
  for this effect?" and search for that alternative directly.
- The **methodological skeptic** query must target the *experimental design* used by
  AutoDiscovery, not just the hypothesis. If the experiment uses RRR, search for known
  confounds of RRR. If it uses small N, search for "statistical power inter-areal communication
  estimation." This surfaces literature that challenges the experiment's own validity, not just
  its conclusion.
- Include **at least 2 queries targeting papers from 2022 onward**. Semantic search
  over-weights highly-cited older work. The recent literature is often where the active debate
  lives.

After generating queries, review them: if two queries are very similar, replace one with a
query targeting a different aspect you haven't covered yet.

---

## Step 3 — Run Literature Searches

Run all searches in parallel. Use `run_in_background=true` for every search — they take
30–60s each. Save each to a uniquely named temp file.

```bash
asta literature find '<query_1>'  -o /tmp/lit_<experiment_id>_q1.json  --timeout 300
asta literature find '<query_2>'  -o /tmp/lit_<experiment_id>_q2.json  --timeout 300
asta literature find '<query_3>'  -o /tmp/lit_<experiment_id>_q3.json  --timeout 300
asta literature find '<query_4>'  -o /tmp/lit_<experiment_id>_q4.json  --timeout 300
asta literature find '<query_5>'  -o /tmp/lit_<experiment_id>_q5.json  --timeout 300
asta literature find '<query_6>'  -o /tmp/lit_<experiment_id>_q6.json  --timeout 300
asta literature find '<query_7>'  -o /tmp/lit_<experiment_id>_q7.json  --timeout 300
asta literature find '<query_8>'  -o /tmp/lit_<experiment_id>_q8.json  --timeout 300
asta literature find '<query_9>'  -o /tmp/lit_<experiment_id>_q9.json  --timeout 300
asta literature find '<query_10>' -o /tmp/lit_<experiment_id>_q10.json --timeout 300
```

After all complete, merge and deduplicate by `corpusId`:

```python
import json, glob

all_papers = {}
for fname in glob.glob("/tmp/lit_<experiment_id>_q*.json"):
    data = json.load(open(fname))
    for paper in data["results"]:
        cid = paper["corpusId"]
        if cid not in all_papers or paper["relevanceScore"] > all_papers[cid]["relevanceScore"]:
            all_papers[cid] = paper

# Sort by relevance
papers = sorted(all_papers.values(), key=lambda p: -p["relevanceScore"])
print(f"Total unique papers: {len(papers)}")
print(f"Above 0.6: {sum(1 for p in papers if p['relevanceScore'] > 0.6)}")
```

**Reading the results — be thorough:**

For papers with `relevanceScore > 0.6`:
- Read the full `relevanceJudgement.relevanceSummary` — this is an AI-written assessment of
  why the paper is relevant; it often contains the specific claim that matters.
- Read ALL `snippets[].text` entries — these are direct text excerpts from the paper body
  (only available for open-access papers). They often contain the key quantitative results.
- Read `citationContexts[].text` — these show how later papers cite this work, which
  reveals the consensus interpretation of the finding.

For papers with `relevanceScore` between 0.4 and 0.6:
- Read the `relevanceSummary` to decide whether to include; skip the snippets unless the
  summary indicates a highly relevant finding.

Include all papers above `relevanceScore > 0.4` in the evidence pool. Only papers below
0.4 should be excluded — err on the side of inclusion and let the categorization step
decide whether each paper is actually relevant.

---

## Step 4 — Categorize Evidence

For each paper with `relevanceScore > 0.5`, assign it to one category. A paper can appear
in multiple categories if it contains multiple relevant claims.

### Supporting evidence
Papers that:
- Demonstrate the same mechanism in a related circuit, task, or species
- Validate the computational framework the hypothesis invokes
- Report quantitative effects in the same direction as the hypothesis predicts
- Provide foundational evidence the hypothesis depends on

### Opposing evidence
Papers that:
- Demonstrate a contradictory mechanism
- Fail to find the predicted effect in a closely matched setup
- Provide evidence for an alternative explanation
- Explicitly argue against the theoretical framework the hypothesis invokes
- Raise methodological concerns about the analysis approach used in this experiment

### Contextual evidence
Papers that:
- Establish the theoretical framework without directly testing this hypothesis
- Characterize the brain regions or task without making the causal claim
- Provide methodological precedent (same analysis applied elsewhere)
- Define what is already known, framing what is unknown

**For each paper, extract:**
- Full citation (authors, title, year, venue)
- `url` — copy `paper["url"]` from the search result directly. Always save it.
- `relevanceScore` — copy `paper["relevanceScore"]` from the search result.
- `abstract` — copy `paper["abstract"]` if the field exists and is non-empty in the search
  result. Set to null otherwise. Do not fetch externally here.
- **`claim`** — Write 1–2 sentences describing the specific finding relevant to this
  hypothesis. Follow this strict priority order and **always record the source**:
  1. **Snippet** (`paper["snippets"]` has text): quote verbatim or close paraphrase from
     snippet text. Set `claim_source = "snippet"`.
  2. **Abstract** (`paper["abstract"]` is non-null): extract the core finding sentence
     from the abstract text. Set `claim_source = "abstract"`.
  3. **AI summary** (`paper["relevanceJudgement"]["relevanceSummary"]` only): extract what
     the summary explicitly states. Set `claim_source = "ai_summary"`. **Do not add
     specificity, quantitative values, or mechanistic detail not present in the summary
     text. A hedged vague claim from AI summary is correct; a specific-sounding claim
     inferred from training knowledge is not.**
  4. **None available**: set `claim = "[abstract not available — claim not written]"`,
     `claim_source = "unavailable"`. Write nothing else.
- **`claim_source`** — **Required. Never omit.** One of:
  - `"snippet"` — verbatim or close paraphrase from open-access PDF text
  - `"abstract"` — extracted from abstract field in search result
  - `"ai_summary"` — derived from `relevanceSummary` (AI-generated; treat with caution)
  - `"unavailable"` — no snippet, abstract, or summary text available
- `excerpt` — if `snippets` has text, copy the single most relevant verbatim snippet (max 300
  chars). Set to null if no snippets available.
- `excerpt_section` — the `sectionTitle` of that snippet, or null.
- `comparability` — **new field.** Cross-check the triage `caveats` list loaded in Step 1.
  If any caveat affects comparability with this paper's findings (e.g., the paper used 5× more
  subjects, or the triage flagged "driven by one subject" while this paper had n=20), write a
  one-sentence note: `"Triage caveat: [caveat] — reduces comparability because [reason]"`.
  Set to null if no caveats apply.
- `direct_analogical` — one of three tiers:
  - `direct` — same circuit (same regions) AND same task
  - `analogical-circuit` — same task, different regions or species
  - `analogical-task` — same regions, different task or species

**Verification pass for opposing papers (do this):**
After categorizing, for each paper in "opposing evidence" where `claim_source` is
`"ai_summary"` or `"unavailable"`, fetch the abstract via `WebFetch` on `paper["url"]`.
This is the highest-stakes category — a mischaracterized opposing paper distorts the
knowledge map. Limit to ≤ 5 papers to stay feasible. If the fetched page contains an
abstract that contradicts or refines the AI summary claim, update `claim` and set
`claim_source = "abstract"`.

---

## Step 5 — Build Knowledge Map

After categorizing, synthesize into four explicit zones.

### What is known
Findings supported by ≥ 2 independent papers from different labs or species.
State each as a declarative fact with citations. Be conservative — only include things
that are genuinely established, not just reported once.

### What is unknown / contested
Explicitly flagged gaps from reviews, conflicting results across papers, or questions
raised but not answered. Include:
- Open questions stated in review papers
- Effects shown in one species/task but not confirmed in others
- Conflicting findings (paper A says X, paper B says not-X)
- Methodological disputes surfaced by the skeptic queries

### How this hypothesis sheds light

Map the hypothesis onto the gap zone using this reasoning framework:

**First, identify the decision node.** What downstream research decision would a scientist
make differently depending on this experiment's outcome? Be specific — not "it informs our
understanding of X" but "a positive result would justify using RRR as a proxy for routing
strength in future studies; a negative result would suggest researchers need a different
estimator."

**Then, classify the contribution type:**

| Type | Description | Signal |
|---|---|---|
| **Resolution** | Experiment directly tests the gap; outcome closes it | Same circuit, same task, adequate N, clean effect |
| **Constraint** | Experiment narrows the gap without closing it | Related circuit/task, or borderline N, or confounds remain |
| **Replication** | Experiment confirms a known finding in a new context | Known effect, new species/region/task |
| **Negative constraint** | Null result rules out a model prediction | No effect where one was predicted |

Most AutoDiscovery experiments will be **Constraint** or **Replication**. Call this honestly.

**Finally, write one paragraph** stating:
- Which specific unknown this experiment addresses (cite the gap from "unknown" section)
- The contribution type (Resolution / Constraint / Replication / Negative constraint)
- What a positive result would establish that is not currently established
- What a negative result would rule out
- What the experiment cannot resolve even with a positive result

### What the caveats affect
**New zone.** If triage caveats were loaded, state explicitly how each caveat limits the
knowledge-map interpretation. Example: "The small-N caveat (flagged in triage) means a
positive result here is a Constraint, not a Resolution — the effect size estimate is
unreliable and the finding would need replication in a larger cohort before it could be
treated as established."

If no caveats were loaded, write: "No triage caveats — caveat impact not assessed."

---

## Step 6 — Score Novelty

Use the same 4-tier scale as the triage skill:

| Tier | Description |
|---|---|
| **1** | Fills an explicitly flagged gap: a review stated "X has not been tested" and this tests X directly. |
| **2** | Quantifies a predicted but unmeasured effect: the framework predicted this, but no one measured it in this specific circuit/task/species. |
| **3** | Confirms an existing framework in a new context. Valid contribution — frame as validation. |
| **4** | Positive control — a known finding re-observed. Useful as system validation only. |

**Scoring procedure:**
1. If any paper in Supporting evidence reports the same result in the same circuit and task → Tier 4
2. If the result is shown in other species/circuits but not this one → Tier 3
3. If the framework predicts this result but it has never been measured → Tier 2
4. If a review paper explicitly lists this as an open question → Tier 1

State the tier with a one-sentence justification and cite the specific paper(s) that
determined it.

---

## Step 7 — Assemble the Card

The experiment card has seven components. Pull from AutoDiscovery fields for components
1, 3, 4, 5 and write components 0, 2, and 6 from this skill's analysis.

**Before assembling, check for review/analysis conflict:**
Read both `analysis` and `review` fields. If `review` contradicts or overrides the
conclusion in `analysis`, this must be flagged explicitly in Component 5 and Component 6.
The `review` verdict is authoritative. Do not silently use one and ignore the other.

### Component 0 — Dataset Context

A compact header strip answering: **what data did this analysis actually run on?**

Extract from `code_output` and `experiment_plan.steps`:

1. **Sessions / NWB files**: Scan `code_output` for filenames or session IDs loaded
   (e.g. `Loading session_664851.nwb`, `Processing Subject 664851`). List the session IDs
   or NWB filenames that were actually processed.

2. **Regions recorded**: Scan `code_output` for lines like `Subject 664851: VIS=43 units,
   MOs=12 units` — extract which regions had sufficient units per subject. These are the
   regions that contributed data, not just the regions that were requested.

3. **Task**: From `experiment_plan.steps` or `analysis`, name the behavioral task
   (e.g. "dynamic routing visual/auditory context-switching task").

4. **Unit counts**: Note total units or per-region unit counts if prominently mentioned.

```
Sessions: 664851, 742903, 668755, 759434, 713655 (5 subjects)
Regions: VIS (43–87 units/subject), MOs (12–31 units/subject)
Task: Visual/auditory context-switching, licking response
```

Keep it to 2–3 lines maximum.

### Component 1 — Hypothesis
The hypothesis as stated by AutoDiscovery, plus any known limitations flagged by the
triage skill (from the triage JSON `caveats` field if available).

### Component 2 — Literature Evidence *(this skill)*
- Supporting evidence (papers + specific claims + comparability notes)
- Opposing evidence (papers + specific claims + comparability notes)
- Contextual evidence (papers + specific claims)
- Knowledge map: Known / Unknown / How this sheds light (with contribution type) / What the caveats affect

### Component 3 — Experimental Plan
From `experiment_plan`: `objective`, `steps`, `deliverables`.

### Component 4 — Similar Analyses in the Literature

Papers that implement the **same analysis method** — not just the same topic.

**A paper qualifies for Component 4 if it uses the same estimator class** (e.g., RRR,
CCA, dDMD, GPFA, PLS) on neural population data. Brain region and species are irrelevant
to this qualification — the math is what matters.

For each qualifying paper, state:
- Which specific method step matches (e.g., "uses RRR to estimate communication subspace
  dimensionality" not just "studies inter-areal communication")
- Whether it was applied to the same or different regions
- Whether it was applied to the same or different task
- Any methodological limitations or caveats the authors note about the estimator

### Component 5 — Results and Findings
From AutoDiscovery `analysis` and `review` fields.

If `review` contradicts `analysis`, report both and flag the discrepancy explicitly:
> **Note:** The `review` field revises the conclusion from `analysis`. The `review` verdict
> is treated as authoritative below, but the discrepancy is noted for transparency.

Do not re-interpret — report what the experiment found.

### Component 6 — Reflection *(conservative)*

**Before writing, extract these concrete facts from `analysis` and `review`:**
- The actual quantitative result (effect size, p-value, N, direction)
- Whether the effect replicated across subjects or was driven by a subset
- Whether the result supports or refutes the hypothesis, or is ambiguous
- Any limitations noted by AutoDiscovery's own review
- Whether `review` overrides `analysis` (flagged in Component 5)

**Write the reflection by filling in this template exactly. Do not skip fields, do not
merge parts, do not proceed to the next part until the current one is complete.**

```
**What was shown:**
[Verdict]: <e.g., "This result does not support the hypothesis" / "This result is
  consistent with the hypothesis but does not confirm it">
[Effect direction and size]: <e.g., "VIS→MOs communication subspace alignment did not
  significantly differ between visual and auditory context blocks">
[Key statistic]: <e.g., "N=4 subjects, t=−0.73, p=0.52">
[Replication]: <e.g., "Effect was consistent across all 4 subjects" OR "Effect was driven
  by 2 of 4 subjects — the group result is not robust">

**Null hypothesis:**
[State it explicitly]: "The null hypothesis is that [X]. This experiment [rejected /
  failed to reject] the null (p = X, N = Y)."
[Power note]: "Given N=Y, this test had [adequate / inadequate / unknown] power to
  detect an effect of the predicted magnitude. Failure to reject [is / is not]
  informative about the true effect."

**What this rules out:**
[Rules out]: "This result rules out [specific model prediction or alternative], because
  [one-sentence mechanistic reason]."
[Does not rule out]: "This result does not rule out [specific alternative], because
  [one-sentence reason — e.g., small N, confound, indirect measure]."

**What would be needed next:**
[One experiment]: <e.g., "N≥10 subjects with matched unit counts across VIS and MOs
  would provide sufficient power to detect the predicted effect size">
[Why this upgrades the finding]: <e.g., "This would move the contribution from Constraint
  to Resolution by ruling out the small-N alternative explanation">
```

**Rules for each field:**
- **[Effect direction and size]**: state what was measured and whether the effect was present,
  absent, or opposite to the prediction. One sentence.
- **[Key statistic]**: include N and the primary test statistic (t, p, or effect size). Do NOT include prior→posterior Bayesian belief shift — that is AutoDiscovery metadata, not hypothesis testing. If p > 0.05, state it plainly — do not soften.
- **[Replication]**: explicitly state whether the effect was consistent across all subjects
  or driven by a subset. "Consistent across N/N subjects" or "present in K of N subjects."
- **[Verdict]**: one sentence using "consistent with", "does not support", or "rules out."
  Never use "demonstrates" or "proves" unless causality was established.
- **[State it explicitly]**: one sentence starting "The null hypothesis is that..." naming
  the specific tested quantity (not just "no effect"). Follow with "This experiment rejected /
  failed to reject the null (p = X, N = Y)." Use "failed to reject" — never "accepted."
- **[Power note]**: state whether N was adequate to detect the effect size the hypothesis
  predicts. "Adequate" requires a power calculation or prior effect size estimate.
  If neither exists, write "unknown power." Crucially: if power is inadequate or unknown,
  state explicitly whether the failure to reject is or is not informative about the true
  effect. A low-power null is not evidence of absence.
- **[Rules out]**: one sentence starting "This result rules out..." followed by a mechanistic
  reason. If the result is null, this is usually the most informative line — do not skip it.
- **[Does not rule out]**: one sentence starting "This result does not rule out..." followed
  by a specific alternative (not a generic "other mechanisms"). Both lines are required.
- **[One experiment]**: name the specific analysis or perturbation, including N or scale.
  No vague suggestions ("more data"). State what data, what analysis, what N.
- **[Why this upgrades]**: name the contribution type transition (e.g., Constraint → Resolution)
  and why the proposed experiment achieves it.

**Additional rules:**
- If `review` overrode `analysis`, the [Verdict] field must note what changed.
- Do not extrapolate beyond the task, circuit, and species studied.
- No forward-looking suggestion may appear before both "rules out" lines are written.
- The reflection is the most conservative section of the card — when in doubt, understate.

---

## Step 8 — Save Outputs

```bash
mkdir -p autodiscovery-runs/<runid>/experiment-cards/literature_evidence
```

Write two files:

**`autodiscovery-runs/<runid>/experiment-cards/literature_evidence/<experiment_id>_literature.json`**

```json
{
  "experiment_id": "<experiment_id>",
  "run_id": "<runid>",
  "hypothesis": "<full text>",
  "novelty_tier": 2,
  "novelty_justification": "<one sentence>",
  "dataset_context": {
    "sessions": ["664851", "742903", "668755", "759434", "713655"],
    "regions": {"VIS": "43–87 units/subject", "MOs": "12–31 units/subject"},
    "task": "Visual/auditory context-switching, licking response",
    "n_subjects": 5
  },
  "triage_caveats": ["<caveat 1>", "<caveat 2>"],
  "search_queries": ["<q1>", "<q2>", "..."],
  "review_analysis_conflict": false,
  "supporting": [
    {
      "corpusId": 123456,
      "title": "...",
      "authors": "...",
      "year": 2019,
      "venue": "Nature Neuroscience",
      "url": "<paper.url from search result>",
      "relevanceScore": 0.82,
      "claim": "<1-2 sentence claim — MUST be non-empty, or '[abstract only — claim not extractable]'>",
      "excerpt": "<verbatim quote from snippets[].text if available, else null>",
      "excerpt_section": "<snippets[].sectionTitle for the excerpt, else null>",
      "comparability": "<one-sentence caveat note, or null>",
      "direct_analogical": "direct | analogical-circuit | analogical-task"
    }
  ],
  "opposing": [ "..." ],
  "contextual": [ "..." ],
  "knowledge_map": {
    "known": ["<finding 1 with citations>"],
    "unknown": ["<gap 1>"],
    "contribution_type": "Constraint | Resolution | Replication | Negative constraint",
    "how_this_sheds_light": "<paragraph — decision node, contribution type, what positive result establishes, negative result rules out, what remains open>",
    "caveat_impact": "<paragraph — how triage caveats limit the knowledge-map interpretation>"
  }
}
```

**`autodiscovery-runs/<runid>/experiment-cards/<experiment_id>_card.md`**

```markdown
# Experiment Card: <experiment_id>

**Run:** <runid>
**Date:** <YYYY-MM-DD>
**Novelty:** Tier <N> — <justification>
**Contribution type:** Constraint | Resolution | Replication | Negative constraint
**Triage verdict:** PASS / FLAG  |  Mechanistic score: <N>/5

---

## 0. Dataset Context
Sessions: ...
Regions: ...
Task: ...

---

## 1. Hypothesis
<hypothesis text>

**Known limitations:** <from triage caveats, or "none flagged">

---

## 2. Literature Evidence

### Supporting
- **[Author et al., Year]** *Title* — <specific claim> *(comparability note if any)*
...

### Opposing
- **[Author et al., Year]** *Title* — <specific claim> *(comparability note if any)*
...

### Contextual
- **[Author et al., Year]** *Title* — <specific claim>
...

### Knowledge Map

**Known:**
- <finding> ([Author et al., Year])

**Unknown / contested:**
- <gap or conflict>

**How this hypothesis sheds light:**
*Contribution type: [Resolution / Constraint / Replication / Negative constraint]*

<paragraph — decision node, what positive result establishes, what negative result rules out,
what the experiment cannot resolve>

**What the caveats affect:**
<paragraph — how triage caveats limit interpretation, or "No triage caveats — not assessed">

---

## 3. Experimental Plan

**Objective:** <from experiment_plan.objective>

**Steps:**
<from experiment_plan.steps>

**Deliverables:** <from experiment_plan.deliverables>

---

## 4. Similar Analyses in the Literature
- **[Author et al., Year]** — Method: <estimator class>. Match: <which step matches>. Regions: same/different. Task: same/different. Caveats: <any noted by authors>.
...

---

## 5. Results and Findings

<from AutoDiscovery analysis and review fields>

*(If review overrides analysis, flag it here explicitly)*

---

## 6. Reflection

**What was shown:**
[Verdict]: <"This result does not support..." / "This result is consistent with...">
[Effect direction and size]: <one sentence>
[Key statistic]: <N, t/p — no prior→posterior>
[Replication]: <consistent across N/N subjects, or driven by K of N>

**Null hypothesis:**
[State it explicitly]: "The null hypothesis is that [X]. This experiment [rejected / failed to reject] the null (p = X, N = Y)."
[Power note]: "Given N=Y, this test had [adequate / inadequate / unknown] power to detect an effect of the predicted magnitude. Failure to reject [is / is not] informative about the true effect."

**What this rules out:**
[Rules out]: "This result rules out [specific prediction], because [reason]."
[Does not rule out]: "This result does not rule out [specific alternative], because [reason]."

**What would be needed next:**
[One experiment]: <specific analysis, N, scale>
[Why this upgrades]: <contribution type transition and reason>
```

---

## Loading the Literature Evidence

```python
import json

with open("autodiscovery-runs/<runid>/experiment-cards/literature_evidence/<experiment_id>_literature.json") as f:
    evidence = json.load(f)

supporting        = evidence["supporting"]
opposing          = evidence["opposing"]
novelty_tier      = evidence["novelty_tier"]
knowledge_map     = evidence["knowledge_map"]
contribution_type = evidence["knowledge_map"]["contribution_type"]
caveat_impact     = evidence["knowledge_map"]["caveat_impact"]
```

---

## Behavior Notes

- Run all literature searches in parallel (`run_in_background=true`) — 8–10 queries, all at once
- **Be thorough**: include all papers above `relevanceScore > 0.4`. Do not truncate.
- For papers with `relevanceScore > 0.6`: read the full `relevanceSummary`, all `snippets[].text`,
  and `citationContexts[].text`. Do not skim these.
- For papers with open-access `snippets`, quote the text directly rather than paraphrasing — the
  actual words matter.
- The `citationContexts` field (how later papers cite this work) is often the best signal for
  consensus interpretation. Prioritize it.
- **Silent failure guard**: if `snippets` is empty and `relevanceSummary` is vague, set `claim`
  to `"[abstract only — claim not extractable]"`. Never write a vague generic claim to fill the
  field.
- **Review/analysis conflict**: always check whether `review` overrides `analysis` before
  writing Components 5 and 6. If it does, flag it explicitly. The `review` verdict is
  authoritative.
- If fewer than 3 supporting papers are found, say so explicitly — do not inflate the literature.
- If no opposing papers are found, note "no direct contradicting evidence found" — absence of
  opposition is itself informative.
- **Contribution type** (Resolution / Constraint / Replication / Negative constraint) must be
  stated in three locations: card header, knowledge map, and reflection. Consistency is required
  across all three.
- The reflection (Component 6) must follow the three-part structure: what was shown → what this
  rules out / does not rule out → what would be needed next. Parts must appear in order and may
  not be blended.
