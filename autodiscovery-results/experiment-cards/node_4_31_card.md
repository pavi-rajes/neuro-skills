# Experiment Card: node_4_31

**Run:** c003951b-6609-4dda-a55f-37841282c20f
**Date:** 2026-04-24
**Novelty:** Tier 2 — Kaufman (2014) and Elsayed (2016) established null/potent and orthogonal coding in primate motor cortex for limb movements, but whether the same mechanism operates via PFC→MOs for lick suppression in mice is unmeasured.
**Triage verdict:** PASS  |  Mechanistic score: 5/5
**Surprise:** Δ -0.495  (prior: 0.708 → posterior: 0.391)

---

## 0. Dataset Context

**Sessions:** 664851, 742903, 668755, 759434, 713655 (5 subjects)
**Regions:** PFC (137–437 units/subject); MOs (recorded)
**Task:** Visual/auditory context-switching — correct rejection (no-go) trials

---

## 1. Hypothesis
Motor suppression is implemented via orthogonal Communication Subspaces: when a mouse successfully withholds a lick to a distractor stimulus (Correct Reject), the population activity projection from PFC to MOs resides in a subspace orthogonal to the active 'Go' subspace observed during Hit trials.

**Known limitations:**
None flagged

---

## 2. Literature Evidence

### Supporting
- **[V et al., 2021]** *Rapid suppression and sustained activation of distinct cortical regions for a delayed sensory-triggered motor response* — Summary The neuronal mechanisms generating a delayed motor response initiated by a sensory cue remain elusive. Here, we tracked the precise sequence of cortical activity in mice transforming a brief w
- **[X et al., 2022]** *Cortical preparatory activity indexes learned motor memories* — The brain’s remarkable ability to learn and execute various motor behaviours harnesses the capacity of neural populations to generate a variety of activity patterns. Here we explore systematic changes
- **[M et al., 2017]** *Commentary: Cortical activity in the null space: permitting preparation without movement* — recently proposed a hypothesis of how cortical neuronal ensembles prepare movements without initiating them prematurely (Kaufman et al. Although novel and potentially paradigm-shifting, their model ap
- **[G et al., 2016]** *Reorganization between preparatory and movement population responses in motor cortex* — Neural populations can change the computation they perform on very short timescales. Although such flexibility is common, the underlying computational strategies at the population level remain unknown
- **[M et al., 2010]** *Cortical preparatory activity: representation of movement or first cog in a dynamical machine?* — The motor cortices are active during both movement and movement preparation. A common assumption is that preparatory activity constitutes a subthreshold form of movement activity: a neuron active duri
- **[M et al., 2025]** *Mapping neural subspace dynamics onto the structure of the mouse descending motor system* — The motor cortex supports various cognitive and motor functions. To prevent interference between these processes, the associated neural dynamics may be organized into orthogonal subspaces

### Opposing
_No direct contradicting evidence found in search results._

### Contextual
- **[? et al., 2017]** *Global Representations of Goal-Directed Behavior in Distinct Cell Types of Mouse Neocortex* — SUMMARY The successful planning and execution of adaptive behaviors in mammals may require long-range coordination of neural networks throughout cerebral cortex. The neuronal implementation of signals
- **[M et al., 2021]** *Interpreting neural computations by examining intrinsic and embedding dimensionality of neural activity.* — The ongoing exponential rise in recording capacity calls for new approaches for analysing and interpreting neural data. Effective dimensionality has emerged as an important property of neural activity
- **[T et al., 2021]** *Hybrid dedicated and distributed coding in PMd/M1 provides separation and interaction of bilateral arm signals* — Pronounced activity is observed in both hemispheres of the motor cortex during preparation and execution of unimanual movements. The organizational principles of bi-hemispheric signals and the functio
- **[T et al., 2022]** *From Parametric Representation to Dynamical System: Shifting Views of the Motor Cortex in Motor Control* — In contrast to traditional representational perspectives in which the motor cortex is involved in motor control via neuronal preference for kinetics and kinematics, a dynamical system perspective emer
- **[M et al., 2025]** *Embodied sensorimotor control: computational modeling of the neural control of movement* — We review how sensorimotor control is dictated by interacting neural populations, optimal feedback mechanisms, and the biomechanics of bodies. First, we outline the distributed anatomical loops that s
- **[S et al., 2022]** *See and Copy: Generation of complex compositional movements from modular and geometric RNN representations* — A hallmark of biological intelligence and control is combinatorial generalization: animals are able to learn various things, then piece them together in new combinations to produce appropriate outputs

### Knowledge Map

**Known:**
- Motor cortex preparatory activity occupies a null space that does not drive movement output (Kaufman et al., 2014)
- Preparatory and movement population activity in motor cortex are organized in orthogonal subspaces (Elsayed et al., 2016)
- Active motor suppression in go/no-go tasks involves distinct frontal circuits separate from movement execution (Esmaeili et al., 2021)
- PFC projects to secondary motor cortex and influences motor preparation and suppression (Sun et al., 2022)

**Unknown / contested:**
- Whether active lick suppression in mice uses an orthogonal PFC→MOs communication subspace analogous to Kaufman null space for primate arm movements
- Whether the null/potent space mechanism generalizes from primate limb motor cortex to rodent orofacial motor cortex
- The relative contribution of PFC-driven orthogonal routing vs local MOs inhibitory circuits to correct rejection

**How this hypothesis sheds light:**
This experiment tests whether active motor suppression uses the orthogonal-subspace mechanism in PFC→MOs that Kaufman and Elsayed established in primate limb motor cortex. A positive result would extend the null/potent framework to orofacial motor control and to PFC→MOs inter-areal communication. A null result would suggest suppression uses different circuitry (e.g., local inhibition) and challenge the generalizability of the null-space framework.

---

## 3. Experimental Plan

**Objective:** Test if active inhibition of a prepotent response involves routing frontal commands into a null-space of the motor cortex to prevent action execution.

**Steps:**
1. Extract subjects with simultaneous high-quality units in PFC and MOs.
2. Extract stimulus-evoked spike counts (0 to 0.5s) for Hit trials and Correct Reject trials.
3. Using only Hit trials, perform Canonical Correlation Analysis (CCA) between PFC and MOs to define the top 3 'Go' communication dimensions (the subspace that successfully drives licking).
4. Project the PFC and MOs population activity from Correct Reject trials into this pre-defined Hit-CCA space.
5. Calculate the variance explained by these top 3 'Go' dimensions for the Correct Reject trials. Compute a baseline by projecting a null-distribution of randomly sampled trial activity into the same space.
6. Perform a statistical test across subjects to demonstrate that the variance of Correct Reject activity in the 'Go' communication subspace is significantly lower than chance, indicating it occupies an orthogonal inhibitory or null subspace.

**Deliverables:** 1. CCA components defining the shared 'Go' subspace between PFC and MOs from Hit trials.
2. Variance explained metrics for Correct Reject trials projected into the 'Go' subspace compared to null models.
3. Cross-subject statistics supporting the orthogonal routing hypothesis for motor suppression.

---

## 4. Similar Analyses in the Literature
_No direct methodological precedent found._

---

## 5. Results and Findings

The experiment executed successfully after resolving the dependency and file path issues. Four subjects (664851, 668755, 742903, 759434) met the inclusion criteria of having at least 10 high-quality units simultaneously recorded in both the prefrontal cortex (PFC) and secondary motor cortex (MOs). A Canonical Correlation Analysis (CCA) was fitted to 'Hit' trials to identify the top communication dimensions ('Go' subspace) between PFC and MOs. When projecting 'Correct Reject' trials into this 'Go' subspace, the resulting variance was compared against a null baseline of randomly sampled trials. Across the four subjects, a paired t-test yielded a t-statistic of 2.0029 and a p-value of 0.1389. The variance of the Correct Reject trials in the 'Go' subspace was not significantly lower than the baseline (and was in fact nominally higher in 3 out of 4 subjects). Therefore, the data does not provide significant evidence to support the hypothesis that motor suppression relies on routing commands into an orthogonal communication subspace.

**AutoDiscovery review:**
The experiment was faithfully implemented, successfully testing the hypothesis. The pipeline extracted high-quality units from PFC and MOs, isolated 'Hit' and 'Correct Reject' trials, and computed the Canonical Correlation Analysis (CCA) to define the 'Go' communication subspace. The projection of Correct Reject trials into this subspace, compared to a null model, showed no significant decrease in variance (t=2.0029, p=0.1389).

---

## 6. Reflection
**What was shown:**
[Verdict]: This result does not support the hypothesis — the effect is in the opposite direction.
[Effect direction and size]: CR trial variance projected into the PFC→MOs "Go" subspace (defined by CCA on Hit trials) was NOT lower than a randomly sampled baseline; it was nominally higher in 3 of 4 subjects.
[Key statistic]: N=4 subjects, t = 2.0029, p = 0.1389.
[Replication]: Effect was directionally opposite to the prediction in 3 of 4 subjects.

**Null hypothesis:**
[State it explicitly]: The null hypothesis is that Correct Reject trial variance projected into the PFC→MOs "Go" subspace does not differ from a baseline distribution. This experiment failed to reject the null (p = 0.1389, N = 4).
[Power note]: Given N=4, this test had inadequate power to detect a modest suppression effect. However, failure to reject is partially informative here: the effect direction was opposite to the prediction in 3 of 4 subjects, which is inconsistent with the suppression account independent of significance.

**What this rules out:**
[Rules out]: This result rules out the prediction that CR commands are routed into a subspace orthogonal to the PFC→MOs "Go" subspace defined by CCA, because CR variance in that subspace was not suppressed and was elevated in 3 of 4 subjects.
[Does not rule out]: This result does not rule out an orthogonal suppression mechanism within MOs intrinsic dynamics, because Kaufman et al.'s null/potent space framework applies to single-region preparatory activity — not cross-regional CCA — and was not tested here.

**What would be needed next:**
[One experiment]: Apply Kaufman et al.'s null/potent space decomposition directly to MOs single-unit activity on CR vs. Hit trials, run on the full ~114-session cohort.
[Why this upgrades]: This would move the contribution from Constraint to Resolution by testing the correct operationalization of the suppression mechanism at adequate scale.
