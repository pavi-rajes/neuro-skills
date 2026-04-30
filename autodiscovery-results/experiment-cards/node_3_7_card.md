# Experiment Card: node_3_7

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — Noise correlations as a context-dependent coupling measure between AUD and MOs during block-based context switching in mice have not been reported; the AUD-MOs circuit is unstudied in this paradigm, making this a predicted-but-unmeasured effect.
**Contribution type:** Constraint
**Triage verdict:** PASS  |  Mechanistic score: 3/5

---

## 0. Dataset Context

Sessions: 664851, 742903, 668755, 759434, 713655 (5 subjects enrolled; 2 usable for this analysis)
Regions: AUD (96–264 task-relevant units, subjects 664851 and 713655 only), MOs (57–77 lick-selective units, subjects 664851 and 713655 only); subjects 742903, 668755, 759434 had zero AUD units and were excluded
Task: Visual/auditory context-switching licking task (Allen Institute Dynamic Routing dataset, mice)

---

## 1. Hypothesis

The functional coupling between Auditory Cortex (AUD) and Secondary Motor Cortex (MOs) dynamically increases during Auditory blocks via enhanced cross-region noise correlations between task-relevant units, supporting the Gain Modulation framework.

**Known limitations:** None flagged at triage (flags list empty). However, code_output reveals that 3 of 5 subjects had zero AUD units, reducing effective N to 2 — a severe data-sparsity issue that substantially limits interpretability regardless of the sign of the result.

---

## 2. Literature Evidence

### Supporting

- **Cohen & Newsome (2008)** *Context-dependent changes in functional circuitry in visual area MT* — Noise correlations between pairs of MT neurons change with behavioral context (task type), validating spike-count noise correlations as a sensitive metric of context-dependent inter-areal functional coupling. *(analogical-circuit: same task concept, different regions)*

- **Ruff & Cohen (2016)** *Attention Increases Spike Count Correlations between Visual Cortical Areas* — Directing spatial attention increases spike-count noise correlations between V4 and MT; inter-areal noise correlations can increase—not only decrease—with top-down cognitive modulation, directly supporting that AUD-MOs coupling could increase during the attended context. *(analogical-circuit)*

- **van den Brink et al. (2022)** *Flexible Sensory-Motor Mapping Rules Manifest in Correlated Variability of Stimulus and Action Codes* — Flexible sensory-motor mapping rules reconfigure correlated variability between sensory and motor brain regions in humans switching between arbitrary stimulus-action mappings. Most directly analogous paper found: same general circuit type (sensory-motor), same paradigm type (context switching). *(analogical-task: sensory-motor, humans)*

- **Dehaqani et al. (2018)** *Selective Changes in Noise Correlations Contribute to an Enhanced Representation of Saccadic Targets in Prefrontal Cortex* — Selective changes in noise correlations among prefrontal ensembles contribute to enhanced representation of task-relevant targets, showing that context-relevant noise correlation changes are task-specific and improve coding. *(analogical-task)*

- **Kuchibhotla et al. (2016)** *Parallel processing by cortical inhibition enables context-dependent behavior* — In mice switching between passive and active auditory tasks, auditory cortex neurons are suppressed or facilitated context-dependently via inhibition, establishing that AUD functional coupling is dynamically reconfigured in mice by behavioral context. *(analogical-task: mice, AUD, context switching)*

- **Carcea et al. (2017)** *Dynamics of auditory cortical activity during behavioural engagement and auditory perception* — Behavioral engagement bidirectionally modulates auditory cortex single-trial variability and tuning curves in rats, showing that task engagement changes noise statistics relevant to noise correlation computation. *(analogical-task)*

### Opposing

- **Cohen & Maunsell (2009)** *Attention improves performance primarily by reducing interneuronal correlations* — The canonical mechanism by which task engagement improves sensory coding is by *decreasing* noise correlations within area, not increasing them; this is the direction opposite to the hypothesis, and the V4 within-area effect is the dominant finding in the field. *(analogical-circuit)*

- **Srinath et al. (2021)** *Attention improves information flow between neuronal populations without changing the communication subspace* — In MT-to-SC inter-areal coupling, attention improves information flow without changing noise correlation structure; gain modulation (increased drive) rather than noise correlation reorganization is the mechanism. This directly challenges the hypothesis that noise correlations are the primary signal of AUD-MOs routing. *(analogical-circuit)*

- **Ito et al. (2019)** *Task-evoked activity quenches neural correlations and variability across cortical areas* — Large-scale task engagement generally quenches inter-region correlations; if AUD-MOs coupling increases during auditory blocks, it would be a region-specific exception requiring specific mechanistic explanation, not a general phenomenon. *(analogical-circuit)*

- **Poort & Roelfsema (2008)** *Noise Correlations Have Little Influence on the Coding of Selective Attention in Area V1* — Noise correlations in V1 have little influence on decoding attentional signals; attention can be read out from population activity without changes in correlation structure, casting doubt on whether noise correlations are necessary for or indicative of routing. *(analogical-circuit)*

- **Yu et al. (2022)** *From correlation to communication: Disentangling hidden factors from functional connectivity changes* — Context-dependent correlation changes can reflect global state shifts or shared non-local inputs rather than specific pairwise communication; cross-region noise correlations between AUD and MOs may reflect arousal state rather than AUD-MOs-specific coupling. *(methodological skeptic)*

### Contextual

- **Averbeck et al. (2006)** *Neural correlations, population coding and computation* — Foundational review: noise correlations can help or hurt population coding depending on sign, magnitude, and relationship to tuning; provides the theoretical framework for why cross-region noise correlation changes are worth measuring.

- **Cohen & Kohn (2011)** *Measuring and interpreting neuronal correlations* — Seminal methods paper establishing r_sc as the standard metric for inter-neuronal functional coupling; note confounds including shared neuromodulatory input and global arousal.

- **Moreno-Bote et al. (2014)** *Information-limiting correlations* — Only 'information-limiting' correlations (aligned with the signal axis) actually limit coding; not all context-dependent correlation changes improve information transfer, relevant to interpreting any observed AUD-MOs change.

- **Weiss & Coen-Cagli (2024)** *Measuring Stimulus Information Transfer Between Neural Populations through the Communication Subspace* — Proposes a framework for quantifying how inter-areal noise correlations affect stimulus information transfer; directly relevant to next-step interpretation of AUD-MOs noise correlation results.

- **Shi et al. (2022)** *Cortical state dynamics and selective attention define the spatial pattern of correlated variability* — Cortical state (arousal) is a major driver of noise correlation structure and can confound context-dependent changes attributed to selective routing; suggests arousal should be tracked.

- **Semedo et al. (2021)** *Feedforward and feedback interactions between visual cortical areas use different population activity patterns* — Feedforward and feedback signaling between V1/V2 use distinct population activity patterns; pairwise noise correlations may be insufficient to characterize directed inter-areal communication.

- **Atiani et al. (2009)** *Task difficulty and performance induce diverse adaptive patterns in gain and shape of primary auditory cortex receptive fields* — Task difficulty modulates gain and receptive field shape in AUD; establishes auditory cortex undergoes gain-modulation-like changes during task engagement.

- **Polterovich et al. (2024)** *Task-related activity in auditory cortex enhances sound representation* — Many AUD neurons show large slow non-sensory firing rate modulations locked to task time points; these could confound noise correlation calculations if not fully captured by PSTH subtraction.

- **Saproo & Serences (2014)** *Attention Improves Transfer of Motion Information between V1 and MT* — Attention increases coupled BOLD activation between V1 and MT for attended stimuli in humans; analogical evidence that inter-areal functional coupling increases for task-relevant modality.

### Knowledge Map

**Known:**
- Behavioral context modulates noise correlations within auditory cortex and between sensory areas in visual circuits; direction depends on whether within-area (typically decrease) or cross-area (can increase) (Cohen & Maunsell 2009; Ruff & Cohen 2016; Kuchibhotla et al. 2016; Carcea et al. 2017)
- Correlated variability between sensory and motor regions changes with context-dependent sensory-motor mapping in humans (van den Brink et al. 2022)
- Task engagement generally quenches large-scale inter-region correlations (Ito et al. 2019)
- Noise correlations are an established coupling metric but confounded by global arousal state (Cohen & Kohn 2011; Shi et al. 2022)

**Unknown / contested:**
- Whether AUD-MOs cross-region noise correlations specifically increase during auditory blocks has not been directly measured in any species or paradigm
- Whether noise correlations or communication subspace geometry is the primary substrate of context-dependent sensory-motor coupling is an open question (Srinath et al. 2021 vs. van den Brink et al. 2022)
- What proportion of context-dependent noise correlation changes reflects specific AUD-MOs routing vs. global arousal changes (Shi et al. 2022)
- Whether gain modulation (same subspace, more drive) or subspace rotation is the dominant mechanism of context-dependent routing in the AUD-MOs pathway

**How this hypothesis sheds light:**
*Contribution type: Constraint*

This experiment addresses the specific gap of whether AUD-MOs functional coupling (measured via noise correlations) is context-dependent in mice performing a visual/auditory context-switching task. The decision node is: should future experiments measuring AUD-MOs routing use noise correlations or communication subspace geometry as their primary readout? A positive result would have established, for the first time, that AUD-MOs noise correlations track behavioral context in this specific circuit, providing empirical grounding for the Gain Modulation interpretation. The observed null result (t = 0.616, p = 0.649, N = 2) rules out the strong version of the Gain Modulation hypothesis — that mean AUD-MOs noise correlations are detectably higher during auditory blocks — at this sample size and effect resolution. However, the experiment is a Constraint, not a Resolution, because: (1) N=2 subjects with AUD recordings gives near-zero power to detect realistic effect sizes (typical r_sc differences ~ 0.001–0.005); (2) three of five subjects lacked AUD recordings entirely; (3) noise correlations are an indirect coupling measure that cannot distinguish AUD-MOs-specific routing from global arousal-driven shared variability. Even a positive result would not confirm that noise correlations are the mechanism of context-dependent routing vs. being an epiphenomenon.

**What the caveats affect:**
No triage caveats were formally flagged (flags list is empty). However, the code_output reveals a critical implicit caveat: 3 of 5 enrolled subjects (742903, 668755, 759434) had zero AUD units, reducing effective N to 2. This was not caught at triage because the unit count threshold was met at the dataset level, not per subject. A paired t-test with N=2 subjects has approximately 8% power to detect a correlation difference of d=0.5 at alpha=0.05, making the null result almost completely uninformative about the true effect. This caveat limits the knowledge-map interpretation to: the experiment provides a feasibility assessment, not an evidentiary contribution to the question of AUD-MOs coupling. The contribution type remains Constraint (not Negative constraint) because the design is underpowered.

---

## 3. Experimental Plan

**Objective:** Test whether trial-by-trial shared variability (noise correlations) between sensory and motor populations is modulated by behavioral context.

**Steps:**
1. Extract high-quality units from AUD and MOs.
2. Identify stimulus-selective units in AUD (significant difference in evoked rate between target and non-target tones) and lick-selective units in MOs (significant peri-response activity).
3. Compute trial-by-trial spike counts for these units during the stimulus window (0 to 0.5s).
4. Subtract the trial-type specific PSTH from each unit's spike count to obtain the residual spike counts (noise).
5. Compute the Pearson correlation of these residual spike counts between all pairs of AUD stimulus-selective and MOs lick-selective units.
6. Average the pair-wise noise correlations separately for Auditory blocks and Visual blocks.
7. Use a paired t-test across subjects to verify if AUD-MOs noise correlations are significantly higher during Auditory blocks.

**Deliverables:**
1. Identified task-relevant unit populations in AUD and MOs.
2. Matrices of cross-region spike-count noise correlations for Auditory and Visual blocks.
3. Statistical analysis demonstrating context-dependent restructuring of functional connectivity.

---

## 4. Similar Analyses in the Literature

- **Cohen & Newsome (2008)** — Method: spike-count noise correlations (r_sc) between pairs of MT neurons computed separately per task context. Match: same estimator class (pairwise Pearson r_sc of residuals from trial-type mean), same PSTH-subtraction approach. Regions: different (MT, not AUD/MOs). Task: different (perceptual context switching in macaque). Caveats: authors note that low N pairs (n ~ 20–50 per session) limits sensitivity; context-dependent changes in mean firing can inflate or deflate r_sc independent of coupling changes.

- **Ruff & Cohen (2016)** — Method: spike-count noise correlations between V4 and MT pairs (inter-area r_sc). Match: cross-area pairwise noise correlation, same estimator class. Regions: different (V4-MT, not AUD-MOs). Task: different (spatial attention task). Caveats: inter-area noise correlations are noisier than within-area; spike-count windows of 200ms used (vs. 500ms here), potentially affecting estimate reliability.

- **van den Brink et al. (2022)** — Method: correlated variability between sensory and motor EEG/MEG population signals during flexible sensory-motor mapping. Match: same conceptual approach (correlated variability between sensory and motor populations, context-dependent). Regions: analogous (human EEG, not single-unit). Task: same type (context-switching sensory-motor mapping). Caveats: mesoscale (EEG), not single-unit; cannot extract pairwise r_sc; population-level correlations may reflect different mechanisms.

- **Dehaqani et al. (2018)** — Method: spike-count noise correlations among PFC neuron ensembles as function of target location. Match: same estimator, inter-area ensemble. Regions: different (PFC, not AUD-MOs). Task: different (saccadic target representation). Caveats: analysis within a single area's subpopulations, not cross-area; effect driven by spatial selectivity rather than temporal context block.

---

## 5. Results and Findings

The experiment successfully executed the full analysis pipeline. The code loaded trials and units parquet datasets, filtered for high-quality units, and excluded optotagging trials. Task-relevant units were identified in AUD and MOs for 2 of 5 subjects (664851: 143 AUD, 57 MOs units; 713655: 96 AUD, 77 MOs units). The three remaining subjects (742903, 668755, 759434) had zero AUD units and were excluded.

Trial-by-trial spike counts were computed for the 0–0.5s stimulus window, and residuals were obtained by subtracting the trial-type × block-specific PSTH from each unit's spike count. Mean cross-region noise correlations (AUD-MOs Pearson r_sc averaged over all unit pairs) were:

| Subject | Auditory block r_sc | Visual block r_sc |
|---------|---------------------|--------------------|
| 664851  | 0.002387            | 0.001972           |
| 713655  | 0.003427            | 0.003525           |

Paired t-test across 2 subjects: t = 0.616, p = 0.649. The p-value exceeds 0.05 by a wide margin. The numeric direction was mixed: subject 664851 showed slightly higher coupling during auditory blocks (difference +0.000415), while subject 713655 showed slightly higher coupling during visual blocks (difference −0.000098).

The analysis and review fields are consistent: both state that no statistically significant difference in functional coupling was found between auditory and visual blocks. The review notes that the implementation was faithful to the plan. There is no conflict between analysis and review fields.

*(No conflict between analysis and review fields.)*

---

## 6. Reflection

**What was shown:**
[Verdict]: This result does not support the hypothesis that AUD-MOs functional coupling increases during Auditory blocks.
[Effect direction and size]: Mean cross-region noise correlations were numerically tiny (r_sc ~ 0.002–0.004) and showed no consistent directional difference between auditory and visual blocks across the two analyzable subjects.
[Key statistic]: N=2 subjects, t=0.616, p=0.649; effect sizes: subject 664851 +0.000415, subject 713655 −0.000098.
[Replication]: Effect was inconsistent across the 2 subjects — one subject showed a small positive direction, one a small negative direction. Group result is not robust.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that mean cross-region spike-count noise correlations between task-relevant AUD units and lick-selective MOs units do not differ between Auditory and Visual context blocks. This experiment failed to reject the null (p = 0.649, N = 2).
[Power note]: Given N=2, this test had inadequate power to detect an effect of the predicted magnitude. With typical inter-areal noise correlation differences of d ~ 0.5, a paired t-test with N=2 has approximately 8% power at alpha=0.05. Failure to reject is not informative about the true effect — the result is consistent with both a genuine null and a real effect that the experiment lacked power to detect.

**What this rules out:**
[Rules out]: This result rules out a very large context-dependent increase in AUD-MOs noise correlations (effect size > 2 SD of the current data), because both subjects show r_sc values below 0.004 with no consistent auditory-block elevation.
[Does not rule out]: This result does not rule out a small-to-moderate context-dependent increase in AUD-MOs noise correlations (d ~ 0.3–1.0), because N=2 is severely underpowered and the effect direction was not even consistent across the two available subjects.

**What would be needed next:**
[One experiment]: Repeat the noise correlation analysis with N≥10 subjects that each have at least 10 high-quality AUD units and 10 MOs units simultaneously recorded; compute r_sc with identical PSTH-subtraction pipeline; use the current 2-subject pilot effect sizes to power an adequately sized replication.
[Why this upgrades]: This would move the contribution from Constraint to either Resolution (if effect detected) or Negative constraint (if null persists with adequate power), by ruling out the underpowered-null alternative explanation. The current result cannot distinguish "no effect" from "effect below the detection limit of N=2."
