# Experiment Card: node_4_29

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — The communication subspace framework has been demonstrated between V1-V2 and in premotor-motor circuits, but whether VIS-to-PFC subspace geometry reconfigures across reward-context blocks (visual vs. auditory) in mice has not been directly measured; the framework predicts this but the specific circuit and task combination is unmeasured.
**Contribution type:** Constraint
**Triage verdict:** PASS | Mechanistic score: 4/5

---

## 0. Dataset Context

Sessions: 664851, 742903, 668755, 759434, 713655 (5 subjects)
Regions: VIS (VISp, VISpm, VISam, VISal, VISrl, VISli) 5–132 units/subject; PFC (ACA, PL, ILA, ORB, ACAd, ACAv, ORBvl, ORBl, ORBm) 7–727 units/subject
Task: Visual/auditory context-switching, licking response (rewarded modality alternates between vis and aud blocks); post-stimulus window 0–0.5 s used for spike counts

---

## 1. Hypothesis

Sensory information is routed to prefrontal cortex (PFC) through context-specific orthogonal subspaces. A Reduced-Rank Regression (RRR) model trained to predict PFC activity from VIS activity during Visual-rewarded blocks will show a significant drop in cross-validated R^2 when applied to VIS-to-PFC activity during Auditory-rewarded blocks, supporting the Communication Subspaces framework.

**Known limitations:** No triage caveats flagged. Note from data: Subject 759434 had only 5 VIS units (minimal threshold) and Subject 713655 had only 7 PFC units — these outlier unit counts likely inflate per-subject variability and reduce power for the paired t-test.

---

## 2. Literature Evidence

### Supporting

- **[Semedo et al., 2019]** *Cortical Areas Interact through a Communication Subspace.* (Neuron) — Population interactions between V1 and V2 in primates are mediated through a low-dimensional subspace identified by RRR, where a small subset of V1 dimensions preferentially predicts V2 activity — establishing the foundational framework this hypothesis invokes.

- **[MacDowell et al., 2023]** *Multiplexed Subspaces Route Neural Activity Across Brain-wide Networks* (bioRxiv / Nature Neuroscience 2024) — Cortex-wide calcium imaging in mice shows that distinct subspaces multiplex and route activity across different brain-wide networks during different cognitive states, directly supporting the idea that subspace geometry gates inter-areal communication.

- **[Bayones et al., 2024]** *Orthogonality of sensory and contextual categorical dynamics embedded in a continuum of responses from the second somatosensory cortex* (bioRxiv) — In primate somatosensory cortex, sensory and contextual categorical signals occupy orthogonal subspaces, providing empirical evidence that orthogonal subspace segregation of different information streams occurs in sensory cortex during task-relevant contexts.

- **[Semedo et al., 2021]** *Feedforward and feedback interactions between visual cortical areas use different population activity patterns* (bioRxiv / Nature Communications) — Feedforward and feedback signals between V1 and V2 operate through distinct, non-overlapping population subspaces, implying that directional inter-areal routing is separated geometrically — foundational support for context-specific subspace routing.

- **[Hajnal et al., 2024]** *Shifts in attention drive context-dependent subspace encoding in anterior cingulate cortex in mice during decision making* (Nature Communications) — In mice, attention shifts reconfigure population subspace encoding in ACC in a context-dependent manner — the closest published analog to the predicted VIS-to-PFC subspace reconfiguration across reward context blocks.

- **[Tang et al., 2020]** *Minimally dependent activity subspaces for working memory and motor preparation in the lateral prefrontal cortex* (eLife) — In primate lateral PFC, working memory and motor preparation signals occupy minimally dependent (near-orthogonal) subspaces, supporting the feasibility of orthogonal subspace segregation in PFC.

- **[Pereira-Obilinovic et al., 2024]** *Cognitive network interactions through communication subspaces in large-scale models of the neocortex* (bioRxiv) — Large-scale cortical network models show that communication subspaces between areas reconfigure during different cognitive states, providing theoretical support for context-dependent subspace reconfiguration.

- **[Liu & Wang, 2023]** *Flexible gating between subspaces in a neural network model of internally guided task switching* (bioRxiv) — RNN models trained on internally-guided task switching show that flexible behavior requires gating between distinct subspaces implemented by context signals — theoretical/computational support for the subspace routing mechanism.

- **[Javadzadeh & Hofer, 2021/2022]** *Dynamic causal communication channels between neocortical areas* (Neuron) — Inter-areal communication channels between neocortical areas are dynamic and change between behavioral contexts — providing empirical evidence that communication subspace geometry is not fixed.

### Opposing

- **[Srinath, Ruff & Cohen, 2021]** *Attention improves information flow between neuronal populations without changing the communication subspace* (Current Biology) — Spatial attention modulates the gain of information flow between MT and SC without altering subspace geometry — a direct counter to the hypothesis that context changes subspace structure, suggesting gain modulation within a stable subspace can explain context-dependent routing. *(analogical-circuit: different regions, different species)*

- **[Naumann, Keijser & Sprekeler, 2021/2022]** *Invariant neural subspaces maintained by feedback modulation* (eLife) — Context invariance in sensory representations can be achieved through feedback modulation that maintains invariant subspaces, rather than through orthogonal routing — suggesting subspace stability may be the functional norm rather than the exception. *(analogical-circuit)*

- **[Mante et al., 2013]** *Context-dependent computation by recurrent dynamics in prefrontal cortex* (Nature) — Context-dependent selection of sensory inputs in PFC is implemented through recurrent dynamics within PFC, not reconfiguration of the afferent communication channel — the PFC internal dynamics, not input routing geometry, is the computational locus. *(analogical-circuit)*

- **[Wu & Pillow, 2025]** *Reduced rank regression for neural communication: a tutorial for neuroscientists* (arXiv) — RRR cross-context generalization can conflate genuine subspace reconfiguration with differences in signal-to-noise across conditions; discusses rank selection confounds and noise correlation limitations that limit interpretation of cross-context R^2 drops. *(methodological)*

### Contextual

- **[Kohn et al., 2020]** *Principles of Corticocortical Communication: Proposed Schemes and Design Considerations.* (Trends in Neurosciences) — Review that explicitly identifies context-dependent modulation of communication subspaces as an open question for future work; establishes the theoretical landscape.

- **[Weiss & Coen-Cagli, 2024]** *Measuring Stimulus Information Transfer Between Neural Populations through the Communication Subspace* (bioRxiv) — Proposes an RRR extension for stimulus information transfer; highlights that shared noise correlations and stimulus-independent variability can confound standard R^2-based communication subspace measures.

- **[Iyer et al., 2021]** *Geometry of inter-areal interactions in mouse visual cortex* (bioRxiv) — Inter-areal interaction geometry in mouse visual cortex is dynamic; same species and visual cortex regions as this experiment — closest contextual precedent.

- **[Semedo et al., 2020]** *Statistical methods for dissecting interactions between brain areas* (Current Opinion in Neurobiology) — Review of dimensionality-reduction methods for inter-areal communication including RRR; notes that identifying directional communication requires careful control for shared noise and non-target-area signals.

- **[Gokcen et al., 2021/2022]** *Disentangling the flow of signals between populations of neurons* (Nature Computational Science) — Proposes delayed linear systems approach to disentangle bidirectional signals; relevant because the RRR approach used here does not control for feedback from PFC to VIS, which could confound the cross-context R^2 comparison.

- **[Ebrahimi et al., 2022]** *Emergent reliability in sensory cortical coding and inter-area communication* (Nature) — In mice performing visual discrimination, population-level coding and inter-area communication reliability is high despite single-neuron variability — contextualizes the expected noisiness of single-subject VIS-to-PFC R^2 estimates.

- **[Liu, Sacks & Golub, 2025]** *Accurate Identification of Communication Between Multiple Interacting Neural Populations* (ICML) — Standard RRR can fail to correctly disentangle sources when multiple interacting populations are present — relevant because PFC receives inputs from many areas beyond VIS, potentially inflating or diluting the estimated communication subspace.

- **[Perich et al., 2017/2018]** *A neural population mechanism for rapid learning* (Neuron) — Rapid behavioral adaptation involves rotations within a stable manifold rather than changes to the manifold itself — a precedent suggesting flexible behavior need not require subspace reconfiguration.

- **[Soldado-Magraner et al., 2023]** *Inferring context-dependent computations through linear approximations of prefrontal cortex dynamics* (bioRxiv) — Linear dynamical models of PFC reveal that input gating within PFC dynamics, not routing via orthogonal afferent subspaces, may be the primary mechanism — relevant alternative interpretation for null results.

- **[Young et al., 2025]** *Hippocampal-Prefrontal Communication Subspaces Align with Behavioral and Network Patterns in a Spatial Memory Task* (eNeuro) — Hippocampal-PFC communication subspaces in rats co-vary with behavioral states, establishing that PFC communication subspaces are task-modulated in rodents — methodological precedent.

### Knowledge Map

**Known:**
- Cortical areas communicate through low-dimensional subspaces identified by RRR (Semedo et al. 2019, Neuron; Semedo et al. 2021, Nature Communications).
- Inter-areal communication channels are dynamic and can differ for feedforward vs. feedback directions (Semedo et al. 2021; Javadzadeh & Hofer 2022, Neuron).
- Within a single area, different task demands can be encoded in near-orthogonal subspaces, allowing selective readout without interference (Tang et al. 2020, eLife; Bayones et al. 2024, bioRxiv).
- In mice, inter-areal subspace geometry in visual cortex is dynamic and not solely determined by structural connectivity (Iyer et al. 2021, bioRxiv).
- RRR has known limitations around rank selection, noise correlation confounds, and multi-source interactions (Wu & Pillow 2025; Weiss & Coen-Cagli 2024; Liu et al. 2025, ICML).

**Unknown / contested:**
- Whether the VIS-to-PFC communication subspace specifically reconfigures across reward-context blocks (visual vs. auditory) in mice — this circuit and task combination has not been directly measured prior to this experiment.
- Whether context-dependent subspace reconfiguration in PFC-projecting circuits represents orthogonal routing (as predicted) versus gain modulation within a stable subspace (Srinath et al. 2021 showed stable subspace under attention in MT-SC; Naumann et al. 2022 showed invariant subspace maintained by feedback).
- Whether the PFC input geometry or PFC internal dynamics is the primary locus of context-dependent computation: Mante et al. 2013 and Soldado-Magraner et al. 2023 argue for internal PFC dynamics; the communication subspace framework argues for the routing channel. These are not mutually exclusive but have different predictions for this experiment.
- Whether N=5 subjects is sufficient power to detect the predicted R^2 drop — no prior power analysis for this specific effect size in VIS-to-PFC communication subspace experiments exists.

**How this hypothesis sheds light:**
*Contribution type: Constraint*

The specific decision node for this experiment is: should future studies use RRR cross-context generalization as a proxy for context-dependent routing in VIS-to-PFC circuits in mice? A positive result (significant R^2 drop, p<0.05) would establish that the VIS-to-PFC communication subspace geometry shifts across reward contexts in the dynamic routing task — providing the first direct evidence that the communication subspace framework extends to the VIS-PFC circuit in rodents during a context-switching paradigm. This would address the gap identified in Kohn et al. 2020 (Trends in Neurosciences), which explicitly flags context-dependent modulation of communication subspaces as an open question. A null result (as observed) rules out strongly orthogonal VIS-to-PFC subspace reconfiguration at the group level under these conditions, but does not rule out subtler reconfiguration detectable with larger N or more sensitive estimators, nor does it rule out the gain-modulation alternative (Srinath et al. 2021). The experiment constitutes a Constraint, not a Resolution, because N=5 is likely underpowered for this effect size, the RRR approach does not control for bidirectional VIS-PFC feedback, and the wide variation in unit counts across subjects (5–132 VIS units) introduces heteroscedasticity that the paired t-test does not address. The experiment cannot resolve whether null results reflect a genuine stable subspace (supporting Srinath et al. / Naumann et al.) or inadequate power, nor whether any detected reconfiguration would be specific to the VIS→PFC direction versus reflecting broader state changes in both areas.

**What the caveats affect:**
No triage caveats were loaded from the triage JSON — caveat impact not assessed from that source. However, two data-quality concerns are visible from code_output: Subject 759434 had only 5 VIS units (at the stated minimum threshold) and Subject 713655 had only 7 PFC units. Both subjects are likely contributing near-noise-floor R^2 estimates, inflating per-subject variability and suppressing the t-statistic. The optimal rank varied from 3 (Subject 713655, small unit count) to 12 (Subject 668755, 132 VIS units), suggesting the RRR model is not fitting a comparable subspace dimensionality across subjects — this makes the paired comparison of Vis_CV_R2 vs. Aud_R2_Geom potentially non-equivalent across subjects. Taken together, these data-quality heterogeneities make the p=0.099 result difficult to interpret as informative evidence for or against the hypothesis.

---

## 3. Experimental Plan

**Objective:** Determine if the VIS-to-PFC communication subspace geometrically reconfigures depending on the task context.

**Steps:**
1. Extract units from VIS (VISp, VISpm, VISam, VISal, VISrl, VISli) and PFC (ACA, PL, ILA, ORB, ACAd, ACAv, ORBvl, ORBl, ORBm) — high-quality units (default_qc=True) only.
2. Using post-stimulus activity (0–0.5 s), fit an RRR model predicting PFC from VIS specifically during Visual-rewarded blocks; select optimal rank by 5-fold cross-validation.
3. Apply the fixed RRR weights learned from Visual blocks to predict PFC from VIS during Auditory-rewarded blocks; compute the out-of-context R^2 geometrically (mean-centered within condition to isolate subspace geometry from mean firing rate shifts).
4. Use a paired t-test across subjects to test whether the predictive R^2 drops significantly when evaluated out-of-context (Auditory blocks) compared to within-context (Visual blocks).

**Deliverables:**
1. Cross-validated R^2 of the VIS→PFC mapping within Visual blocks.
2. R^2 of the same mapping applied to Auditory blocks.
3. Statistical analysis confirming or disconfirming context-dependency of the communication subspace.

---

## 4. Similar Analyses in the Literature

- **[Semedo et al., 2019]** — Method: RRR applied to V1→V2 population activity in macaque (same estimator class as this experiment). Regions: V1-V2 (visual cortex, different from VIS-PFC). Task: Passive viewing (different from context-switching). Caveats noted by authors: RRR dimensionality is sensitive to recording duration and trial count; the communication subspace is identified only up to orthogonal rotation within the low-rank subspace.

- **[Wu & Pillow, 2025]** — Method: Tutorial on RRR for neural communication; includes worked examples and a mathematical treatment of the estimator's properties. Regions: Multiple examples across cortical areas. Task: Multiple. Caveats: Explicitly discusses rank selection confounds, noise correlation artifacts, and the problem of cross-context generalization — the exact analysis used in this experiment. Key warning: cross-context R^2 drop can reflect differences in population variability or trial count across conditions rather than genuine subspace reconfiguration.

- **[D'Aleo et al., 2022]** — Method: Uses RRR-like dimensionality reduction to quantify cortico-cortical drive between premotor (PM) and primary motor (M1) cortex. Regions: PM-M1 (different from VIS-PFC). Task: Motor preparation and execution (different). Caveats: Communication direction difficult to establish from simultaneous recordings; RRR identifies correlation structure, not causation.

- **[Weiss & Coen-Cagli, 2024]** — Method: Extends RRR to explicitly measure stimulus information transfer through the communication subspace (SI-RRR). Regions: Generic sensory populations. Task: Stimulus response. Caveats: Notes that standard RRR R^2 conflates signal and noise components; proposes corrections that could be applied to this experiment's analysis.

- **[Liu et al., 2025]** — Method: MultiSource-RRR that simultaneously estimates communication from multiple source populations to a target population. Regions: Multi-area recordings. Task: Multiple. Caveats: Standard single-source RRR applied to PFC (which receives inputs from many areas) may overestimate or underestimate the VIS-specific communication subspace due to unmeasured sources contaminating the regression.

- **[Gokcen et al., 2021/2022]** — Method: Delayed linear systems model (dDMD-based) to disentangle bidirectional signals between populations. Regions: Multiple cortical areas. Task: Multiple. Caveats: Directly addresses the confound that standard RRR does not separate feedforward VIS→PFC from feedback PFC→VIS contributions; applied to this experiment, the standard RRR weights could partially reflect PFC self-consistency rather than VIS-driven routing.

- **[Young et al., 2025]** — Method: RRR communication subspace applied to hippocampal-PFC simultaneous recordings in rats during spatial memory. Regions: HPC-PFC (different from VIS-PFC but shares the PFC terminus). Task: Spatial memory (different). Caveats: Shows communication subspace alignment varies with behavioral states and network oscillations — establishing that within-session state variation is a confound for cross-context RRR comparisons unless carefully controlled.

---

## 5. Results and Findings

The experiment was successfully executed. Units were extracted from VIS and PFC across 5 subjects. An RRR model was trained on post-stimulus (0–0.5 s) spike counts to predict PFC activity from VIS activity during Visual-rewarded blocks, with rank selected by 5-fold cross-validation. The fixed RRR weights were then applied to Auditory-rewarded block data, with out-of-context R^2 computed geometrically (both conditions mean-centered within condition).

**Per-subject results:**

| Subject | VIS Units | PFC Units | Opt Rank | Vis CV R² | Aud R² (Geom) |
|---------|-----------|-----------|----------|-----------|----------------|
| 664851  | 87        | 157       | 10       | 0.3282    | 0.0738         |
| 742903  | 20        | 727       | 7        | 0.1139    | 0.0702         |
| 668755  | 132       | 226       | 12       | 0.2784    | 0.1470         |
| 759434  | 5         | 111       | 4        | 0.1804    | -0.2201        |
| 713655  | 29        | 7         | 3        | 0.0248    | 0.0468         |

Average drop in geometric R²: 0.1616
Paired t-test: t = 2.1390, p = 0.0992, N = 5 subjects

Because p > 0.05, the drop in predictive performance when evaluated out-of-context is not statistically significant.

**Conclusion (from code_output):** The communication subspace from VIS to PFC appears to remain relatively stable in its geometry across task contexts, rather than strictly reconfiguring into orthogonal subspaces depending on the rewarded modality.

**Review vs. Analysis:** The `review` field is consistent with `analysis`. Both report the same quantitative result (t=2.1390, p=0.0992) and reach the same conclusion: the hypothesis is not supported. There is no discrepancy between the two fields.

---

## 6. Reflection

**What was shown:**
[Verdict]: This result does not support the hypothesis. The cross-context R^2 drop is in the predicted direction (0.1616 average drop) but is not statistically significant at the p<0.05 threshold.
[Effect direction and size]: The VIS→PFC RRR model showed lower predictive R^2 on Auditory-rewarded blocks than on Visual-rewarded blocks in 4 of 5 subjects (with one subject showing negative out-of-context R^2), but the group effect was not significant.
[Key statistic]: prior 0.708 → posterior 0.422, N=5 subjects, t=2.1390, p=0.0992. The average within-context CV R^2 was 0.185 and the average out-of-context geometric R^2 was 0.024.
[Replication]: The directional effect (Vis_CV_R2 > Aud_R2_Geom) was present in 4 of 5 subjects; Subject 713655 (7 PFC units) showed a reversed trend. The group result is not robust — driven by 4 of 5 subjects with unequal unit counts, and the one reversal subject had minimal PFC units.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that the cross-validated R^2 of the VIS→PFC RRR model is equal when applied within Visual-rewarded blocks versus when applied to Auditory-rewarded blocks (i.e., the communication subspace geometry does not change across reward contexts). This experiment failed to reject the null (p = 0.0992, N = 5).
[Power note]: Given N=5, this test had unknown but likely inadequate power to detect an effect of the predicted magnitude. No prior effect size estimate for VIS-to-PFC communication subspace reconfiguration in this task exists; the observed Cohen's d-equivalent is approximately 0.96 (t/√N ≈ 2.14/2.24), which would require N≈10 for 80% power at α=0.05 two-tailed. Failure to reject is not informative about the true effect — the result is consistent with both a true null (stable subspace) and an underpowered detection of a real effect.

**What this rules out:**
[Rules out]: This result rules out strongly orthogonal VIS-to-PFC subspace reconfiguration at the group level that would be detectable with N=5 subjects and the RRR/paired t-test analysis used, because the observed p-value (0.099) is above the conventional threshold and the between-subject variance is large relative to the mean drop.
[Does not rule out]: This result does not rule out moderate subspace reconfiguration detectable in a larger cohort (N≥10), because the observed effect direction and magnitude (mean drop of 0.1616 R^2 units; directional in 4/5 subjects) are consistent with a real but statistically detectable effect that the current sample is too small to confirm.

**What would be needed next:**
[One experiment]: Apply the same RRR cross-context generalization analysis in a cohort of N≥10 subjects from the same dataset (114 sessions available per project memory), selecting only subjects with ≥20 VIS units and ≥20 PFC units, and using a permutation test (shuffling context labels) rather than a paired t-test to control for non-normality induced by the outlier-unit-count subjects.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by providing adequate statistical power to detect or rule out the predicted effect size, and by eliminating the heteroscedasticity confound that makes the current N=5 result uninterpretable as evidence of absence.
