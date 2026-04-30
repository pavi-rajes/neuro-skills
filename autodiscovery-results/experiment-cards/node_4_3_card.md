# Experiment Card: node_4_3

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — The specific VIS→PFC (context-invariant) vs. VIS→MOs (context-gated) dissociation has not been directly measured in rodents performing a visual/auditory context-switching task; the Communication Subspaces framework predicts target-specific routing but this combination of regions and task is unmeasured.
**Contribution type:** Negative constraint
**Triage verdict:** PASS  |  Mechanistic score: 4/5

---

## 0. Dataset Context

Sessions: 759434, 742903, 664851, 668755, 713655 (5 subjects)
Regions: VIS (source, units available per subject), MOs and PFC (prediction targets; PFC defined as PL/ILA/ACA/ORB prefixes)
Task: Visual/auditory context-switching, licking response (rewarded_modality blocks — Visual-rewarded vs. Auditory-rewarded)

---

## 1. Hypothesis

Visual signals are routed to the PFC continuously for state-monitoring regardless of context, while routing to MOs is strictly context-gated, supporting the Communication Subspaces framework of independent and target-specific routing geometries.

**Known limitations:** none flagged by triage

---

## 2. Literature Evidence

### Supporting

- **Semedo et al., 2019** *Cortical Areas Interact through a Communication Subspace.* (Neuron, score 0.987) — V1 and V2 interact via a low-dimensional communication subspace identified by RRR; only a subset of V1 population variance is preferentially transmitted to V2, establishing that inter-areal routing is target-specific and geometry-constrained rather than broadcast. *(analogical-circuit — same computational framework, different regions)*

- **MacDowell et al., 2025** *Multiplexed subspaces route neural activity across brain-wide networks.* (Nature Communications, score 0.928) — In mice performing flexible cognitive tasks, cortical and subcortical regions coordinate via multiplexed, task-dependent subspaces; cognitive flexibility relies on routing information through different networks depending on cognitive demands. *(analogical-task — same species, overlapping regions, flexible task context)*

- **Hajnal et al., 2024** *Shifts in attention drive context-dependent subspace encoding in anterior cingulate cortex in mice during decision making.* (Nature Communications, score 0.973) — Attention shifts drive context-dependent reconfiguration of population encoding geometry in mouse ACC, supporting the idea that subspace encoding changes with cognitive context in frontal areas closely related to PFC. *(analogical-circuit — mouse ACC rather than PFC/MOs)*

- **Snyder, Yu & Smith, 2021** *A Stable Population Code for Attention in Prefrontal Cortex Leads a Dynamic Attention Code in Visual Cortex.* (Journal of Neuroscience, score 0.759) — PFC maintains a stable population-level attention signal while visual cortex shows dynamic responses; PFC precedes and leads the attention code in visual cortex, consistent with a PFC state-monitoring role that is relatively context-invariant. *(analogical-task — primate, attention task)*

- **Rowe, Garrido & Tsuchiya, 2023** *Feedforward connectivity patterns from visual areas to the front of the brain contain information about sensory stimuli regardless of awareness or report.* (Cortex, score 0.927) — Feedforward input patterns from visual cortex to PFC carry stimulus-content information regardless of whether the stimulus was consciously seen, directly supporting context-independent VIS→PFC routing for state-monitoring. *(analogical-task — human EEG, different species and method)*

- **Peters et al., 2022** *Visuomotor learning promotes visually evoked activity in the medial prefrontal cortex.* (bioRxiv, score 0.769) — After visuomotor learning in mice, mPFC develops visually evoked responses reflecting learned stimulus-movement associations, suggesting mPFC continuously receives and represents visual signals once associations are learned. *(analogical-task — mouse visuomotor learning)*

- **Young et al., 2025** *Hippocampal-Prefrontal Communication Subspaces Align with Behavioral and Network Patterns in a Spatial Memory Task.* (eNeuro, score 0.772) — Hippocampal-PFC communication subspaces align with behavioral performance and network oscillatory states, demonstrating that PFC communication subspace structure is functionally meaningful and behavior-linked. *(analogical-circuit — hippocampus-PFC, different source region)*

### Opposing

- **Srinath, Ruff & Cohen, 2021** *Attention improves information flow between neuronal populations without changing the communication subspace.* (Current Biology, score 0.674) — Spatial attention increases information flow between MT and SC without changing the geometry of the communication subspace itself; this challenges the hypothesis that context gates routing by rotating subspace geometry, suggesting instead that routing modulation operates via gain on a fixed subspace. *(analogical-circuit — MT-SC, primate attention)*

- **Ferguson & Cardin, 2020** *Mechanisms underlying gain modulation in the cortex.* (Nature Reviews Neuroscience, score 0.978) — Cortical context-dependence is primarily mediated by gain modulation — multiplicative scaling of neuronal responses — rather than by geometric rotation of routing subspaces; provides a mechanistically distinct alternative to the Communication Subspaces account.

- **Naumann, Keijser & Sprekeler, 2021** *Invariant neural subspaces maintained by feedback modulation.* (bioRxiv, score 0.970) — Context-invariant sensory representations can be established through feedback modulation that maintains stable subspaces across contexts; the PFC-continuous pattern the hypothesis predicts might reflect feedback stabilization rather than independent target-specific routing geometries.

- **Liu, Sacks & Golub, 2025** *Accurate Identification of Communication Between Multiple Interacting Neural Populations.* (ICML, score 0.970) — Standard pairwise RRR produces systematically biased estimates when confounded by shared third-area inputs; the true communication subspace may be misidentified when only two of three interacting regions (VIS, MOs, PFC) are modeled — directly undermining the pairwise VIS→MOs and VIS→PFC metrics used here.

- **Liu et al., 2026 (preprint)** *State-Dependent Dissociation of Shared Input and Directed Information Flow in the Visual Cortex.* (bioRxiv, score 0.972) — RRR-estimated inter-laminar subspaces in V1 are modulated by both visual stimulation and internal brain state (eyes open vs. closed); differences in RRR metrics across conditions may reflect state changes in shared input rather than directed routing changes.

### Contextual

- **Semedo et al., 2020** *Statistical methods for dissecting interactions between brain areas.* (Current Opinion in Neurobiology, score 0.976) — Reviews RRR and related methods for estimating communication subspaces from large-scale recordings; establishes RRR as the standard estimator for this class of question.

- **Wu & Pillow, 2025** *Reduced rank regression for neural communication: a tutorial for neuroscientists.* (preprint, score 0.974) — Comprehensive tutorial on RRR including mathematical foundations, hyperparameter selection, and known limitations (sample size requirements, regularization sensitivity).

- **Weiss & Coen-Cagli, 2024** *Measuring Stimulus Information Transfer Between Neural Populations through the Communication Subspace.* (bioRxiv, score 0.974) — Proposes a framework linking subspace structure to stimulus information transmitted between populations; shared noise variability can confound subspace-based routing estimates.

- **Mante et al., 2013** *Context-dependent computation by recurrent dynamics in prefrontal cortex.* (Nature, score 0.721) — Foundational evidence that PFC implements context-dependent integration of sensory inputs via recurrent dynamics; forms the backdrop against which the hypothesis's PFC-continuous claim must be evaluated.

- **Gokcen et al., 2021** *Disentangling the flow of signals between populations of neurons.* (Nature Computational Science, score 0.740) — DLAG framework enables disentangling bidirectional communication; feedforward and feedback signals occupy different subspaces — a critical methodological context for interpreting pairwise RRR estimates.

- **Semedo et al., 2021** *Feedforward and feedback interactions between visual cortical areas use different population activity patterns.* (bioRxiv, score 0.738) — Feedforward and feedback signals between V1 and V2/V3 occupy geometrically distinct subspaces; pairwise RRR conflates both directions.

- **Wang, Liu & Yao, 2019** *Control of adaptive action selection by secondary motor cortex during flexible visual categorization.* (bioRxiv, score 0.778) — MOs is causally required for adaptive action selection during flexible visual categorization in mice; bilateral inactivation impairs boundary switching but not basic visual discrimination, establishing MOs as a context-sensitive gate for visually-guided actions.

- **Chang et al., 2024** *Rule-based modulation of a sensorimotor transformation across cortical areas.* (eLife, score 0.668) — In mice performing a cross-modal sensory selection task (lick to tactile or visual stimuli based on rule), rule context reshapes population geometry along a cortical processing chain — directly analogous to the VIS→MOs context-gating claim.

- **Terada et al., 2022** *Transition of distinct context-dependent ensembles from secondary to primary motor cortex in skilled motor performance.* (Cell Reports, score 0.665) — Context dependency is consistently high in M2/MOs L2/3 neurons and low in M1, characterizing MOs as a context-sensitive node that integrates contextual and motor signals.

- **Pereira-Obilinovic, Froudist-Walsh & Wang, 2024** *Cognitive network interactions through communication subspaces in large-scale models of the neocortex.* (bioRxiv, score 0.957) — Large-scale cortical network models show inter-areal communication subspaces reorganize during cognitive task switching, with different networks engaging different routing channels by context.

- **Iyer et al., 2021** *Geometry of inter-areal interactions in mouse visual cortex.* (bioRxiv, score 0.930) — Inter-areal interaction geometry between mouse visual areas shows both fixed and dynamic components; directly relevant to whether VIS→PFC and VIS→MOs subspaces are fixed or context-dependent.

- **Chow, Romo & Brody, 2009** *Context-Dependent Modulation of Functional Connectivity: Secondary Somatosensory Cortex to Prefrontal Cortex Connections.* (Journal of Neuroscience, score 0.934) — Functional connectivity between S2 and PFC varies with task phase (encoding vs. comparison) in a discrimination task, analogous to context-gated sensory-to-prefrontal routing.

- **Okazawa & Kiani, 2022** *Neural Mechanisms that Make Perceptual Decisions Flexible.* (Annual Review of Physiology, score 0.972) — Reviews flexible decision-making mechanisms; highlights that the mechanisms by which PFC integrates context-gated vs. continuous sensory signals remain an open question.

### Knowledge Map

**Known:**
- Inter-areal communication operates through low-dimensional subspaces identifiable by RRR: only a subset of source-area variance is transmitted to each target (Semedo et al., 2019; Semedo et al., 2020).
- Subspace routing is target-specific: different downstream areas receive different projections of the same upstream population activity (Semedo et al., 2019; MacDowell et al., 2025).
- MOs/secondary motor cortex is causally required for context-dependent action selection during visual tasks in mice and maintains high context dependency in its population activity (Wang et al., 2019; Terada et al., 2022).
- PFC maintains stable population codes for cognitive states over time; its input from visual areas carries stimulus content regardless of task context (Snyder et al., 2021; Rowe et al., 2023).
- Feedforward and feedback inter-areal signals occupy distinct population subspaces; pairwise RRR conflates both (Semedo et al., 2021; Gokcen et al., 2021).

**Unknown / contested:**
- Whether VIS→PFC and VIS→MOs communication subspaces have qualitatively different context-dependence (one invariant, one gated) in rodents performing a visual/auditory context-switching task — the specific gap this experiment targets.
- Whether pairwise RRR context modulation metrics reliably dissociate target-specific routing from shared upstream state changes: Liu et al. (2025, ICML) demonstrate systematic bias when a third area simultaneously interacts with both targets, which is precisely the VIS-MOs-PFC scenario here.
- Whether context-invariance of VIS→PFC routing is general or task-specific: reviewed literature shows PFC can be context-gated (Mante et al., 2013) or context-invariant (Rowe et al., 2023) depending on the specific computation.
- Whether subspace geometry rotation or gain modulation is the mechanism for context-dependent routing — attention studies (Srinath et al., 2021; Ferguson & Cardin, 2020) support gain modulation on a fixed subspace as a competitive alternative.

**How this hypothesis sheds light:**
*Contribution type: Negative constraint*

The specific unknown this experiment addresses is whether VIS→PFC and VIS→MOs pathways show qualitatively different context-dependence in a rodent context-switching task — a gap at the intersection of the Communication Subspaces framework and the empirical literature on MOs as a context-gated node. The decision node for downstream research is: should a scientist designing a follow-up optogenetic or pharmacological experiment target VIS→MOs routing (if strictly context-gated) versus VIS→PFC routing (if context-invariant) as the primary locus of contextual gating? The null result (t=0.124, p=0.9073, N=5) does not support the hypothesized dissociation, providing a Negative constraint: it rules out a strong differential effect (mean difference = 0.002 context modulation units, trivially small) but does not rule out a smaller effect undetectable at N=5. A positive result would have constrained the communication architecture and justified designing circuit-level interventions targeting differential routing. The null result rules out the strongest form of the claim — that VIS→MOs context modulation substantially exceeds VIS→PFC context modulation in this task — but cannot determine whether this reflects genuine biological equivalence, limitations of the PCA+Ridge estimator, a third-area confound (Liu et al., 2025), or insufficient power. The experiment cannot resolve which alternative explanation is operative, nor can it establish that the two pathways are equivalent (absence of evidence is not evidence of absence at N=5).

**What the caveats affect:**
No triage caveats were flagged for this experiment. However, the dataset used (N=5 subjects, pilot cohort) is a documented scale limitation — project memory notes the full dataset has ~114 sessions available. With N=5 subjects and mean context modulation near zero for both pathways (Mod_MOs=0.0128, Mod_PFC=0.0108), the paired t-test has very low power to detect a small but real differential effect. A null result at N=5 is a Negative constraint, not a Resolution: it narrows the plausible large-effect-size range but cannot rule out a genuine differential effect smaller than this experiment's detection threshold. Scaling to the full cohort would be required to draw stronger conclusions.

---

## 3. Experimental Plan

**Objective:** Compare the context-dependence of VIS-to-MOs predictive coupling versus VIS-to-PFC predictive coupling by utilizing smoothing and dimensionality reduction (PCA) to extract robust, cross-validated predictive variance (R-squared) metrics.

**Steps:**
1. Setup & Data Loading: Safely load dependency packages. Robustly locate and selectively load `units.parquet` and `trials.parquet`. Filter for high-quality units (default_qc==True) assigned to VIS, MOs, and PFC regions.
2. Trial & Activity Extraction: Isolate trials from Visual-rewarded and Auditory-rewarded blocks based on `rewarded_modality`. For each unit, extract post-stimulus activity (0.0s to 0.5s) using larger 50ms time bins (10 bins per trial).
3. Smoothing & Denoising: Apply a Gaussian filter (sigma=1.5 or 2) across time bins for each trial to smooth binned spike counts and improve signal-to-noise ratio.
4. Dimensionality Reduction (PCA): Concatenate all trials and fit PCA for each region to extract the top 10 principal components (or fewer if a region has <10 units). Transform smoothed unit activity into this low-dimensional PC space.
5. Predictive Modeling: Split PC-transformed data back into Visual and Auditory trial sets. For each context, fit cross-validated Ridge Regression models (RidgeCV, K-Fold CV) predicting MOs PC scores from VIS PC scores and PFC PC scores from VIS PC scores.
6. Metric Calculation: Calculate cross-validated R-squared for all four models (VIS→MOs Visual, VIS→MOs Auditory, VIS→PFC Visual, VIS→PFC Auditory). Compute Context Modulation Metric as (Visual R2 - Auditory R2) for each pathway.
7. Statistical Testing: Perform a paired t-test across subjects comparing the Context Modulation Metric of VIS-to-MOs against VIS-to-PFC to determine if VIS→MOs coupling is significantly more context-dependent.

**Deliverables:**
1. PC-transformed, smoothed neural trajectories for VIS, MOs, and PFC.
2. Cross-validated R-squared values for VIS-to-MOs and VIS-to-PFC pathways in both contexts.
3. Context Modulation Metrics (Visual R2 - Auditory R2) for both pathways.
4. Statistical test results comparing the context modulation of the two pathways across subjects.

---

## 4. Similar Analyses in the Literature

- **Semedo et al., 2019** (Neuron) — Method: RRR to identify communication subspace between V1 and V2. Match: uses cross-validated RRR to find low-dimensional predictive mapping between neural populations, directly analogous to the VIS→MOs and VIS→PFC Ridge+PCA approach here. Regions: V1→V2 (primate), different from VIS→MOs/PFC (mouse). Task: passive viewing, different from context-switching task. Caveats: authors note that RRR rank selection is sensitive to regularization strength and trial count.

- **MacDowell et al., 2025** (Nature Communications) — Method: Cortex-wide calcium imaging combined with RRR-style dimensionality reduction to quantify routing across brain-wide networks. Match: computes context-dependent routing metrics across multiple cortical targets, same conceptual design as this experiment. Regions: 8 cortical and subcortical regions (mouse), overlapping with VIS/MOs/PFC. Task: flexible cognitive tasks in mice, same species and approximate task structure. Caveats: calcium imaging has slower temporal resolution than electrophysiology.

- **Young et al., 2025** (eNeuro) — Method: RRR to estimate hippocampal-PFC communication subspaces. Match: applies RRR cross-validated predictive framework to assess PFC communication subspace structure during a memory task. Regions: hippocampus→PFC (rat), different source region. Task: spatial memory, different task. Caveats: none noted by authors specific to RRR.

- **Liu, Sacks & Golub, 2025** (ICML) — Method: Multi-population RRR extension that accounts for simultaneous interactions among three or more areas. Match: directly addresses the methodological limitation of pairwise RRR used here (VIS→MOs and VIS→PFC estimated separately rather than jointly). Regions: multi-area simulated and real data. Task: N/A (methodological). Caveats: requires simultaneous recordings from all three areas, which the current dataset provides — but the analysis did not use the multi-area variant.

- **Gokcen et al., 2021** (Nature Computational Science) — Method: DLAG (delayed latents across groups), a directional dimensionality reduction that explicitly disentangles feedforward and feedback signals. Match: addresses the directional ambiguity in pairwise RRR (which conflates VIS→target with target→VIS feedback). Regions: V1-V2/V4 (primate). Task: passive visual stimulation. Caveats: requires precise temporal alignment; harder to apply when trial structure dominates over continuous dynamics.

- **Liu et al., 2026** (bioRxiv) — Method: RRR applied to laminar recordings in macaque V1 with explicit decomposition of shared input vs. directed flow. Match: shows that context modulation metrics derived from RRR can reflect shared input changes rather than directed routing changes — a direct methodological concern for this experiment. Regions: V1 laminar (macaque). Task: passive viewing vs. eyes-closed. Caveats: laminar approach requires depth information not available in the current single-unit dataset.

---

## 5. Results and Findings

The revised experiment successfully executed the pipeline with Gaussian smoothing and PCA dimensionality reduction, achieving meaningful positive R-squared values (ranging from ~0.05 to ~0.30), indicating the models captured predictive variance. The Context Modulation Metric was calculated as (Visual R2 - Auditory R2) for each pathway.

**Per-subject results:**

| Subject | VIS→MOs Vis R2 | VIS→MOs Aud R2 | VIS→PFC Vis R2 | VIS→PFC Aud R2 | Mod_MOs | Mod_PFC |
|---------|---------------|---------------|---------------|---------------|---------|---------|
| 759434  | 0.0754        | 0.0732        | 0.0838        | 0.0625        | 0.0022  | 0.0213  |
| 742903  | 0.1505        | 0.1302        | 0.1509        | 0.1282        | 0.0202  | 0.0227  |
| 664851  | 0.1578        | 0.1261        | 0.2730        | 0.2773        | 0.0317  | -0.0042 |
| 668755  | 0.3019        | 0.3055        | 0.2746        | 0.2356        | -0.0036 | 0.0390  |
| 713655  | 0.1807        | 0.1674        | 0.0557        | 0.0803        | 0.0133  | -0.0246 |

Mean Context Modulation Metric (VIS→MOs): 0.0128
Mean Context Modulation Metric (VIS→PFC): 0.0108
Paired t-test (VIS→MOs vs VIS→PFC context modulation): t-statistic = 0.124, p-value = 0.9073

**Conclusion from analysis and review:** No statistically significant difference in context modulation between VIS→MOs and VIS→PFC pathways. Both pathways exhibit similar, relatively low levels of context modulation. The hypothesis that VIS→MOs coupling is strictly context-gated while VIS→PFC routing is continuous is not supported by the data.

The review confirms the analysis: the experiment faithfully implemented the plan with the corrected methodology (Gaussian smoothing + PCA resolving the negative R-squared issue from a prior run). The review and analysis are consistent — there is no conflict.

---

## 6. Reflection

**What was shown:**
[Verdict]: This result does not support the hypothesis. The expected dissociation between a context-invariant VIS→PFC pathway and a context-gated VIS→MOs pathway was not observed.
[Effect direction and size]: Both VIS→MOs and VIS→PFC pathways showed similarly low and statistically indistinguishable levels of context modulation, with mean context modulation metrics of 0.0128 (MOs) and 0.0108 (PFC) — a difference of 0.002.
[Key statistic]: N=5 subjects, t=0.124, p=0.9073 (paired t-test, two-tailed, VIS→MOs context modulation vs. VIS→PFC context modulation).
[Replication]: The direction of the effect was inconsistent across subjects: 3 of 5 subjects showed slightly higher MOs context modulation, and 2 of 5 showed higher PFC context modulation; the group result reflects near-zero effect in both pathways, not a consistent directional trend.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that VIS→MOs and VIS→PFC context modulation metrics (Visual R2 minus Auditory R2) do not differ across subjects. This experiment failed to reject the null (p=0.9073, N=5).
[Power note]: Given N=5, this test had unknown power to detect an effect of the predicted magnitude — no prior effect size estimate was available to anchor a power calculation. The extremely high p-value (0.9073) and trivially small effect size (0.002 difference in context modulation) suggest that if a true differential effect exists, it is very small and not detectable at N=5. Failure to reject is not informative about the true effect at this sample size — it does not rule out a real but small differential between the two pathways.

**What this rules out:**
[Rules out]: This result rules out a large context-gating differential between VIS→MOs and VIS→PFC in this five-subject pilot dataset, because the observed mean difference was 0.002 with a t-statistic of 0.124, constituting no evidence whatsoever for a strong pathway-specific routing asymmetry.
[Does not rule out]: This result does not rule out a real but smaller differential effect between VIS→MOs and VIS→PFC context modulation, because N=5 provides insufficient power to detect small-to-medium effects, and the within-subject variance in context modulation was high relative to the mean difference.

**What would be needed next:**
[One experiment]: Apply the same PCA+RidgeCV pipeline to N≥30 subjects from the full ~114-session cohort, with matched unit count requirements for VIS, MOs, and PFC, to achieve adequate power to detect a context modulation differential of 0.02–0.05 (the scale observed within each pathway here); additionally, apply multi-population RRR (Liu et al., 2025) jointly modeling all three areas to control for shared-input confounds.
[Why this upgrades]: This would move the contribution from Negative constraint to Resolution — a null result at N≥30 would constitute genuine evidence of equivalence, while a positive result at N≥30 would provide adequately powered evidence for the hypothesized asymmetry and justify targeting the VIS→MOs circuit in downstream causal experiments.
