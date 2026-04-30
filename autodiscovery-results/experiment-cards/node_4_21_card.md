# Experiment Card: node_4_21

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — Cohen & Maunsell (2009) showed noise correlations predict attention effects within areas, but whether pre-stimulus VIS-AUD inter-areal correlations predict false alarm errors in a cross-modal switching task has not been measured.
**Triage verdict:** PASS  |  Mechanistic score: 5/5
**Surprise:** Δ -0.106  (prior: 0.708 → posterior: 0.641)

---

## 0. Dataset Context

**Sessions:** 664851, 742903, 668755, 759434, 713655 (5 subjects)
**Regions:** AUD (16248–16248 units/subject); VIS (242–317 units/subject)
**Task:** Cross-modal context-switching — false alarm vs. correct rejection trial comparison

---

## 1. Hypothesis
False Alarm errors are caused by a transient failure to dynamically decouple competing sensory streams. In the pre-stimulus period immediately preceding a False Alarm trial, stimulus-independent cross-regional noise correlations between VIS and AUD neuron pairs are significantly higher than prior to a Correct Reject trial.

**Known limitations:**
None flagged

---

## 2. Literature Evidence

### Supporting
- **[Y et al., 2022]** *Cortical state dynamics and selective attention define the spatial pattern of correlated variability in neocortex* — Correlated activity fluctuations in the neocortex influence sensory responses and behavior. Neural correlations reflect anatomical connectivity but also change dynamically with cognitive states such a
- **[Y et al., 2022]** *Cortical state dynamics and selective attention define the spatial pattern of correlated variability in neocortex* — Correlated activity fluctuations in the neocortex influence sensory responses and behavior. Neural correlations reflect anatomical connectivity but also change dynamically with cognitive states such a
- **[B et al., 2024]** *Neural Dynamics Underlying False Alarms in Extrastriate Cortex* — The unfolding of neural population activity can be approximated as a dynamical system. Stability in the latent dynamics that characterize neural population activity has been linked with consistency in
- **[J et al., 2021]** *Revisiting Persistent Neuronal Activity During Covert Spatial Attention* — Persistent activity has been observed in the prefrontal cortex (PFC), in particular during the delay periods of visual attention tasks. Classical approaches based on the average activity over multiple
- **[N et al., 2020]** *Boosts in brain signal variability track liberal shifts in decision bias* — Adopting particular decision biases allows organisms to tailor their choices to environmental demands. For example, a liberal response strategy pays off when target detection is crucial, whereas a con
- **[E et al., 2009]** *Crossmodal Links between Vision and Touch in Spatial Attention: A Computational Modelling Study* — Many studies have revealed that attention operates across different sensory modalities, to facilitate the selection of relevant information in the multimodal situations of every-day life. Cross-modal 

### Opposing
_No direct contradicting evidence found in search results._

### Contextual
- **[G et al., 2010]** *Predictive Coding or Evidence Accumulation? False Inference and Neuronal Fluctuations* — Perceptual decisions can be made when sensory input affords an inference about what generated that input. Here, we report findings from two independent perceptual experiments conducted during function
- **[M et al., 2018]** *27th Annual Computational Neuroscience Meeting (CNS*2018): Part One* — This article is distributed under the terms of the Creative Commons Attribution 4. 0 International License (http://creat iveco mmons
- **[S et al., 2010]** *The Impact of Ongoing Brain Activity on the Variability of Human Brain Function and Behaviour* — Perceptual decisions can be made when sensory input affords an inference about what generated that input. Here, we report findings from two independent perceptual experiments conducted during function
- **[A et al., 2018]** *Learning and attention reveal a general relationship between population activity and behavior* — The neuronal population is the key unit The responses of pairs of neurons to repeated presentations of the same stimulus are typically correlated, and an identical neuronal population can perform many
- **[J et al., 2003]** *Continuous detection of weak sensory signals in afferent spike trains: the role of anti-correlated interspike intervals in detection performance* — An important problem in sensory processing is deciding whether fluctuating neural activity encodes a stimulus or is due to variability in baseline activity. Neurons that subserve detection must examin
- **[L et al., 2018]** *Moment-to-Moment Fluctuations in Neuronal Excitability Bias Subjective Perception Rather than Strategic Decision-Making* — Abstract Perceiving an external stimulus depends not only on the physical features of the stimulus, but also fundamentally on the current state of neuronal excitability, indexed by the power of ongoin

### Knowledge Map

**Known:**
- Noise correlations between neurons predict attentional state and behavioral accuracy in sensory cortex (Cohen & Maunsell, 2009)
- Pre-stimulus cortical state determines perceptual sensitivity and affects false alarm rates (Shi et al., 2022)
- Cross-modal attention requires competitive suppression between sensory streams; failures produce false alarms (Sahoo et al., 2024)
- Neural variability and cortical excitability fluctuations link to decision criterion shifts and error rates (Kloosterman et al., 2020)

**Unknown / contested:**
- Whether elevated VIS-AUD noise correlations specifically predict false alarms in a cross-modal switching task in mice
- Whether the decoupling mechanism is reflected in noise correlations vs mean firing rate differences
- Whether this is a consistent across-subject effect or dominated by subjects with high false alarm rates

**How this hypothesis sheds light:**
This experiment tests whether failure to reduce VIS-AUD noise correlations predicts false alarm errors. A positive result would provide the first evidence linking inter-areal VIS-AUD correlations to false alarms in a cross-modal task, extending Cohen & Maunsell's within-area findings to inter-areal decoupling. A null result would point to other sources (motor bias, decision threshold, local dynamics).

---

## 3. Experimental Plan

**Objective:** Quantify changes in VIS-AUD network noise correlations immediately preceding cross-modal attention errors compared to successful inhibitions.

**Steps:**
1. Identify all False Alarm (FA) and Correct Reject (CR) trials within 'trials.parquet'.
2. Extract pre-stimulus spike counts (-0.5s to 0.0s, single bin) for all high-quality units in VIS and AUD.
3. Compute the trial-averaged PSTH for FA and CR trials separately, and subtract it from the single-trial spike counts to isolate 'noise' (stimulus/context-independent variability).
4. Compute the pairwise Pearson correlation coefficient (noise correlation) between every VIS unit and every AUD unit across trials, yielding a cross-region noise correlation matrix for FA and CR conditions.
5. Compute the mean absolute cross-region noise correlation for FA and CR conditions for each subject.
6. Perform a paired t-test across subjects to determine if pre-stimulus VIS-AUD noise correlations are significantly elevated before FA errors.

**Deliverables:** 1. Cross-region (VIS-AUD) pairwise noise correlation matrices for FA and CR trials. 2. Mean noise correlation magnitudes per subject. 3. Statistical testing demonstrating whether cross-modal decoupling fails prior to False Alarms.

---

## 4. Similar Analyses in the Literature
_No direct methodological precedent found._

---

## 5. Results and Findings

The experiment successfully executed the pipeline to compute pre-stimulus cross-regional (VIS-AUD) noise correlations for False Alarm (FA) versus Correct Reject (CR) trials. 

**Results:** 
- The script identified 746 high-quality units across the VIS and AUD regions. However, only 2 out of the 5 subjects (664851 and 713655) had simultaneous high-quality recordings in both VIS and AUD regions, severely limiting the sample size for cross-subject statistical testing.
- For the two valid subjects, the mean absolute VIS-AUD noise correlations were consistently elevated prior to False Alarms (0.1017 and 0.1217) compared to Correct Rejects (0.0531 and 0.0555).
- A paired t-test across these two subjects yielded a t-statistic of 6.542 and a p-value of 0.097.

**Findings:** 
Although there is an observable trend where stimulus-independent noise correlations between visual and auditory cortices are approximately twice as high prior to a False Alarm error compared to a successful Correct Reject, the statistical test was extremely underpowered (n=2). Consequently, the difference did not reach the standard threshold for statistical significance (p < 0.05). While the trend directionally aligns with the hypothesis that errors stem from a failure to dynamically decouple competing sensory streams, the hypothesis cannot be formally supported due to the limited number of subjects with dual-region recordings.

**AutoDiscovery review:**
The experiment pipeline was faithfully implemented according to the plan. The data loading, filtering, spike counting, and correlation calculations were executed correctly. The analysis appropriately recognized the severe limitation in sample size (only 2 out of 5 subjects had simultaneous high-quality recordings in both visual and auditory regions), and accurately summarized the observed trends without making unsupported statistical claims.

---

## 6. Reflection
**What was shown:**
[Verdict]: This result is underpowered — no population-level inference is valid at N=2 effective subjects.
[Effect direction and size]: Pre-stimulus VIS–AUD noise correlations were ~2× higher before False Alarm trials (0.1017, 0.1217) than before Correct Reject trials (0.0531, 0.0555) in both qualifying subjects; only 2 of 5 subjects had simultaneous high-quality VIS and AUD recordings.
[Key statistic]: N=2 effective subjects, t = 6.542, p = 0.097.
[Replication]: Direction was consistent across both qualifying subjects, but N=2 renders the group test uninterpretable.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that pre-stimulus VIS–AUD noise correlations do not differ between False Alarm and Correct Reject trials. This experiment failed to reject the null (p = 0.097, N = 2 effective subjects).
[Power note]: Given N=2 effective subjects, this test had inadequate power — one degree of freedom makes the group test uninterpretable. Failure to reject is not informative; the bottleneck is simultaneous VIS–AUD recording coverage across subjects, not the absence of a signal.

**What this rules out:**
[Rules out]: This result rules out drawing any population-level conclusion about the decoupling failure account, because N=2 cannot support a group inference regardless of effect size.
[Does not rule out]: This result does not rule out the decoupling failure hypothesis itself, nor does it rule out that elevated noise correlations are downstream of arousal fluctuation (pupil-linked state) — an untested confound that independently predicts both higher noise correlations and more false alarms.

**What would be needed next:**
[One experiment]: Expand to the full ~114-session cohort to increase subjects with joint VIS–AUD coverage beyond 2, and include pre-stimulus pupil area as a covariate.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by separating the decoupling account from the arousal confound and providing a statistically valid group test.
