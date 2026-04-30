# Experiment Card: node_4_27

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — The Communication Subspaces framework predicts context-dependent VIS-to-MOs alignment, but this effect has not been directly measured in this specific rodent circuit and attentional task.
**Contribution type:** Constraint
**Triage verdict:** PASS  |  Mechanistic score: 4/5

---

## 0. Dataset Context

Sessions: 664851, 668755, 713655, 742903, 759434 (5 subjects)
Regions: VIS (5–87 units/subject; subject 759434: 5 units, subject 742903: 20 units), MOs (137–437 units/subject)
Task: Visual/auditory context-switching task; mice attend to rewarded modality (visual or auditory) in interleaved steady-state blocks, licking in response to targets

---

## 1. Hypothesis

The alignment between visual cortex (VIS) population activity and the VIS-to-motor (MOs) communication subspace is significantly greater during visual-attend blocks compared to auditory-attend blocks, supporting the Communication Subspaces framework (routing via selective subspace alignment).

**Known limitations:** No triage caveats were loaded. However, code_output reveals subject 759434 had only 5 VIS units — the 5-component PLS subspace captures 100% of variance in both conditions for this subject (algorithmic saturation, not biology). VIS unit counts also vary substantially (5–87 units), which may affect PLS subspace reliability.

---

## 2. Literature Evidence

### Supporting

- **Semedo et al., 2019** *Cortical Areas Interact through a Communication Subspace* (Neuron) — V1-V2 interactions in macaques occur through a low-dimensional communication subspace distinct from the dominant within-area variance; RRR identifies this subspace as the theoretically preferred estimator. *(analogical-circuit)*

- **Weiss & Coen-Cagli, 2024** *Measuring Stimulus Information Transfer Between Neural Populations through the Communication Subspace* (bioRxiv) — Formal framework links context-dependent alignment between population covariance and the subspace projection direction to flexible routing and gating of stimulus information; a higher alignment in the relevant context is the predicted mechanism. *(analogical-circuit)*

- **Tafazoli, Bouchacourt et al., 2025** *Building compositional tasks with shared neural subspaces* (Nature) — In monkeys switching between tasks, sensory and motor information was represented in shared subspaces that were flexibly engaged in a task-specific manner; the sensory subspace transformed toward the motor subspace during task performance, providing the closest analogue to the predicted VIS→MOs alignment shift. *(analogical-circuit)*

- **Hajnal, Tran et al., 2024** *Shifts in attention drive context-dependent subspace encoding in anterior cingulate cortex in mice during decision making* (Nature Communications) — In the same visual/auditory attention-switching task in mice, ACC population activity exhibits context-dependent low-dimensional subspace encoding with suppression of the irrelevant modality representation; supports the idea that context-dependent subspace structure extends beyond V1/ACC to downstream motor regions. *(analogical-task)*

- **Rikhye, Gilra, Halassa, 2018** *Thalamic regulation of switching between cortical representations enables cognitive flexibility* (Nature Neuroscience) — In mice switching attention between visual and auditory cues, the mediodorsal thalamus enhances context-relevant and suppresses context-irrelevant PFC representations, consistent with a circuit-level mechanism that would gate VIS-to-MOs routing. *(analogical-task)*

- **Lazar et al., 2023** *Paying attention to natural scenes in area V1* (bioRxiv) — Attentional enhancement of stimulus decodability from macaque V1 is captured by a low-dimensional subspace aligned with attentional variance, supporting the subspace alignment hypothesis for sensory routing. *(analogical-circuit)*

- **Young, Shin, Guo, Jadhav, 2025** *Hippocampal-Prefrontal Communication Subspaces Align with Behavioral and Network Patterns in a Spatial Memory Task* (eNeuro) — Task-relevant behaviors align with CA1-PFC communication subspaces and are dynamically modulated by network state, confirming that communication subspace alignment is behaviorally meaningful across diverse circuits. *(analogical-task)*

### Opposing

- **Srinath, Ruff, Cohen, 2021** *Attention improves information flow between neuronal populations without changing the communication subspace* (bioRxiv) — In macaque MT→SC during spatial attention switching, attention increased inter-area communication efficacy WITHOUT changing subspace dimensionality or geometry, directly contradicting the routing-via-alignment prediction. This is the most direct challenge: the same class of experiment (attention + visuomotor circuit) found no subspace change. *(Comparability note: Different circuit — primate MT→SC vs. mouse VIS→MOs — and different attention type — spatial vs. modality switching. The opposing finding may be circuit-specific.)* *(analogical-circuit)*

- **Reynolds & Heeger, 2009** *The normalization model of attention* (Neuron) — A normalization/gain model fully accounts for the range of attentional effects on sensory neurons without requiring subspace geometry changes; serves as the primary mechanistic alternative. The VIS alignment difference across blocks could arise from differential gain on VIS units rather than structural subspace reconfiguration. *(analogical-circuit)*

- **Naumann, Keijser, Sprekeler, 2021** *Invariant neural subspaces maintained by feedback modulation* (bioRxiv) — Context-invariant representations can be achieved by slow, spatially diffuse feedback gain modulation that reorients neural activity manifolds at the population level; this predicts that observed alignment differences across blocks could reflect gain-driven manifold rotation rather than routing-specific subspace alignment. *(analogical-circuit)*

- **Liu, Sacks, Golub, 2025** *Accurate Identification of Communication Between Multiple Interacting Neural Populations* (ICML) — Standard RRR and PLS approaches cannot reliably disentangle inter-regional communication from unobserved-region inputs and local dynamics; MR-LFADS substantially outperforms these methods, suggesting that PLS-based alignment scores may conflate true communication with confounded signal. *(analogical-circuit)*

### Contextual

- **Semedo, Gokcen, Machens, Yu, 2020** *Statistical methods for dissecting interactions between brain areas* (Current Opinion in Neurobiology) — Reviews multivariate methods for inter-areal analysis and notes interpretational challenges; provides methodological context for RRR/PLS limitations.

- **Myers-Joseph, Wilmes et al., 2023** *Disinhibition by VIP interneurons is orthogonal to cross-modal attentional modulation in primary visual cortex* (Neuron) — In the same task, VIP-SOM disinhibition and attentional modulation operate via orthogonal mechanisms in V1, establishing local V1 circuit context for how attention modulates visual output. *(direct — same task, same V1 region)*

- **Takeda et al., 2018** *Dynamic laminar rerouting of inter-areal mnemonic signal by cognitive operations in primate temporal cortex* (Nature Communications) — Cognitive operations reroute inter-areal signals to different cortical laminae, establishing dynamic routing as a general cortical phenomenon.

- **Ebbesen et al., 2018** *More than Just a 'Motor': Recent Surprises from the Frontal Cortex* (Journal of Neuroscience) — Reviews evidence that rodent motor cortex (MOs) integrates sensory and contextual signals, establishing the anatomical plausibility of VIS→MOs routing.

- **Tauste Campo et al., 2014** *Task-driven intra- and interarea communications in primate cerebral cortex* (PNAS) — Task-driven directional correlations between sensory and motor areas vanish without decision-making demands, confirming that inter-areal communication geometry is task-contingent.

- **Wu & Pillow, 2025** *Reduced rank regression for neural communication: a tutorial for neuroscientists* (preprint) — Tutorial covering RRR extensions and new alignment metrics; relevant as methodological grounding for interpreting variance-explained as an alignment measure.

### Knowledge Map

**Known:**
- Cortical areas communicate via low-dimensional subspaces distinct from dominant within-area variance (Semedo et al. 2019; Young et al. 2025)
- Attentional context modulates population geometry in sensory cortex, with low-dimensional subspace alignment to task-relevant features (Lazar et al. 2023)
- In the same visual/auditory switching task in mice, ACC shows context-dependent subspace encoding (Hajnal et al. 2024)
- Thalamus gates cortical context-switching (Rikhye et al. 2018)
- Gain modulation fully explains a wide range of attentional effects without subspace change (Reynolds & Heeger 2009)

**Unknown / contested:**
- Whether VIS-to-MOs subspace alignment specifically reconfigures across visual vs. auditory contexts in mice has not been measured prior to this experiment
- Contested: Srinath et al. (2021) found no subspace geometry change in MT→SC during spatial attention — the present experiment is a direct test of whether this negative result generalizes to modality-switching in mice
- PLS/variance-explained metrics do not distinguish structural subspace reconfiguration from gain-driven manifold rotation (Naumann et al. 2021; Liu et al. 2025)
- The low VIS unit counts in subjects 759434 (5 units) and 742903 (20 units) introduce subspace estimation noise of unknown magnitude

**How this hypothesis sheds light:**
*Contribution type: Constraint*

The decision node: should future studies use PLS/RRR-based alignment as a proxy for context-dependent routing strength in the VIS→MOs circuit? The experiment directly addresses the gap identified by Srinath et al. (2021): their negative result in MT→SC for spatial attention leaves open whether a different circuit (VIS→MOs) or a different attentional manipulation (modality switching) would show the predicted alignment shift. The result here (significant alignment difference, p=0.0097, t=3.78, N=5) constrains this gap by reporting a positive finding. This is a Constraint rather than a Resolution because (1) PLS serves as a proxy for RRR and variance-explained does not isolate communication from confounded shared inputs; (2) one of five subjects (759434, 5 VIS units) shows algorithmic 100% alignment in both conditions, inflating consistency; and (3) the gain-modulation alternative cannot be ruled out without matched subspace geometry comparison across blocks. A positive result establishes that differential VIS engagement of the motor-predictive subspace is observable in this circuit — it does not establish that routing occurs through structural subspace reconfiguration. A negative result would have supported the Srinath et al. finding and weakened the routing-via-alignment interpretation for this circuit. What the experiment cannot resolve: whether the alignment difference is caused by genuine subspace geometry reconfiguration, by context-dependent gain changes that incidentally project more onto the PLS directions, or by the large between-subject heterogeneity in VIS unit counts.

**What the caveats affect:**
No formal triage caveats were loaded for this experiment. However, the code_output reveals a subject-level confound with material impact on interpretation: subject 759434 contributed alignment scores of 1.000 in both conditions (5 VIS units, algorithmic saturation of the PLS subspace). This subject's inclusion in the paired t-test means the significant p-value (0.0097) is partly driven by a subject whose condition difference is definitionally zero (contributing no information). If this subject is removed, N=4 and the test's power and p-value would differ. This is functionally equivalent to a triage caveat about small-N fragility. The contribution type remains Constraint rather than Resolution because replication with matched VIS unit counts across subjects (minimum 20–30 per subject) would be needed to reliably estimate the effect size.

---

## 3. Experimental Plan

**Objective:** Determine if the mapping of sensory information to motor regions relies on context-dependent geometric alignment of communication subspaces.

**Steps:**
1. Extract high-quality units from VIS and MOs for each subject.
2. Isolate steady-state trials (last 30 trials of a block) for visual and auditory blocks.
3. Compute stimulus-evoked spike counts (0 to 0.5s post-stimulus) for all steady-state trials.
4. Use Reduced Rank Regression (RRR) — implemented as PLS regression — to identify the VIS→MOs communication subspace exclusively using data from visual-attend steady-state trials.
5. Project VIS population activity from visual blocks and auditory blocks onto this visual-block VIS→MOs subspace.
6. Compute the variance explained (alignment) of the projected activity for both block types.
7. Perform a one-sided paired t-test across subjects to verify that alignment is significantly higher during visual blocks than auditory blocks.

**Deliverables:**
1. Dimensionality and variance explained metrics for the VIS→MOs subspace per subject.
2. Subspace alignment scores for visual vs. auditory blocks.
3. Statistical test results (paired t-test) validating the context-dependent subspace alignment.

---

## 4. Similar Analyses in the Literature

- **Semedo et al., 2019** (Neuron) — Method: RRR applied to V1-V2 population recordings in macaques to identify communication subspace. Match: identifies the predictive low-dimensional mapping from source to target population (same estimator class as PLS used here). Regions: different (V1→V2 in macaques vs. VIS→MOs in mice). Task: passive visual stimulation, not context-switching. Caveats: authors note that the RRR subspace is specific to the conditions used to estimate it, so estimating the subspace on visual-block data and evaluating alignment on auditory-block data (as in this experiment) is consistent with their approach.

- **Wu & Pillow, 2025** (preprint) — Method: RRR tutorial with new alignment metrics between communication axes and principal modes of activity. Match: directly relevant to the variance-explained alignment metric used in this experiment; the tutorial notes that alignment metrics are sensitive to estimation noise when unit counts are low — directly applicable to subjects with 5–20 VIS units.

- **Tafazoli, Bouchacourt et al., 2025** (Nature) — Method: Population subspace analysis (PCA/SVD on population activity) to identify shared sensory and motor subspaces during task switching in monkeys. Match: uses subspace projection to measure task-specific engagement of sensory→motor subspaces, same conceptual approach as this experiment. Regions: lateral PFC and motor cortex in primates. Task: compositional task switching. Caveats: richer behavioral design (3 tasks, within-session switching) allows cleaner disambiguation of task vs. attention effects.

- **Young, Shin, Guo, Jadhav, 2025** (eNeuro) — Method: RRR applied to CA1-PFC population recordings to identify communication subspace; behavior is used to score alignment. Match: same RRR estimator class and same alignment-to-behavior analysis. Regions: CA1→PFC in rats. Task: spatial memory. Caveats: single task context, no cross-context comparison.

- **Myers-Joseph et al., 2023** (Neuron) — Method: Population decoding and dimensionality analysis in V1 during cross-modal attention-switching task in mice. Match: same task as this experiment; measures how attention modulates V1 population geometry. Regions: V1 only (not inter-areal). Caveats: no communication subspace analysis — single area only.

---

## 5. Results and Findings

**From AutoDiscovery analysis (no conflict with review):**

The experiment successfully processed all 5 subjects. PLS regression was used as a proxy for RRR to identify the VIS-to-MOs communication subspace from visual-attend steady-state trials. VIS population activity from both visual and auditory blocks was then projected onto this subspace, and variance explained (alignment) was computed for each.

**Subject-level results:**
| Subject | VIS units | MOs units | Align (VIS blocks) | Align (AUD blocks) |
|---------|-----------|-----------|--------------------|--------------------|
| 664851  | 87        | 137       | 0.5616             | 0.4796             |
| 742903  | 20        | 437       | 0.6623             | 0.5982             |
| 668755  | 132       | 241       | 0.4209             | 0.3222             |
| 759434  | 5         | 147       | 1.0000             | 1.0000             |
| 713655  | 29        | 188       | 0.5747             | 0.4828             |

In 4 of 5 subjects, alignment was clearly higher during visual-attend blocks. Subject 759434 (5 VIS units) showed 100% alignment in both conditions — a mathematically expected result for a 5-component PLS spanning the full 5-dimensional space; this subject contributes no discriminating information to the test.

**Group result:** One-sided paired t-test (VIS alignment > AUD alignment): t = 3.7799, p = 0.0097. The null hypothesis is rejected at α = 0.05.

**Both analysis and review agree:** The findings support the Communication Subspaces hypothesis. Review notes: "The results provide strong evidence for the hypothesis. The findings support the Communication Subspaces framework, demonstrating that the flow of sensory information from the visual cortex to downstream motor regions relies on context-dependent geometric alignment." Review explicitly identifies the 759434 subject issue as expected and not invalidating the test.

*(No conflict between analysis and review fields.)*

---

## 6. Reflection

**What was shown:**
[Verdict]: This result is consistent with the hypothesis that VIS population activity aligns preferentially with the VIS-to-MOs communication subspace during visual-attend blocks, but does not confirm routing-via-alignment as the mechanism.
[Effect direction and size]: VIS alignment to the motor-predictive subspace was higher during visual-attend blocks than auditory-attend blocks in 4 of 5 subjects, with a mean difference of approximately 0.07–0.09 alignment units across the informative subjects.
[Key statistic]: prior 0.708 → posterior 0.891, N=5 subjects, one-sided paired t-test t=3.7799, p=0.0097; one subject (759434, 5 VIS units) contributed alignment=1.000 in both conditions and is uninformative.
[Replication]: Effect was consistent across 4 of 5 informative subjects; subject 759434 showed algorithmic saturation (100% alignment in both conditions) due to only 5 VIS units and should be considered a data quality exclusion rather than biological replication.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that the alignment of VIS population activity to the VIS-to-MOs PLS communication subspace does not differ between visual-attend and auditory-attend blocks. This experiment rejected the null (p = 0.0097, N = 5, one-sided paired t-test).
[Power note]: Given N=5 (with one subject contributing zero discriminating information, effectively N=4), this test had unknown power to detect the predicted effect size — no prior effect size estimate for this specific circuit and task existed before this experiment. Rejection of the null at p=0.0097 with N=5 is consistent with a large effect size (t=3.78 at df=4 corresponds to Cohen's d ≈ 1.69), but this estimate is unreliable at small N and may be inflated by the high-leverage subjects (subject 664851: 87 VIS units, driving much of the effect). Failure to reject would not have been informative given insufficient power.

**What this rules out:**
[Rules out]: This result rules out the possibility that VIS population activity is completely context-invariant in its alignment to the motor-predictive dimensions — even in an auditory context, VIS activity retains some alignment, but the visual-context alignment is systematically higher across the informative subjects.
[Does not rule out]: This result does not rule out that the alignment difference is caused by context-dependent gain modulation on VIS neurons (which would incidentally project more onto the PLS subspace during visual blocks) rather than structural subspace reconfiguration, because variance-explained alignment cannot distinguish these two mechanisms and no control for gain changes (e.g., matched single-unit firing rate comparison) was performed.

**What would be needed next:**
[One experiment]: Re-run the same PLS alignment analysis with a minimum of 30 VIS units per subject (N ≥ 8 subjects), and add a parallel analysis comparing VIS population variance and mean firing rates across blocks to explicitly test whether the alignment difference is explained by overall gain changes rather than subspace geometry.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by (1) providing adequate statistical power to detect the predicted effect size reliably, (2) ruling out the gain-modulation alternative, and (3) removing the algorithmic saturation issue that currently makes one subject uninformative; together these steps would allow the finding to be interpreted as evidence for routing-via-alignment rather than routing-via-gain.
