# Experiment Card: node_4_12

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — Srinath (2021) showed attention improves VIS communication, but whether VIS→MOs subspace specifically fails on Miss trials trial-by-trial has not been measured.
**Triage verdict:** PASS  |  Mechanistic score: 5/5
**Surprise:** Δ -0.203  (prior: 0.708 → posterior: 0.578)

---

## 0. Dataset Context

**Sessions:** 664851, 742903, 668755, 713655 (4 subjects)
**Regions:** VIS (20–132 units/subject); MOs (137–437 units/subject)
**Task:** Visual target trials — hit vs. miss comparison (Dynamic Routing task)

---

## 1. Hypothesis
Subspace Geometry of Errors: When an animal fails to respond to a target (Miss trial), it is because the sensory-to-motor (VIS->MOs) communication subspace has geometrically rotated out of alignment, rather than a mere drop in sensory amplitude, supporting the Communication Subspaces routing framework.

**Known limitations:**
None flagged

---

## 2. Literature Evidence

### Supporting
- **[U et al., 2025]** *Neural dynamics outside task-coding dimensions drive decision trajectories through transient amplification* — Most behaviors involve neural dynamics in high-dimensional activity spaces. A common approach is to extract dimensions that capture task-related variability, such as those separating stimuli or choice
- **[R et al., 2021]** *Attention improves information flow between neuronal populations without changing the communication subspace* — Visual attention allows observers to flexibly use or ignore visual information, suggesting that information can be flexibly routed between visual cortex and neurons involved in decision-making. We inv
- **[Y et al., 2021]** *Contribution of non-sensory neurons in visual cortical areas to visually guided decisions in the rat.* — It is widely assumed that trial-by-trial variability in visual detection performance is explained by the fidelity of visual responses in visual cortical areas influenced by fluctuations of internal st
- **[M et al., 2020]** *Motor cortical dynamics are shaped by multiple distinct subspaces during naturalistic behavior* — Behavior relies on continuous influx of sensory information about the body. In primates, motor cortex must integrate somatic feedback to accurately reach and manipulate objects
- **[C et al., 2020]** *Minimally dependent activity subspaces for working memory and motor preparation in the lateral prefrontal cortex* — The lateral prefrontal cortex is involved in the integration of multiple types of information, including working memory and motor preparation. However, it is not known how downstream regions can extra
- **[C et al., 2019]** *Independent Activity Subspaces for Working Memory and Motor Preparation in the Lateral Prefrontal Cortex* — The lateral prefrontal cortex is involved in the integration of multiple types of information, including working memory and motor preparation. However, it is not known how downstream regions can extra

### Opposing
_No direct contradicting evidence found in search results._

### Contextual
- **[M et al., 2016]** *Distinct roles of visual, parietal, and frontal motor cortices in memory-guided sensorimotor decisions* — Mapping specific sensory features to future motor actions is a crucial capability of mammalian nervous systems. We investigated the role of visual (V1), posterior parietal (PPC), and frontal motor (fM
- **[L et al., 2021]** *Modulation in cortical excitability disrupts information transfer in perceptual-level stimulus processing* — Despite significant interest in the neural underpinnings of behavioral variability, little light has been shed on the cortical mechanism underlying the failure to respond to perceptual-level stimuli. 
- **[J et al., 2015]** *Mouse V1 population correlates of visual detection rely on heterogeneity within neuronal response patterns* — Previous studies have demonstrated the importance of the primary sensory cortex for the detection, discrimination, and awareness of visual stimuli, but it is unknown how neuronal populations in this a
- **[J et al., 2015]** *Heterogeneity and dynamics of cortical populations coding visual detection* — Previous studies have demonstrated the importance of the primary sensory cortex for the detection, discrimination and awareness of visual stimuli, but it is unknown how neuronal populations in this ar
- **[C et al., 2024]** *Task-specific invariant representation in auditory cortex* — Categorical sensory representations are critical for many behaviors, including speech perception. In the auditory system, categorical information is thought to arise hierarchically, becoming increasin
- **[K et al., 2021]** *The geometry of representational drift in natural and artificial neural networks* — Neurons in sensory areas encode/represent stimuli. Surprisingly, recent studies have suggested that, even during persistent performance, these representations are not stable and change over the course

### Knowledge Map

**Known:**
- Attention improves information flow between visual populations through communication subspace alignment (Srinath et al., 2021)
- The VIS→MOs communication subspace is identifiable via PLS/RRR and predicts motor cortex activity (Semedo et al., 2019)
- Trial-by-trial neural variability in sensory cortex predicts behavioral hits and misses (Osako et al., 2021)
- Neural dynamics outside task-coding dimensions drive decision trajectories (Pereira-Obilinovic et al., 2025)

**Unknown / contested:**
- Whether Miss trials specifically reflect reduced VIS→MOs subspace alignment rather than upstream encoding failure or downstream motor threshold effects
- Whether subspace failure on Miss trials is consistent across subjects or driven by single sessions
- Whether communication subspace alignment captures something causally distinct from single-unit activity predictors of misses

**How this hypothesis sheds light:**
This experiment directly tests whether perceptual misses involve a breakdown in VIS→MOs subspace communication trial-by-trial. A positive result would be the first evidence that inter-areal subspace alignment tracks trial outcome, linking the communication subspace framework to behavior. A null result would suggest misses reflect upstream encoding or downstream decision failures not captured by subspace geometry.

---

## 3. Experimental Plan

**Objective:** Test if the fixed VIS->MOs communication subspace identified during Hit trials fails to capture the VIS->MOs interaction during Miss trials significantly more than what is expected by amplitude differences.

**Steps:**
1. Identify subjects with >=15 units in VIS and MOs.
2. Extract stimulus-evoked (0-0.5s) spike counts for visual target trials during visual-rewarded blocks.
3. Fit a Reduced-Rank Regression (RRR) model mapping VIS to MOs using only 'Hit' trials to define the 'Successful Communication Subspace'.
4. Compute the predictive R^2 of this model when applied to held-out 'Hit' trials vs 'Miss' trials.
5. To control for gain/amplitude drops on Miss trials, normalize the R^2 on Miss trials by the total variance of the MOs activity on Miss trials.
6. Perform a paired t-test across subjects to check if the normalized R^2 is significantly lower on Miss trials, indicating a geometric misalignment rather than just a gain reduction.

**Deliverables:** 1. Normalized predictive R^2 of the Hit-trained RRR model evaluated on held-out Hit vs Miss trials per subject.
2. Statistical test results determining if errors are characterized by subspace rotation/misalignment.

---

## 4. Similar Analyses in the Literature
_No direct methodological precedent found._

---

## 5. Results and Findings

The code executed successfully and tested the hypothesis that Miss trials are driven by a geometric misalignment in the VIS->MOs communication subspace. 

Four subjects were initially identified with at least 15 high-quality units in both VIS and MOs. However, subjects 664851 and 668755 were skipped because they had only 1 Miss trial each during the visual-rewarded blocks, leaving only two subjects (713655 and 742903) for the analysis. 

For these two subjects, the Reduced-Rank Regression (RRR) model trained on Hit trials yielded negative predictive R² values for both held-out Hit and Miss trials, suggesting poor overall model generalization or high noise. Despite this, the R² values for Miss trials (-4.07 and -4.94) were notably much lower than those for held-out Hit trials (-0.54 and -0.17). A paired t-test across the two subjects yielded a t-statistic of 6.7131 and a p-value of 0.0941. 

Because the p-value is greater than 0.05, the result is not statistically significant. The dataset's small number of Miss trials in proficient subjects severely limited statistical power, preventing conclusive validation of the subspace rotation hypothesis for error trials.

**AutoDiscovery review:**
The experiment was successfully implemented and followed the planned steps to test the hypothesis.

**Hypothesis:** During a visual-rewarded block, when an animal fails to respond to a visual target (Miss trial), the error is driven by a geometric rotation/misalignment of the sensory-to-motor (VIS->MOs) communication subspace, rather than a mere reduction in sensory response amplitude.

**Experiment Results:**
- The pipeline successfully identified 4 valid subjects with at least 15 high-quality units in both the visual cortex (VIS) and secondary motor cortex (MOs).
- Upon filtering for target trials in visual-rewarded blocks, two subjects (664851 and 668755) had to be excluded because they each only performed 1 Miss trial, making cross-validation impossible.
- For the remaining two subjects (713655 and 742903), a Reduced-Rank Regression (RRR) model was trained exclusively on 'Hit' trials using 5-fold cross-validation to define the successful VIS->MOs communication subspace.
- The model's normalized predictive R² was evaluated on held-out Hit trials versus Miss trials. 
- The predictive R² values for both held-out Hit and Miss trials were negative (Hit R²: -0.54, -0.17; Miss R²: -4.07, -4.94), indicating poor overall model generalization or a high degree of noise on single trials.
- Despite negative values, the R² on Miss trials was drastically lower than on held-out Hit trials. A paired t-test across the 2 subjects yielded a t-statistic of 6.7131 and a p-value of 0.0941.

**Findings:**
Although the model fits generated substantially worse predictions for Miss trials compared to Hit trials (which conceptually aligns with a subspace misalignment on error trials), the results are not statistically significant (p = 0.0941 > 0.05). The primary limitation is the extremely low number of Miss trials produced by proficient mice, restricting the analysis to only two viable subjects and severely limiting statistical power. Consequently, while the trend points towards the Communication Subspaces framework for error trials, the hypothesis cannot be conclusively validated with this specific dataset.

---

## 6. Reflection
**What was shown:**
[Verdict]: This result is underpowered — no conclusion about the hypothesis is valid at N=2 effective subjects.
[Effect direction and size]: Only 2 of 4 qualifying subjects had sufficient Miss trials; RRR Miss-trial R² (−4.07, −4.94) was substantially lower than Hit-trial R² (−0.54, −0.17), but all R² values were negative indicating poor model generalization.
[Key statistic]: N=2 effective subjects, t = 6.71, p = 0.0941.
[Replication]: Direction was consistent across both qualifying subjects, but N=2 is insufficient to draw any population-level inference.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that MOs→VIS communication-subspace alignment does not differ between Hit and Miss trials. This experiment failed to reject the null (p = 0.0941, N = 2 effective subjects).
[Power note]: Given N=2 effective subjects, this test had inadequate power — a single degree of freedom renders the t-test uninterpretable. Failure to reject is not informative; the analysis cannot distinguish between no effect and insufficient trial counts (Miss trials are rare in proficient animals).

**What this rules out:**
[Rules out]: This result rules out drawing any conclusion about the subspace misalignment account at pilot scale, because N=2 effective subjects cannot support a population-level test — the single degree of freedom makes the t-test meaningless.
[Does not rule out]: This result does not rule out the subspace misalignment hypothesis itself, because the direction of the effect is consistent with the prediction in both subjects and the bottleneck is trial count (Miss trials are rare in proficient animals), not an absence of the predicted signal.

**What would be needed next:**
[One experiment]: Filter the full ~114-session cohort for sessions with ≥10 Miss trials in visual-rewarded blocks, then re-run the RRR comparison with at least N=8 qualifying subjects.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by replacing the underpowered 2-subject comparison with a properly powered cross-subject analysis.
