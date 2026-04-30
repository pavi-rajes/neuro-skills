# Experiment Card: node_3_14

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — The gain modulation vs subspace geometry debate has precedent in V1/V2 (Semedo 2019, Srinath 2021), but whether VIS→MOs subspace geometry is fixed while gain varies in a context-switching task in mice has not been directly measured.
**Triage verdict:** PASS  |  Mechanistic score: 5/5
**Surprise:** Δ -0.641  (prior: 0.708 → posterior: 0.297)

---

## 0. Dataset Context

**Sessions:** 664851, 742903, 668755, 713655 (4 subjects)
**Regions:** VIS (recorded); MOs (recorded)
**Task:** Visual/auditory context-switching licking task (Allen DR dataset)

---

## 1. Hypothesis
Context-dependent Gain Modulation vs. Subspace Alignment in Sensory-Motor Routing: In subjects with simultaneous sensory (VIS or AUD) and secondary motor (MOs) recordings, the communication subspace (measured via Reduced-Rank Regression) between sensory cortex and MOs remains geometrically fixed across contexts. Instead of rotating, the magnitude of sensory population activity projected into this subspace is significantly amplified (Gain Modulation framework) when the sensory modality is the currently rewarded context compared to when it is unrewarded.

**Known limitations:**
None flagged

---

## 2. Literature Evidence

### Supporting
- **[J et al., 2019]** *Cortical Areas Interact through a Communication Subspace.* — Most brain functions involve interactions among multiple, distinct areas or nuclei. For instance, visual processing in primates requires the appropriate relaying of signals across many distinct cortic
- **[S et al., 1999]** *Feature-based attention influences motion processing gain in macaque visual cortex* — Changes in neural responses based on spatial attention have been demonstrated in many areas of visual cortex, indicating that the neural correlate of attention is an enhanced response to stimuli at an
- **[B et al., 2025]** *Reduced rank regression for neural communication: a tutorial for neuroscientists* — Reduced rank regression (RRR) is a statistical method for finding a low-dimensional linear mapping between a set of high-dimensional inputs and outputs. In recent years, RRR has found numerous applica
- **[O et al., 2024]** *Measuring Stimulus Information Transfer Between Neural Populations through the Communication Subspace* — Sensory processing arises from the communication between neural populations across multiple brain areas. While the widespread presence of neural response variability shared throughout a neural populat
- **[R et al., 2021]** *Attention improves information flow between neuronal populations without changing the communication subspace* — Visual attention allows observers to flexibly use or ignore visual information, suggesting that information can be flexibly routed between visual cortex and neurons involved in decision-making. We inv
- **[J et al., 2002]** *Attentional modulation strength in cortical area MT depends on stimulus contrast.* — The attentional modulation of sensory information processing in the visual system is the result of top-down influences, which can cause a multiplicative modulation of the firing rate of sensory neuron

### Opposing
_No direct contradicting evidence found in search results._

### Contextual
- **[V et al., 2013]** *Context-dependent computation by recurrent dynamics in prefrontal cortex* — Prefrontal cortex is thought to have a fundamental role in flexible, context-dependent behaviour, but the exact nature of the computations underlying this role remains largely unknown. In particular, 
- **[J et al., 2021]** *Feedforward and feedback interactions between visual cortical areas use different population activity patterns* — Brain function relies on the coordination of activity across multiple, recurrently connected brain areas. For instance, sensory information encoded in early sensory areas is relayed to, and further pr
- **[J et al., 2020]** *Statistical methods for dissecting interactions between brain areas* — The brain is composed of many functionally distinct areas. This organization supports distributed processing, and requires the coordination of signals across areas
- **[J et al., 2004]** *Attentional modulation of visual processing.* — Single-unit recording studies in the macaque have carefully documented the modulatory effects of attention on the response properties of visual cortical neurons. Attention produces qualitatively diffe
- **[L et al., 2023]** *Strong attentional modulation of V1/V2 activity implements a robust, contrast-invariant control mechanism for selective information processing* — When selective attention is devoted to one of multiple stimuli within receptive fields of neurons in visual area V4, cells respond as if only the attended stimulus was present. The underlying neural m
- **[B et al., 2025]** *Accurate Identification of Communication Between Multiple Interacting Neural Populations* — Neural recording technologies now enable simultaneous recording of population activity across many brain regions, motivating the development of data-driven models of communication between brain region

### Knowledge Map

**Known:**
- Cortical areas interact through low-dimensional communication subspaces that selectively transmit activity (Semedo et al., 2019)
- Attention modulates neural responses via multiplicative gain changes in sensory cortex (Treue & Martinez-Trujillo, 1999; Reynolds & Chelazzi, 2004)
- Reduced-rank regression identifies low-dimensional inter-areal communication axes (Semedo et al., 2020)
- Context-dependent computation in prefrontal cortex is implemented by recurrent dynamics (Mante et al., 2013)

**Unknown / contested:**
- Whether VIS→MOs communication subspace geometry rotates or stays fixed while gain varies across attend-visual vs attend-auditory blocks
- Whether gain modulation alone fully explains context-dependent sensory-motor routing in mice, or whether subspace re-alignment is also required
- Whether results from primate V1/V2 attention studies generalize to rodent sensory-motor routing circuits

**How this hypothesis sheds light:**
This experiment directly tests whether the VIS→MOs communication subspace rotates or stays fixed across attentional contexts. A positive result (fixed subspace, modulated gain) would be the first direct evidence in the rodent sensory-motor circuit that gain modulation — not geometric re-alignment — implements context-dependent routing. A null result (subspace rotates) would favor rotation-based theories.

---

## 3. Experimental Plan

**Objective:** Test whether cross-modal attention routes information via dynamic re-alignment of sensory-motor communication subspaces or via context-dependent gain modulation within a fixed subspace.

**Steps:**
1. Identify all subjects with at least 15 high-quality units (default_qc == True) in both a primary sensory area (e.g., any 'VIS' structure) and 'MOs'.
2. Bin spike counts in a 0 to 0.5s post-stimulus window.
3. Fit a single Reduced-Rank Regression (RRR) model (e.g., rank 5) predicting MOs activity from Sensory activity using trials from BOTH contexts to define a global 'fixed' communication subspace.
4. Project the trial-averaged Sensory population response to the preferred target stimulus into this fixed subspace separately for rewarded block trials and unrewarded block trials.
5. Compute the L2-norm (vector magnitude) of these projected representations.
6. Perform a paired t-test across valid subjects to determine if the projected magnitude is significantly higher in the rewarded context versus the unrewarded context.

**Deliverables:** 1. L2-norms of the sensory-to-motor subspace projections for rewarded and unrewarded contexts per subject.
2. Statistical results (paired t-test) across all qualifying subjects.

---

## 4. Similar Analyses in the Literature
_No direct methodological precedent found._

---

## 5. Results and Findings

The experiment successfully tested the context-dependent gain modulation hypothesis by analyzing neural recordings from 4 subjects that met the criteria of having at least 15 high-quality units in both the visual cortex (VIS) and the secondary motor cortex (MOs). A global Reduced-Rank Regression (RRR) model was fit to define a fixed communication subspace between VIS and MOs across all trials. The trial-averaged sensory population responses to the preferred target stimulus were then projected into this fixed subspace separately for rewarded and unrewarded contexts. The L2-norm magnitudes of these projections were compared across the subjects. The results showed varying baseline projection magnitudes across subjects (ranging from ~15 to ~32 L2 units) but no consistent or large differences between the contexts. A paired t-test yielded t = -0.7273 and p = 0.5197, indicating no statistically significant difference in the projected magnitudes between the rewarded and unrewarded contexts. Therefore, the data does not support the hypothesis that cross-modal attention routes information primarily via context-dependent gain modulation within a fixed sensory-motor communication subspace.

**AutoDiscovery review:**
The experiment was faithfully implemented and successfully executed the planned steps to test the hypothesis. 

**Hypothesis:** Cross-modal attention routes information via context-dependent gain modulation within a fixed sensory-motor communication subspace, such that sensory activity projected into the secondary motor cortex (MOs) subspace is amplified when the sensory modality is rewarded.

**Experiment Results:**
- The pipeline successfully identified 4 valid subjects with sufficient simultaneous high-quality unit recordings in both the visual cortex (VIS) and the secondary motor cortex (MOs).
- A Reduced-Rank Regression (RRR) model was fit using all trials to define a global, fixed communication subspace between VIS and MOs.
- The trial-averaged sensory population responses to the preferred visual target stimulus were projected into this subspace, partitioned by whether the visual modality was the rewarded context or the unrewarded (distractor) context.
- The L2-norm magnitudes of these projections were compared. The magnitudes ranged between ~15 and ~32 L2 units across subjects, showing significant inter-subject variability but minimal within-subject modulation across contexts.
- A paired t-test across the 4 subjects yielded no statistically significant difference between the rewarded and unrewarded contexts (t = -0.7273, p = 0.5197).

**Findings:**
The data does not support the Context-dependent Gain Modulation hypothesis for sensory-to-motor routing. The magnitude of the sensory population response projected into the fixed MOs communication subspace does not significantly scale up when the sensory modality becomes the task-relevant, rewarded context. This implies that cross-modal attention might rely on mechanisms other than simple gain modulation within a fixed subspace, such as dynamic subspace re-alignment or local computations within the prefrontal/motor areas themselves.

---

## 6. Reflection
**What was shown:**
[Verdict]: This result does not support the hypothesis.
[Effect direction and size]: VIS→MOs projected L2-norm magnitudes showed no consistent difference between rewarded and unrewarded contexts across subjects (values ranged ~15–32 units per subject but without directional consistency).
[Key statistic]: N=4 subjects, t = −0.7273, p = 0.5197.
[Replication]: Effect was not consistent across subjects — 3 of 4 showed no meaningful context-dependent difference in projection magnitude.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that context (rewarded vs. unrewarded) does not modulate the magnitude of VIS→MOs projections within a fixed communication subspace. This experiment failed to reject the null (p = 0.5197, N = 4).
[Power note]: Given N=4, this test had inadequate power to detect a small-to-medium effect. Failure to reject is not informative — the result is consistent with either no effect or an effect too small for N=4 to detect.

**What this rules out:**
[Rules out]: This result rules out a large, subject-consistent gain modulation within a fixed VIS→MOs communication subspace as the primary routing mechanism, because projected magnitudes did not differ directionally across contexts in N=4 subjects (p = 0.52, no consistent trend).
[Does not rule out]: This result does not rule out subspace rotation as an alternative routing mechanism, because the RRR design held the subspace fixed by construction — geometric changes between contexts were not measurable by this analysis.

**What would be needed next:**
[One experiment]: Fitting separate RRR models per context block and comparing principal subspace angles across attend-visual vs attend-auditory blocks, applied to the full ~114-session cohort.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by testing subspace rotation directly — the mechanism the fixed-subspace design could not address.
