---
name: experiment-triage
description: >
  Triage AutoDiscovery experiments for scientific rigor and mechanistic value. Use when the user
  wants to review, filter, or prioritize experiments from an AutoDiscovery run — phrases like
  "triage experiments", "find the good experiments", "filter for flaws", "which experiments are
  valid", "rank the hypotheses", "show me the best experiments from run X", "what can I present",
  "quality check autodiscovery". Takes a run ID as input. Also triggers when the user uploads or
  references JSON files containing fields like hypothesis, surprise, prior, posterior, analysis,
  review, code_output, experiment_plan — any AutoDiscovery JSON schema.
argument-hint: <runid>
user-invocable: true
---

# Experiment Triage

Given an AutoDiscovery run ID, evaluate every experiment for scientific validity and mechanistic
value. Produce a prioritized list of passing experiment IDs (ready for the experiment card skill)
and save results to disk.

---

## Step 1 — Load the Run

```bash
asta autodiscovery experiments <runid> --format json
```

Parse the JSON array. Each element has:

| Field | What it tells you |
|---|---|
| `experiment_id` | Node ID (e.g. `node_2_0`) — use this as the canonical ID |
| `id_in_run` | Human-readable index (1–N) |
| `hypothesis` | The scientific claim being tested |
| `experiment_plan` | `{objective, steps, deliverables}` |
| `analysis` | What the code actually found |
| `review` | AutoDiscovery's self-review of execution faithfulness |
| `code_output` | Raw stdout — per-subject unit counts, errors, warnings |
| `is_surprising` | Boolean from Bayesian scoring |
| `surprise` / `prior` / `posterior` | Bayesian belief shift |
| `status` | SUCCEEDED / FAILED / etc. |

---

## Step 2 — Apply Validity Filters

Assign each experiment one of three verdicts:

- **PASS** — no disqualifying flaws; ready for deeper analysis
- **FLAG** — one or more soft issues; findings are preliminary only
- **FAIL** — hard disqualifying flaw; exclude from primary results

Work through checks **in order**. Stop at the first FAIL.

---

### Check A — Execution Status

**FAIL** if `status != SUCCEEDED` or `code_output` contains error tracebacks or
"execution failed". **FAIL** if `analysis` is null or empty.

---

### Check B — Cross-Subject Reproducibility (hard requirement)

The inferential unit is **the subject**, not the neuron or trial. An effect is only considered
supported if confirmed across subjects — not just observed in one.

**Hard N rules:**

| N subjects | Verdict |
|---|---|
| N = 1 | **FAIL** — cannot generalize |
| N = 2 | **FAIL** — paired tests with N=2 are meaningless |
| N = 3 | **FLAG** — underpowered; acceptable only if effect is dramatic |
| N ≥ 4 | Proceed to next check |

**How to count subjects:** Scan `code_output` for lines matching `Processing Subject <ID>:`
and count unique IDs. Also check `analysis` for explicit N statements.

**Watch for hidden single-subject analyses.** Sometimes code runs on all 5 files but the
actual result comes from 1 mouse because only 1 subject had the required region/unit combination.

**FAIL** if any of the following appear in `code_output`, `analysis`, or `review`:
- "after filtering, 1 session remained" / "only subject X had sufficient units"
- "the session with the most units" / "best candidate session"
- Specific session ID mentioned as the sole source of the finding
- "could not be confirmed across subjects"

**FLAG** if subjects are highly unbalanced (one subject >60% of units or trials) without
per-subject statistics to compensate.

---

### Check C — Pseudo-Replication

**FAIL** if:
- Group-level hypothesis tested with N = number of neurons/units (not subjects) as the
  primary statistical sample size
- t-test or ANOVA run on neuron-level pooled data without subject-level aggregation or a
  mixed model with subject as random effect
- Degrees of freedom implausibly large relative to subject count (e.g., `t(843)` for a
  5-subject dataset)

**FLAG** if `experiment_plan.steps` does not mention subject-level aggregation, mixed models,
or per-subject statistics.

---

### Check D — Circular Analysis

**FAIL** if the readout dimension is defined using the same variable it is then used to predict.
The most common form: split data by an outcome variable (e.g., fast vs. slow RT trials) to
define an axis, then report that projection onto that axis predicts the outcome. This is
guaranteed to "work" regardless of biology.

**How to detect:** Look for patterns in `experiment_plan.steps` or `analysis` where:
- A condition split (Hit/FA, fast/slow, attend/ignore) is used to define an axis or subspace
- The same condition split is the target variable for decoding or regression
- No independent validation set or held-out data is mentioned

---

### Check E — Hypothesis-Level Redundancy

AutoDiscovery often generates 3–7 variants of the same idea (e.g., "MOs pre-stimulus state
predicts RT" tested with PLS, Ridge regression, Euclidean distance, fast/slow split).

**FLAG** if the hypothesis is substantially redundant with another experiment in the same run
that has a cleaner design or stronger result. When flagging redundancy, name the experiment ID
that supersedes it.

When multiple variants exist, keep only the cleanest version in the passing list. Presenting
multiple variants of the same finding destroys credibility with expert audiences.

---

### Check F — Unit Quality Filtering

**FLAG** if `code_output` or `analysis` shows no mention of quality filtering
(`default_qc`, `quality_metric`, `firing_rate threshold`, `presence_ratio`, or equivalent).

**FLAG** if any subject has suspiciously low unit counts (< 10 units for a region expected
to have many) without explanation — this often signals the hidden single-subject problem.

---

### Check G — Statistical Rigor

**FLAG** if any of the following:
- Multiple comparisons (> 2 tests) with no correction mentioned (Bonferroni, FDR/BH,
  permutation)
- Decoding or classification accuracy reported without cross-validation — high accuracy
  without a held-out test set is meaningless
- Class imbalance unaddressed: e.g., if 94% of trials are one class, a 90% accurate
  classifier is below chance at detecting the minority class
- p-values without effect sizes
- Non-significant result re-framed as partial support in `review`

**Note:** Null results are valid. A null result re-framed as support is a flaw.

---

### Check H — Plan–Hypothesis Alignment

**FLAG** if:
- `experiment_plan.objective` does not logically test the `hypothesis`
- Analysis performed differs substantially from `experiment_plan.steps`
- `review` notes the plan was not faithfully executed

---

### Check I — Minimum Mechanistic Testability

**FAIL** if:
- Hypothesis is purely descriptive ("region X will be active during Y")
- Hypothesis is trivially unfalsifiable ("X may play a role in Y")
- Experiment cannot distinguish the hypothesis from a null model

---

### Check J — Figure–Finding Consistency (only if figures are present)

If `code_output` contains figure paths (lines like `"Saved figure to ..."`, `"Figure saved:"`, or any `.png`/`.pdf` path), read each figure using the `Read` tool and visually inspect it.

**What to check:**

| Reported metric | What to look for in the figure |
|---|---|
| "significant increase / decrease" | Trajectory or bar must show a clear directional shift; error bars should not overlap substantially |
| "two populations are separable" | Scatter/PCA plot must show visible cluster separation, not complete overlap |
| R² or correlation value | Scatter plot tightness must be consistent with the stated magnitude (R²=0.85 → tight cloud; R²=0.2 → loose) |
| Decoding accuracy above chance | Learning curve or bar must visually exceed the chance line by a meaningful margin |
| "effect persists across subjects" | Per-subject traces or bars must show consistent direction across subjects, not just on average |
| Effect size / Cohen's d | Effect visible by eye must match the stated magnitude — large d with indistinguishable distributions is a red flag |
| Inflection point / transition trial | Zero-crossings in the trajectory must occur near the reported trial number; a crossing that appears 50+ trials off is a mismatch |
| Fit line or model prediction | The fitted curve must visually track the data — a flat or near-horizontal fit over a noisy cloud is a degenerate result even if a slope is reported |

**Verdict rules:**

- **FLAG** if the visual trajectory is ambiguous or weakly consistent with the reported metric (e.g., effect present but much smaller than described, or confined to 1–2 subjects)
- **FLAG** if error bars or per-subject spread suggest the effect could plausibly be noise, even if p < 0.05
- **FAIL** if the figure directly contradicts the reported metric (e.g., flat or reversed trajectory where an increase is claimed; complete overlap where separation is claimed)
- **Skip** if no figure paths are found in `code_output`, or if the path does not exist on disk

When flagging, quote the specific discrepancy: *"analysis reports R²=0.82 but scatter plot shows wide dispersion inconsistent with this value"*.

---

## Step 3 — Score Mechanistic Interpretability

For all **PASS** and **FLAG** experiments, score 1–5:

| Score | Description |
|---|---|
| **5** | Tests a specific causal mechanism — how a signal is computed, routed, or transformed. Could falsify a circuit-level or algorithmic theory. |
| **4** | Tests directional causality or functional specificity (e.g., "X drives Y under condition Z, not W"). |
| **3** | Tests whether a known computational construct (subspace, manifold, gain) has a specific property during a condition. |
| **2** | Tests a correlation or co-variation without mechanistic commitment. |
| **1** | Descriptive — characterizes what exists, not how it works. |

**High score signals (4–5):** "drives", "gates", "routes", "computes", "selects",
"suppresses", "transforms"; falsifiable by a specific null model; distinguishes two competing
mechanisms; findings would constrain a circuit model.

**Low score signals (1–2):** "correlates with", "is related to", "reflects"; findings equally
consistent with multiple mechanistic accounts; tests presence/absence rather than mechanism.

---

## Step 4 — Calibrate Novelty

For each PASS experiment, assign a novelty tier. Do not say "novel" for tier 3 or 4 — an
expert audience will notice and it undermines everything else.

| Tier | Description |
|---|---|
| **1** | Fills an explicitly flagged gap: a published review or paper stated "X has not been tested" and this tests X. |
| **2** | Quantifies a predicted but unmeasured effect: the framework predicted this, but nobody measured it in this circuit/task/species. |
| **3** | Confirms an existing framework in a new context. Frame as validation, not discovery. |
| **4** | Positive control — a textbook finding AutoDiscovery independently rediscovered. Frame as system validation only. |

---

## Step 5 — Common Failure Modes (Quick Reference)

Check for all of these before finalizing verdicts:

| Failure Mode | How to Detect | Example |
|---|---|---|
| Single-session analysis | Session ID in analysis, "best candidate" language | "Session 664851 had the most units" |
| Hidden single-subject | Code runs on all 5 but 1 survives filtering | "After filtering, 1 session remained" |
| Redundant hypothesis cluster | 3+ hypotheses testing same core claim | 5 variants of "MOs predicts RT" |
| Circular axis definition | Readout dimension defined using outcome variable | Fast/slow split → predict RT |
| High-D orthogonality artifact | Observed angle ≈ null mean, both ≈ 90° | "Indistinguishable from random" |
| Pooled-unit statistics | p-value from unit-level test, no subject summary | "p < 1e-9 across 380 units" |
| Missing cross-validation | Decoder accuracy without held-out test set | "LDA accuracy = 95%" with no CV |
| Class imbalance | High accuracy driven by base rate | 90% accuracy when 94% are one class |
| Region availability bias | Analysis limited to subjects with rare region combos | "3/5 subjects had CA1" |
| Ceiling/floor effect | 100% or 0% in a condition | 5-unit subject → 100% variance explained |
| Figure–metric mismatch | Visual trajectory contradicts reported statistic | Flat trace but analysis claims significant increase |

---

## Step 6 — Domain Context: Dynamic Routing Dataset

Apply this context when the run is on the Allen Institute Dynamic Routing dataset:

- **Pilot run: N = 5 subjects.** The AutoDiscovery runs used a 5-subject pilot. The full
  dataset has ~114 sessions and can be used to scale any finding. N=4 is acceptable for
  the pilot; N≤3 is underpowered even in the pilot. Do NOT frame N=5 as a hard dataset
  ceiling — frame it as a pilot constraint with a concrete scaling path.
- **Contribution type framing:** A passing result at N=5 is a **Constraint**. Note explicitly
  that it would upgrade to **Resolution** if replicated across the full ~114-session cohort.
- **Region availability:** Not all subjects have all regions. CA1 and ORB have limited coverage.
  Always verify per-subject region availability before accepting a cross-region result.
- **Known positive controls** (do not present as discoveries):
  - Attentional gain modulation in VIS during visual-attend blocks
  - Context decoding from MOs/ACA
  - Reaction time prediction from motor preparatory activity
- **Relevant theoretical frameworks** for mechanistic scoring:
  - Communication subspaces (Semedo et al. 2019)
  - Null/potent space (Kaufman et al. 2014)
  - Orthogonal coding (Mante et al. 2013; Elsayed et al. 2016)
  - Context-dependent computation (Mante et al. 2013)
- **Trial types:** Hit (correct go), Correct Reject (correct no-go), False Alarm (incorrect go),
  Miss (incorrect no-go).
- **Block transitions:** First ~10 trials after a context switch are "transition"; remaining
  are "steady-state". Analyses that mix these without separation are confounded.

---

## Step 7 — Output

### 7a. Display to User

**Passing experiments** (PASS, sorted by mechanistic score desc, then surprise desc):

```
experiment_id: node_2_0
id_in_run:     1
hypothesis:    <full hypothesis text>
mech_score:    5
novelty_tier:  2
verdict:       PASS
caveats:       none
surprise:      -0.690  (prior: 0.708 → posterior: 0.266)
finding:       <one sentence from analysis summarizing the key result>
```

**Full triage table** (all experiments):

```
# | experiment_id | Verdict | Mech | Flaws
--|---------------|---------|------|----------------------------------
1 | node_2_0      | PASS    |  5   | —
7 | node_3_5      | PASS    |  4   | —
51| node_8_1      | FLAG    |  5   | B: N=4 subjects (borderline)
3 | node_1_2      | FLAG    |  3   | G: no cross-validation
2 | node_1_0      | FAIL    |  —   | B: N=1 (single subject)
```

**Reject summary:** For each FAIL, quote the specific line from `code_output`, `analysis`, or
`review` that triggered the failure.

**Cross-finding narrative:** After individual assessments, check whether the PASS experiments
compose into a coherent mechanistic story. If they do, describe it — but only make claims the
data actually supports:
- "These findings are consistent with X" — OK (states a constraint)
- "These findings demonstrate X" — only if causal chain is established
- "These findings suggest a 3-stage architecture" — avoid (implies sequential causation that
  correlational analyses cannot establish)

---

### 7b. Save Artifacts

Create the output directory if it doesn't exist:

```bash
mkdir -p autodiscovery-runs/<runid>
```

Write two files — a machine-readable index and a human-readable report:

**`autodiscovery-runs/<runid>/triage.json`**

```json
{
  "run_id": "<runid>",
  "triage_date": "<YYYY-MM-DD>",
  "total_experiments": 70,
  "passing": [
    {
      "experiment_id": "node_2_0",
      "id_in_run": 1,
      "mechanistic_score": 5,
      "novelty_tier": 2,
      "hypothesis": "<full text>",
      "finding": "<one-sentence summary>",
      "surprise": -0.690,
      "prior": 0.708,
      "posterior": 0.266
    }
  ],
  "flagged": [
    {
      "experiment_id": "node_8_1",
      "id_in_run": 51,
      "mechanistic_score": 5,
      "caveats": ["N=4 subjects (borderline)"],
      "hypothesis": "<full text>"
    }
  ],
  "failed": [
    {
      "experiment_id": "node_1_0",
      "id_in_run": 2,
      "reason": "B: single subject",
      "evidence": "<quoted line from code_output or analysis>"
    }
  ]
}
```

**`autodiscovery-runs/<runid>/triage.md`**

A human-readable report with: run metadata, passing experiment details, full triage table,
reject summary, and cross-finding narrative. Use the display format from 7a.

---

### Loading Experiment IDs from the Artifact

The JSON is designed for easy programmatic loading:

```python
import json

with open("autodiscovery-runs/<runid>/triage.json") as f:
    triage = json.load(f)

# All passing experiment IDs
passing_ids = [e["experiment_id"] for e in triage["passing"]]

# Top experiments by mechanistic score
top = sorted(triage["passing"], key=lambda e: e["mechanistic_score"], reverse=True)
```

---

## Behavior Notes

- Process **all** experiments — a non-surprising null with a clean design is more valuable
  than a surprising result with pseudo-replication
- When in doubt between PASS and FLAG, choose FLAG
- Do not penalize null results — a well-executed rejection of a hypothesis is a valid finding
- If `code_output` is truncated or missing, note "insufficient output to verify" and FLAG
- If the run has > 30 experiments, process in batches of 15–20 and maintain a running tally
- Only one experiment from a redundancy cluster should appear in the passing list; the others
  go to FLAG with a note naming the superseding experiment
