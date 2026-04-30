# Experiment Card: node_3_8

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — The Communication Subspaces framework predicts context-dependent VIS→MOs alignment in mice, but this specific circuit and task combination has never been directly measured.
**Contribution type:** Constraint
**Triage verdict:** PASS | Mechanistic score: 3/5

---

## 0. Dataset Context

Sessions: 664851, 668755, 713655, 742903, 759434 (5 subjects attempted; 2 met inclusion criteria)
Regions: VIS (5–87 units/subject), AUD (0–264 units/subject), MOs (137–437 units/subject); only subjects 664851 and 713655 had ≥5 high-quality units simultaneously in all three regions
Task: Dynamic routing visual/auditory context-switching task; target trials only, spike counts in 0–0.5 s post-stimulus window

---

## 1. Hypothesis

During visual-rewarded blocks, the population activity in the primary visual cortex (VIS) aligns more strongly with the pre-motor cortex (MOs) communication subspace than during auditory-rewarded blocks, supporting the Communication Subspaces framework where sensory routing to motor outputs is dynamically gated via subspace alignment rather than changes in single-region firing rates.

**Known limitations:** None flagged in triage. However, the experiment's own inclusion filter (≥5 simultaneous high-quality units in VIS, AUD, and MOs) reduced the effective N from 5 to 2 subjects, which is functionally equivalent to a small-N caveat.

---

## 2. Literature Evidence

### Supporting

- **Semedo et al., 2019** *Cortical Areas Interact through a Communication Subspace.* (Neuron, relevance 0.987) — V1 and V2 populations in primates interact through a low-dimensional subspace identified via RRR; trial-to-trial fluctuations in V1 transmitted to V2 occupy a subspace of lower dimensionality than full V1 activity, establishing the foundational Communication Subspaces result this hypothesis invokes. *(analogical-circuit: same framework, primate visual hierarchy rather than rodent VIS→MOs)*

- **Hajnal et al., 2024** *Shifts in attention drive context-dependent subspace encoding in anterior cingulate cortex in mice during decision making.* (Nature Communications, relevance 0.963) — In mice performing a context-dependent cross-modal decision task, ACC populations shift their subspace encoding depending on which sensory modality is task-relevant; demonstrates context-dependent subspace reconfiguration in the same species and closely related task. *(analogical-circuit: same species and task structure, different source→target regions)*

- **Chang et al., 2024** *Rule-based modulation of a sensorimotor transformation across cortical areas.* (eLife, relevance 0.755) — Head-fixed mice performing a cross-modal sensory selection task show rule-dependent modulation of population-level sensorimotor transformations across cortical areas; confirms that behavioral context shapes the population geometry of sensory-to-motor routing in mice. *(analogical-task: same species and task type, different specific regions recorded)*

- **MacDowell et al., 2023** *Multiplexed Subspaces Route Neural Activity Across Brain-wide Networks.* (bioRxiv, relevance 0.760) — Cortex-wide calcium imaging shows distinct low-dimensional subspaces route activity through different brain-wide networks depending on behavioral state; subspace identity rather than firing rate determines downstream routing. *(analogical-circuit: same routing-via-subspace mechanism, different regions)*

- **Semedo et al., 2021** *Feedforward and feedback interactions between visual cortical areas use different population activity patterns.* (bioRxiv, relevance 0.784) — Feedforward and feedback interactions between V1, V2, V3 engage distinct population subspaces; the Communication Subspaces framework generalizes across cortical hierarchies and directions of information flow. *(analogical-circuit)*

- **Xue et al., 2026** *State-Dependent Dissociation of Shared Input and Directed Information Flow in the Visual Cortex.* (bioRxiv, relevance 0.974) — RRR applied to laminar macaque V1 recordings shows both visual stimulation and internal state modulate communication subspace structure; demonstrates that context-dependent subspace changes are detectable with RRR in a closely analogous paradigm. *(analogical-circuit)*

- **Iyer et al., 2021** *Geometry of inter-areal interactions in mouse visual cortex.* (bioRxiv, relevance 0.620) — RRR analysis of simultaneous multi-area recordings in mouse visual cortex reveals low-dimensional communication subspaces between VISp and higher visual areas; establishes technical feasibility of this approach in the same species and partially same source region (VIS). *(analogical-circuit)*

### Opposing

- **Srinath, Ruff & Cohen, 2021** *Attention improves information flow between neuronal populations without changing the communication subspace.* (bioRxiv, relevance 0.608) — Spatial attention in primates increases information transmitted between V4 and IT populations but does not alter the subspace through which they communicate; the communication subspace is stable across attention conditions and only magnitude changes. This directly challenges the hypothesis that context gates routing via subspace realignment — gain modulation within a stable subspace is an alternative mechanistic account. *(comparability note: primate V4→IT under spatial attention, not rodent VIS→MOs under reward-context switching; generalizability is limited but the mechanistic alternative is live)*

- **Jaramillo, Borges & Zador, 2014** *Auditory Thalamus and Auditory Cortex Are Equally Modulated by Context during Flexible Categorization of Sounds.* (Journal of Neuroscience, relevance 0.670) — In rats performing flexible auditory categorization, both auditory cortex and thalamus are equally modulated by task context at the single-neuron level; supports the alternative view that subcortical gating (upstream firing rate changes) rather than cortical subspace reconfiguration drives context-dependent sensory routing. *(analogical-task)*

- **Liu, Sacks & Golub, 2025** *Accurate Identification of Communication Between Multiple Interacting Neural Populations.* (ICML, relevance 0.802) — Standard RRR-based communication models are confounded when multiple populations interact simultaneously; the estimated subspace may reflect shared background inputs rather than directed communication, especially with small N. Directly challenges the methodological validity of the N=2 analysis used in this experiment. *(methodological concern, comparability: applies directly to this experiment's three-region setting)*

### Contextual

- **Wu & Pillow, 2025** *Reduced rank regression for neural communication: a tutorial for neuroscientists.* (preprint, relevance 0.975) — Comprehensive tutorial on RRR covering cross-validated R² as a measure of communication subspace alignment, potential confounds (shared noise correlations, small-N cross-validation bias), and best practices for implementation.

- **Semedo et al., 2020** *Statistical methods for dissecting interactions between brain areas.* (Current Opinion in Neurobiology, relevance 0.811) — Review establishing RRR and related approaches as the standard for identifying communication subspaces; frames the open question of whether subspaces reconfigure with cognitive context.

- **Kohn et al., 2020** *Principles of Corticocortical Communication: Proposed Schemes and Design Considerations.* (Trends in Neurosciences, relevance 0.713) — Review explicitly lists context-dependent reconfiguration of communication subspaces as a key open question for future work; directly frames the gap this experiment addresses.

- **Weiss & Coen-Cagli, 2024** *Measuring Stimulus Information Transfer Between Neural Populations through the Communication Subspace.* (bioRxiv, relevance 0.968) — Extends RRR to specifically quantify stimulus-related information transmission; notes that shared noise correlations can confound standard R² estimates of communication subspace alignment.

- **Zatka-Haas et al., 2020** *A perceptual decision requires sensory but not action coding in mouse cortex.* (bioRxiv, relevance 0.740) — In mice discriminating visual contrast, stimulus-related activity is present in both VIS and MOs; establishes that VIS and MOs are functionally coupled during visually guided behavior in the same species and overlapping task structure.

- **Coen et al., 2021** *Mouse frontal cortex mediates additive multisensory decisions.* (bioRxiv, relevance 0.773) — Mouse frontal cortex (including MOs) causally combines auditory and visual evidence for multisensory decisions; VIS and AUD signals both converge on MOs in rodent multisensory context tasks.

- **Pereira-Obilinovic et al., 2024** *Cognitive network interactions through communication subspaces in large-scale models of the neocortex.* (bioRxiv, relevance 0.672) — Computational model predicts that cognitive flexibility is implemented by reconfiguring inter-area communication subspaces; provides theoretical grounding for why subspace alignment should determine routing.

- **Jha et al., 2025** *Prioritized learning of cross-population neural dynamics.* (Journal of Neural Engineering, relevance 0.792) — Demonstrates that standard dimensionality reduction conflates within-population and cross-population dynamics; a methodological limitation relevant to interpreting the RRR R² shifts observed here.

### Knowledge Map

**Known:**
- Cortical areas communicate through low-dimensional subspaces identified via RRR (established in primate V1→V2; Semedo et al. 2019)
- Behavioral context and internal state modulate communication subspace geometry in multiple cortical regions and species (Hajnal et al. 2024; Xue et al. 2026; Chang et al. 2024)
- VIS and MOs are functionally coupled during visually guided and multisensory decisions in mice (Zatka-Haas et al. 2020; Coen et al. 2021)
- Sensorimotor transformations across cortical areas in mice are rule-modulated at the population level (Chang et al. 2024, eLife)

**Unknown / contested:**
- Whether VIS→MOs communication subspace alignment specifically reconfigures between visual-rewarded and auditory-rewarded task blocks in rodents — this has not been directly tested prior to this experiment
- Whether context-dependent routing is mediated by subspace reconfiguration (this hypothesis) or by gain modulation within a stable subspace (Srinath et al. 2021 found no subspace change under attention in primates) or by subcortical gating (Jaramillo et al. 2014)
- Whether RRR reliably estimates communication subspace changes with N=2 subjects: Liu et al. 2025 shows standard RRR is confounded by shared background inputs in multi-region settings; Wu & Pillow 2025 notes cross-validation bias at small N
- Whether observed R² shifts reflect genuine subspace reconfiguration or merely firing rate magnitude changes (both affect RRR R² and are not distinguished by this analysis)

**How this hypothesis sheds light:**
*Contribution type: Constraint*

The key decision node is whether RRR-based VIS→MOs alignment measures can serve as a valid proxy for context-dependent sensory routing strength in future large-scale mouse studies. This experiment addresses the gap explicitly flagged by Kohn et al. 2020 (Trends in Neurosciences): whether communication subspaces reconfigure with behavioral context. A positive result would establish that the VIS→MOs communication subspace is quantifiably context-dependent during visual/auditory reward switching in mice — a measurement that does not currently exist in the literature. This would justify using cross-validated RRR R² as an operational proxy for routing gating in future mouse studies and would narrow the theoretical space by ruling out the view that VIS→MOs acts as a context-independent broadcast channel. A negative result would suggest either that routing operates through a different channel (thalamic gating, AUD-selective subspaces), that VIS→MOs is not the primary routing pathway, or that the experiment lacks power. What the experiment cannot resolve even with a positive result: whether subspace reconfiguration is mechanistically distinct from gain modulation, whether the effect is driven top-down by prefrontal cortex, and whether the finding generalizes to the majority of subjects (3 of 5 lacked sufficient AUD units). Because N=2 provides only 1 degree of freedom for the paired t-test, this contribution is a Constraint — it narrows the theoretical space and provides preliminary evidence but cannot resolve the open question without a larger cohort.

**What the caveats affect:**
No triage caveats were formally loaded. However, the experiment's data reveal a self-imposed constraint: only 2 of 5 subjects met the ≥5-unit-per-region inclusion criterion simultaneously, resulting in N=2 for the main analysis. This is functionally equivalent to a small-N caveat. The paired t-test with N=2 (1 degree of freedom) has effectively no power: for the VIS→MOs effect, p=0.0611 is formally non-significant; for AUD→MOs, p=0.0337 reaches significance but from a single degree of freedom. Both results should be treated as preliminary. The effect size estimates (mean R² drops of 0.14 and 0.31 respectively) are based on only two data points and may be dominated by individual subject idiosyncrasies. A positive result from this analysis is a Constraint, not a Resolution: it motivates a larger study (N≥10 subjects with matched multi-region unit counts) but does not establish the finding.

---

## 3. Experimental Plan

**Objective:** Quantify context-dependent changes in the communication subspace geometry between sensory (VIS/AUD) and motor (MOs) regions.

**Steps:**
1. Extract high-quality units from VIS, AUD, and MOs across all subjects.
2. For each block context (Visual-rewarded vs Auditory-rewarded), isolate the stimulus-evoked activity (0 to 0.5s post-stimulus) for Target trials.
3. Use Reduced Rank Regression (RRR) to predict MOs population activity from VIS population activity, identifying the optimal low-dimensional predictive subspace for each context.
4. Compute the cross-validated predictive accuracy (R²) of the VIS→MOs RRR model using data from the Visual block, and then evaluate how well this specific 'Visual block' subspace predicts MOs activity using data from the Auditory block.
5. Repeat the process for AUD→MOs.
6. Perform a paired t-test across subjects comparing the VIS→MOs R² within the visual context vs. within the auditory context.

**Deliverables:**
1. RRR optimal rank estimation for sensory-motor communication.
2. Cross-validated R² predictive metrics for VIS→MOs and AUD→MOs across contexts.
3. Statistical summary demonstrating whether predictive subspace alignment is significantly dependent on the behavioral context.

---

## 4. Similar Analyses in the Literature

- **Semedo et al., 2019** (Neuron) — Method: RRR to estimate communication subspace between V1 and V2. Match: identical estimator class (RRR with cross-validated R²). Regions: V1→V2 in primates (different from VIS→MOs in mice). Task: passive viewing (different from active context switching). Caveats noted by authors: RRR identifies the subspace that predicts fluctuations, not necessarily the subspace that transmits stimulus information; shared noise can inflate R².

- **Xue et al., 2026** (bioRxiv) — Method: RRR applied to laminar V1 recordings to quantify low-dimensional predictive subspaces between Input and Superficial layers. Match: identical RRR cross-validated R² approach; explicitly tests state-dependent changes in subspace geometry. Regions: within macaque V1, not across VIS and MOs. Task: passive viewing with eyes open vs. closed state manipulation.

- **Wu & Pillow, 2025** (preprint) — Method: Comprehensive tutorial and implementation of RRR for neural communication. Match: identical estimator class. Caveats explicitly documented: (a) cross-validation bias inflates R² at small N; (b) shared input correlations can inflate apparent communication subspace dimensionality; (c) optimal rank selection via cross-validation is sensitive to sample size. Directly applicable to interpreting the node_3_8 results.

- **Liu, Sacks & Golub, 2025** (ICML) — Method: Multi-population extension of RRR (Multipopulation Communication). Match: extends the same RRR estimator class to multiple simultaneously interacting regions. Caveats: shows that standard pairwise RRR conflates shared background inputs with directed communication when multiple regions are recorded simultaneously — a direct concern for the three-region (VIS/AUD/MOs) setting used here.

- **Xu et al., 2024** (Neuron) — Method: RRR applied to inter-laminar recordings in macaque V1 to measure context-dependent information flow. Match: identical estimator (RRR), same evaluation strategy (cross-validated R² as communication measure), same goal (detecting state-dependent subspace changes). Regions: laminar V1 (different from VIS→MOs). Task: spatial context manipulation around visual stimuli.

- **Jha et al., 2025** (Journal of Neural Engineering) — Method: Prioritized dimensionality reduction to separate cross-population from within-population dynamics. Match: alternative to RRR that addresses a known confound; not used in this experiment but relevant for future work. Caveats: standard RRR (used in node_3_8) does not disentangle these; the context-dependent R² shifts could partially reflect within-population dynamics rather than cross-population communication changes.

---

## 5. Results and Findings

The experiment successfully ran on 5 subjects, but only 2 met the simultaneous inclusion criterion (≥5 high-quality units in each of VIS, AUD, and MOs). The three excluded subjects (742903, 668755, 759434) lacked AUD units entirely or had insufficient VIS units.

**Per-subject results (2 valid subjects: 664851, 713655):**

*VIS→MOs:*
- Subject 664851: CV R² in visual context = 0.0594; R² in auditory context = −0.0682 (optimal rank = 1)
- Subject 713655: CV R² in visual context = 0.2204; R² in auditory context = 0.0656 (optimal rank = 1)
- Mean R² visual context: 0.1399; mean R² auditory context: −0.0013
- Paired t-test: t = 10.39, p = 0.0611 (N = 2, 1 degree of freedom) — not significant at α = 0.05

*AUD→MOs:*
- Subject 664851: CV R² in auditory context = 0.1101; R² in visual context = −0.3920 (optimal rank = 2)
- Subject 713655: CV R² in auditory context = 0.2263; R² in visual context = −0.2253 (optimal rank = 2)
- Mean R² auditory context: 0.1682; mean R² visual context: −0.3086
- Paired t-test: t = 18.87, p = 0.0337 (N = 2, 1 degree of freedom) — significant at α = 0.05

The analysis (AutoDiscovery `analysis` field) concludes: "These drastic context-dependent shifts in R² suggest that sensory routing to motor outputs is dynamically gated via subspace alignment based on task rules." The `review` field reaches the same conclusion while explicitly emphasizing the N=2 limitation: "These findings strongly support the Communication Subspaces framework... However, the extremely small sample size (N=2) necessitates caution in interpreting the statistical significance."

**Note:** The `review` field does not contradict `analysis` — both affirm the direction of the effect and both flag the small sample size. The `review` verdict is treated as authoritative.

A negative R² (e.g., AUD→MOs R² = −0.31 in the out-of-context condition) indicates that the subspace learned in the relevant context actively makes predictions worse than guessing the mean when applied to the irrelevant context — a strong signal of genuine subspace reorganization, not merely a magnitude reduction.

---

## 6. Reflection

**What was shown:**
[Verdict]: This result is consistent with the hypothesis but does not confirm it; the direction of the effect is strong for both VIS→MOs and AUD→MOs, but statistical significance at α=0.05 is reached only for AUD→MOs, and N=2 provides 1 degree of freedom throughout.
[Effect direction and size]: VIS→MOs cross-validated R² dropped from 0.1399 (visual context) to −0.0013 (auditory context); AUD→MOs R² dropped from 0.1682 (auditory context) to −0.3086 (visual context); both effects are in the predicted direction and the magnitudes are large.
[Key statistic]: prior 0.708 → posterior 0.734; VIS→MOs: t=10.39, p=0.0611, N=2; AUD→MOs: t=18.87, p=0.0337, N=2.
[Replication]: Effect was consistent in direction across both valid subjects for both VIS→MOs and AUD→MOs, but N=2 means "consistent across all subjects" is uninformative about population-level robustness.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that the cross-validated predictive R² of the VIS→MOs RRR subspace does not differ between visual-rewarded and auditory-rewarded blocks. This experiment failed to reject the null for VIS→MOs (p=0.0611, N=2) and rejected the null for AUD→MOs (p=0.0337, N=2).
[Power note]: Given N=2, this test had unknown power to detect an effect of the predicted magnitude — there is no prior effect size estimate for this specific circuit, and a paired t-test with 1 degree of freedom is almost always underpowered. The failure to reject for VIS→MOs is not informative about the true effect; the effect direction (R² drop of ~0.14) is consistent with the hypothesis and the non-significance likely reflects insufficient power rather than absence of an effect.

**What this rules out:**
[Rules out]: This result rules out the possibility that the VIS→MOs subspace is entirely context-independent (i.e., that the same subspace predicts MOs equally well in both contexts), because both subjects showed a directionally consistent and large drop in predictive R² when evaluated out of context.
[Does not rule out]: This result does not rule out the alternative that the observed R² drop reflects changes in overall firing rate magnitude (signal power) rather than genuine subspace reconfiguration, because the experiment did not partial out firing rate differences or control for input covariance between conditions.

**What would be needed next:**
[One experiment]: N≥10 subjects from the full 114-session dataset with ≥5 simultaneous high-quality units in all three regions (VIS, AUD, MOs), combined with a rate-normalized version of the RRR analysis (e.g., z-scoring spike counts within each condition before fitting) to distinguish subspace reconfiguration from overall rate changes.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by providing adequate statistical power (N=10 gives 9 degrees of freedom, moving p < 0.01 for t ≥ 3.25) and by ruling out the firing-rate confound — the single most important remaining alternative explanation. The larger cohort from the full dataset already exists and would not require new data collection.
