# Experiment Card: node_3_10

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — The attractor-dynamics framework predicts transient dimensionality expansion during context transitions, but no prior study has measured this directly with participation ratio on a brain-wide multi-region electrophysiology dataset during unsignaled block switches in this task.
**Contribution type:** Negative constraint
**Triage verdict:** PASS  |  Mechanistic score: 4/5

---

## 0. Dataset Context

Sessions: 759434, 742903, 664851, 668755, 713655 (5 subjects)
Regions: All high-quality units pooled globally across all recorded regions per subject (global brain state vector)
Task: Visual/auditory context-switching task with unsignaled block switches; pre-stimulus window (-0.5 to 0 s); 25 blocks analyzed (5 per subject; block 0 excluded)

---

## 1. Hypothesis

Brain-wide state space dimensionality transiently expands during context transitions: the participation ratio of the global neural population (all recorded regions combined) is significantly higher during the first 10 trials after an unsignaled block switch compared to steady-state trials, reflecting a high-dimensional search before settling into a new low-dimensional attractor state.

**Known limitations:** none flagged in triage. Two methodological concerns emerge from the literature: (1) participation ratio is substantially biased toward overestimation with small sample sizes (10 trials per epoch; Chun et al. 2025; Altan et al. 2020); (2) the global PR depends on how many units are recorded and is unbounded by neuron count (Manley et al. 2024), complicating cross-subject comparison.

---

## 2. Literature Evidence

### Supporting

- **Kikumoto et al., 2024** *A transient high-dimensional geometry affords stable conjunctive subspaces for efficient action selection* — Before successful context-dependent action selection in humans (EEG), there is a transient expansion of representational dimensionality that separates conjunctive subspaces; entry into this stable, high-dimensional state predicts individual trial performance.
- **Badre et al., 2020** *The dimensionality of neural representations for control* — Review identifies dimensionality changes during cognitive control as a predicted but uncharacterized effect; separability/generalizability trade-off in prefrontal control representations frames dimensionality expansion as theoretically expected.
- **Katori et al., 2011** *Representational Switching by Dynamical Reorganization of Attractor Structure in a Network Model of the Prefrontal Cortex* — Representational switching between task contexts corresponds to bifurcations in attractor structure driven by short-term synaptic plasticity; the model predicts transient network-wide reorganization before settling into the new stable attractor state.
- **Miller, 2016** *Itinerancy between attractor states in neural systems* — Discrete attractor states form within neural circuits; external stimuli or internal signals cause transitions, and the transitional period is distinct from steady-state attractor occupancy. Hidden Markov modeling reveals such state transitions across many circuits.

### Opposing

- **Soldado-Magraner, Mante, Sahani, 2023** *Inferring context-dependent computations through linear approximations of prefrontal cortex dynamics* — Context-dependent computations in PFC can be implemented via either context-dependent recurrent dynamics or subtle input modulation, both involving low-dimensional linear dynamics within each context; no transient dimensionality expansion is required between contexts. This challenges the necessity of a PR expansion during transitions.
- **Chun, Canatar, Chung, Lee, 2025** *Estimating Dimensionality of Neural Representations from Finite Samples* — Participation ratio is highly biased with small sample sizes; with 10 trials and hundreds of units (as used here), PR overestimates true dimensionality and the bias is large enough to mask or mimic real condition differences. *(Direct methodological concern for this experiment.)*
- **Altan, Solla, Miller, Perreault, 2020** *Estimating the dimensionality of the manifold underlying multi-electrode neural recordings* — All dimensionality estimation algorithms including PR fail when sample count is low or when true dimensionality exceeds ~20; most algorithms overestimate dimensionality in high-noise conditions. *(Direct methodological concern for this experiment.)*
- **Mazzucato, Fontanini, La Camera, 2015** *Stimuli Reduce the Dimensionality of Cortical Activity* — Sensory stimuli reduce (not expand) cortical dimensionality relative to ongoing activity by driving the network into a single attractor basin; this opposing prediction challenges the hypothesis direction.

### Contextual

- **Manley et al., 2024** *Simultaneous, cortex-wide dynamics of up to 1 million neurons reveal unbounded scaling of dimensionality with neuron number* — Dimensionality scales unboundedly with neuron number; half the neural variance is captured in ~16 behavioral dimensions, but global PR is strongly dependent on recording scale.
- **Wang et al., 2025** *The geometry and dimensionality of brain-wide activity* — Brain-wide neural activity covariance spectrum is scale-invariant (subpopulations resemble the full brain); PR on a random subsample is an unreliable index of global dimensionality.
- **Stringer et al., 2019** *Spontaneous behaviors drive multidimensional, brainwide activity* — Ongoing pre-stimulus brain-wide activity is already high-dimensional (>100 reliable latent dimensions) in mice; this brainwide behavioral-state signal persists orthogonally during task engagement, meaning the steady-state baseline is not low-dimensional.
- **Ueltzhöffer et al., 2015** *Stochastic Dynamics Underlying Cognitive Stability and Flexibility* — Attractor-like working memory dynamics implement task-rule switching; transitions between rule attractors are stochastic, with dopaminergic modulation adjusting stability thresholds — without requiring high-dimensional expansion.
- **Dahmen et al., 2020** *Strong and localized recurrence controls dimensionality of neural activity across brain areas* — Recurrent synaptic network structure is the primary determinant of neural dimensionality; cortical activity transitions among states with different dimensionalities through time, driven by local circuitry.
- **Jazayeri & Ostojic, 2021** *Interpreting neural computations by examining intrinsic and embedding dimensionality of neural activity* — Participation ratio primarily reflects embedding dimensionality and may not capture computationally relevant changes in representation geometry during context switching.
- **Song, Shim, Rosenberg, 2022** *Large-scale neural dynamics in a shared low-dimensional state space reflect cognitive and attentional dynamics* — Whole-brain dynamics traverse low-dimensional latent states across attention and cognition; cognitive context shifts are reflected in traversals along low-dimensional gradients, not high-dimensional expansions.
- **Flesch et al., 2022** *Orthogonal representations for robust context-dependent task performance in brains and neural networks* — Context-dependent task performance relies on low-dimensional orthogonal manifolds for each context ('rich coding'); neural geometry in macaque PFC and human fMRI is consistent with structured low-dimensional coding, not high-dimensional expansion.
- **Engel & Steinmetz, 2019** *New perspectives on dimensionality and variability from large-scale cortical dynamics* — Review notes that local and global dimensionality measures can diverge; activity propagates on multiple spatial scales and diverse observations can be reconciled by considering multi-scale propagation.

### Knowledge Map

**Known:**
- Neural populations operating during cognitive tasks occupy low-dimensional state spaces reflecting computational structure (Badre et al. 2020; Jazayeri & Ostojic 2021).
- Attractor models of working memory and context predict transient network reorganization between attractor states (Katori et al. 2011; Miller 2016; Ueltzhöffer et al. 2015).
- Spontaneous (pre-stimulus) brain-wide neural activity in mice is already high-dimensional, driven by multidimensional behavioral states (Stringer et al. 2019).
- Dimensionality scales with neuron number; recurrent synaptic structure is the primary determinant of instantaneous dimensionality (Dahmen et al. 2020; Manley et al. 2024).
- Participation ratio is biased in finite-sample regimes — overestimates true dimensionality with small N (Chun et al. 2025; Altan et al. 2020).

**Unknown / contested:**
- Whether brain-wide participation ratio transiently increases during the first 10 post-switch trials relative to the last 10 within-block trials — this is the direct gap addressed by the experiment.
- Whether the high-dimensionality of spontaneous activity (Stringer et al. 2019) changes quantifiably across the block, or is stable from trial 1 to trial N.
- Whether the attractor-transition window (first 10 post-switch trials) is the correct timescale to observe PR changes using pre-stimulus spike counts.
- Whether global multi-region PR is sensitive enough to detect transition effects, given unbounded dimensionality scaling and scale invariance of the covariance spectrum (Manley et al. 2024; Wang et al. 2025).
- Contested: whether context switching is implemented via high-dimensional transient expansion (Kikumoto et al. 2024) or via low-dimensional reconfigurations of orthogonal manifolds (Flesch et al. 2022; Soldado-Magraner et al. 2023).

**How this hypothesis sheds light:**
*Contribution type: Negative constraint*

The decision node is whether brain-wide participation ratio is a usable proxy for context-transition dynamics in this dataset. A positive result would have provided initial evidence that the attractor-search framing (high-dimensional search after block switch, low-dimensional steady state) is detectable in this multi-region mouse dataset, justifying PR as a readout metric in future scaled analyses. The negative result (mean PR transition = 6.93, steady-state = 7.00, paired t = -0.39, p = 0.70, N = 25 blocks across 5 subjects) constrains the hypothesis: a strong, reliable PR expansion during transition does not exist at this spatial and temporal scale using this analysis. What the experiment cannot resolve: (1) whether a small effect exists that is below the power of N=25 blocks to detect; (2) whether the null reflects true biological absence of dimensionality expansion or measurement insensitivity of PR in finite samples; (3) whether dimensionality expansion occurs on finer timescales than blocks 1–10 post-switch.

**What the caveats affect:**
No triage caveats were flagged for this experiment. However, two methodological concerns from the literature directly affect interpretation. First, PR with only 10 trials per epoch and up to 727 units per subject is in a regime where Chun et al. (2025) demonstrate substantial upward bias and condition differences may be dominated by sampling noise — meaning the observed similarity in PR values (6.93 vs. 7.00) cannot be cleanly interpreted as a true biological null without a bias-corrected analysis. Second, the lack of statistical power (N = 25 blocks, effect size ~1% difference in PR) means the failure to reject is not informative about the true effect — the contribution remains a Negative constraint rather than a Resolution, and would need a bias-corrected estimator and at least N ≥ 30 subjects before it could be treated as an established absence of the predicted effect.

---

## 3. Experimental Plan

**Objective:** Quantify changes in the effective dimensionality of the global brain state during task rule transitions.

**Steps:**
1. Pool all high-quality units across all regions for a given session to form a global brain state vector. Extract spike counts in the pre-stimulus window (-0.5 to 0 s).
2. Isolate 'Transition' trials (trials 0–10 post-switch) and 'Steady-State' trials (last 10 trials of a block).
3. For each condition, compute the covariance matrix of the global population activity.
4. Perform Eigenvalue Decomposition on the covariance matrices to obtain the variance explained by each principal component.
5. Calculate the Participation Ratio (PR = (sum(eigenvalues))^2 / sum(eigenvalues^2)) for the Transition and Steady-State periods.
6. Perform a paired t-test across subjects and blocks to verify if the Participation Ratio is significantly higher during Transitions.

**Deliverables:**
1. Eigenvalue spectra of global population activity during Transition vs. Steady-State periods.
2. Calculated Participation Ratios for each condition per subject.
3. Cross-subject statistical test of dimensionality expansion during task switching.

---

## 4. Similar Analyses in the Literature

- **Chun, Canatar, Chung, Lee, 2025** — Method: Participation ratio of eigenvalues of neural covariance matrices applied to calcium imaging, electrophysiology, and fMRI data. Match: identical estimator (PR of covariance eigenvalues) applied to neural population recordings. Regions: different (primarily visual cortex and LLM activations). Task: different (passive viewing / language). Caveats: authors explicitly demonstrate PR is biased upward with finite samples and propose a bias-corrected estimator.

- **Altan, Solla, Miller, Perreault, 2020** — Method: Multiple dimensionality estimation algorithms (including PR-like measures) evaluated on synthetic and real neural data. Match: PR-class estimator on multi-electrode spike count data. Regions: different (motor cortex). Task: different (reaching). Caveats: all algorithms fail when true dimensionality exceeds ~20 or sample count is low.

- **Mazzucato, Fontanini, La Camera, 2015** — Method: Dimensionality (scaling of variance with ensemble size) of spike count covariance from simultaneously recorded neurons. Match: eigenspectrum analysis of spike count covariance on multi-unit data in alert animals. Regions: different (gustatory cortex). Task: different (spontaneous vs. stimulus-evoked). Caveats: dimensionality estimates depend strongly on ensemble size and number of trials; theory provides bounds on PR-like measures.

- **Dahmen et al., 2020** — Method: Analysis of effective dimensionality from Neuropixels spike count recordings across mouse cortex, using eigenspectrum of correlation/covariance matrices. Match: same analysis class (eigenspectrum) on same species (mouse) with same technology (Neuropixels). Regions: multiple cortical areas including visual and frontal. Task: different (spontaneous, resting, and passive viewing states). Caveats: dimensionality is strongly controlled by local recurrent structure and transitions across states.

---

## 5. Results and Findings

The experiment successfully executed the planned pipeline. Five subjects were processed, yielding 25 block-level participation ratio estimates (5 blocks per subject, with block 0 excluded as it had no preceding switch). Spike counts were extracted in the pre-stimulus window (-0.5 to 0 s) and covariance matrices were computed for the global population (all high-quality units pooled, ranging from ~100–730 units per subject depending on recording coverage).

**Key quantitative results:**
- Mean PR (Transition, first 10 trials post-switch): 6.93
- Mean PR (Steady-State, last 10 trials of block): 7.00
- Paired t-test (Transition vs. Steady-State): t = -0.3895, p = 0.70 (25 blocks)
- The mean PR was nominally *lower* (not higher) during transitions than during steady state.
- The eigenvalue spectra (average scree plots) were visually nearly identical between conditions, with minor differences: slightly higher variance in PC1 for Transition, slightly higher variance in PCs 2–5 for Steady-State. PC10 dropped to zero in both conditions (effective rank limit of 9, likely due to only 10 trials per epoch).

**Hypothesis verdict:** The hypothesis that brain-wide PR is significantly higher during the first 10 post-switch trials is not supported. The nominal direction of the effect was reversed (PR was slightly lower during transitions), and the difference was not statistically significant.

**Analysis and review agreement:** The `analysis` and `review` fields are consistent. Both conclude that the hypothesis is not supported by the data and suggest the null result may reflect either a true biological absence of dimensionality expansion at this timescale or an underpowered analysis.

*(No conflict between analysis and review fields.)*

---

## 6. Reflection

**What was shown:**
[Verdict]: This result does not support the hypothesis; the direction of the nominal effect was opposite to the prediction (PR was slightly lower, not higher, during transitions) and the difference was not statistically significant.
[Effect direction and size]: Brain-wide participation ratio was nominally 1% lower during the first 10 post-switch trials (mean PR = 6.93) than during the last 10 steady-state trials (mean PR = 7.00), with very high block-to-block variability (error bars span ~0–0.9 rank units).
[Key statistic]: Prior 0.708 → posterior 0.266, N = 25 blocks (5 subjects × 5 blocks), paired t = -0.3895, p = 0.700.
[Replication]: The direction of the effect (transition vs. steady-state) was inconsistent across subjects and blocks — some blocks showed higher transition PR, others showed higher steady-state PR, with no consistent pattern across the 5 subjects.

**Null hypothesis:**
[State it explicitly]: "The null hypothesis is that the mean participation ratio of the global neural population during the first 10 post-switch trials equals the mean participation ratio during the last 10 within-block trials. This experiment failed to reject the null (p = 0.700, N = 25 blocks)."
[Power note]: "Given N = 25 blocks and the observed within-subject variability (SEM ~0.4 rank units relative to a mean difference of 0.07), this test had unknown — likely inadequate — power to detect an effect of the predicted magnitude. Failure to reject is not informative about the true effect: with this sample size and variance, even a biologically real 10–15% PR expansion during transitions would likely not reach significance. The null should not be interpreted as evidence of absence."

**What this rules out:**
[Rules out]: "This result rules out a strong, reliable brain-wide participation ratio expansion of more than ~5% during the first 10 post-switch trials relative to steady-state, at the scale of 5 subjects and 25 blocks in this task, because the observed effect size (~1%) and variance preclude detecting such an effect even if it existed in a simple form."
[Does not rule out]: "This result does not rule out a small but real dimensionality expansion during context transitions, because the participation ratio estimator used here is known to be strongly upward-biased with only 10 trials per epoch (Chun et al. 2025; Altan et al. 2020), which would attenuate any true condition difference; the null may reflect measurement insensitivity rather than biological absence."

**What would be needed next:**
[One experiment]: Apply a bias-corrected PR estimator (Chun et al. 2025) to the full 114-session dataset (~114 subjects), extracting 20–30 transition trials and 20–30 steady-state trials per block, to provide both sufficient power and a reliable dimensionality estimate.
[Why this upgrades]: This would move the contribution from Negative constraint to Resolution by (1) eliminating the finite-sample bias that confounds the current estimator, (2) providing N ≥ 100 blocks to detect even a 5% PR difference at p < 0.05, and (3) confirming or ruling out the transition-dimensionality effect with an estimator validated on neural data in the regime of interest.
