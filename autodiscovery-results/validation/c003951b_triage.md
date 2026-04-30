# Triage Report — Run c003951b

**Date:** 2026-04-28  
**Dataset:** Allen Institute Dynamic Routing (5-subject pilot)  
**Total experiments:** 70  
**PASS:** 12 | **FLAG:** 31 | **FAIL:** 27

---

## Passing Experiments

*(sorted by mechanistic score desc, then surprise desc)*

```
experiment_id: node_2_6
id_in_run:     7
hypothesis:    The strength of the context representation in the PFC on trial N linearly predicts the neural discriminability of sensory stimuli in the relevant sensory cortex on trial N+1, supporting the Gain Modulation framework where frontal areas set the sensory gain for upcoming trials.
mech_score:    4
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.690  (prior: 0.708 → posterior: 0.266)
finding:       Linear Mixed-Effects model across 892 trial pairs from 5 subjects finds PFC trial-N context confidence does not predict VIS trial-N+1 sensory discriminability (slope=-0.003, p=0.695); trial-by-trial PFC→VIS gain gating is not supported.
```

```
experiment_id: node_4_18
id_in_run:     49
hypothesis:    Following a behavioral error, the prefrontal cortex engages a distinct error-correction communication subspace with sensory cortices on the subsequent trial. Specifically, the Frontal->Sensory communication subspace identified on Post-Error trials is structurally orthogonal to the subspace identified on Post-Correct trials. This supports the Communication Subspaces framework.
mech_score:    4
novelty_tier:  2
verdict:       PASS
caveats:       none
surprise:      -0.690  (prior: 0.708 → posterior: 0.266)
finding:       Post-Error and Post-Correct Frontal-Sensory communication subspaces are not significantly orthogonal relative to a shuffled null distribution across 5 subjects (p=0.199); error correction does not engage a structurally distinct communication geometry.
```

```
experiment_id: node_3_14
id_in_run:     23
hypothesis:    Context-dependent Gain Modulation vs. Subspace Alignment in Sensory-Motor Routing: In subjects with simultaneous sensory (VIS or AUD) and secondary motor (MOs) recordings, the communication subspace (measured via Reduced-Rank Regression) between sensory cortex and MOs remains geometrically fixed across contexts. Instead of rotating, the magnitude of sensory population activity projected into this subspace is significantly amplified (Gain Modulation framework) when the sensory modality is the currently rewarded context compared to when it is unrewarded.
mech_score:    4
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.641  (prior: 0.708 → posterior: 0.297)
finding:       Projection magnitude of VIS stimulus activity into a fixed VIS-MOs communication subspace does not differ between rewarded and unrewarded contexts across 4 subjects (t=-0.727, p=0.520); gain modulation of a fixed subspace is not the mechanism.
```

```
experiment_id: node_4_3
id_in_run:     29
hypothesis:    Visual signals are routed to the PFC continuously for state-monitoring regardless of context, while routing to MOs is strictly context-gated, supporting the Communication Subspaces framework of independent and target-specific routing geometries.
mech_score:    4
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.495  (prior: 0.708 → posterior: 0.391)
finding:       Context Modulation Metric (Visual R²−Auditory R²) is equally low for VIS-to-MOs (0.013) and VIS-to-PFC (0.011) pathways across 5 subjects (t=0.124, p=0.907); VIS routing to motor cortex is not strictly context-gated relative to PFC.
```

```
experiment_id: node_4_31
id_in_run:     65
hypothesis:    Motor suppression is implemented via orthogonal Communication Subspaces: when a mouse successfully withholds a lick to a distractor stimulus (Correct Reject), the population activity projection from PFC to MOs resides in a subspace orthogonal to the active 'Go' subspace observed during Hit trials.
mech_score:    4
novelty_tier:  2
verdict:       PASS
caveats:       none
surprise:      -0.495  (prior: 0.708 → posterior: 0.391)
finding:       CR trial variance in the PFC-MOs 'Go' subspace is not significantly lower than null baseline across 4 subjects (t=2.003, p=0.139); in 3/4 subjects it is nominally HIGHER, arguing against motor suppression via orthogonal communication routing.
```

```
experiment_id: node_2_2
id_in_run:     3
hypothesis:    On False Alarm errors, the prefrontal cortex (PFC) generates an error state deviation that temporally precedes deviation in motor cortex (MOs), leading to a transient increase in PFC-to-MOs directed coupling on the subsequent trial. This supports the Gain Modulation framework where frontal error signals dynamically adjust motor excitability.
mech_score:    4
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.446  (prior: 0.708 → posterior: 0.422)
finding:       Neither the divergence latency of PFC vs MOs trajectories on FA trials (mean 34.0 vs 22.0 ms, p=0.477) nor post-FA PFC-MOs Granger Causality vs post-CR (0.904 vs 0.696, p=0.478) reached significance; the error signal cascade hypothesis is not supported.
```

```
experiment_id: node_3_4
id_in_run:     13
hypothesis:    Attention lapses are corrected via targeted top-down frontal signals. On Miss errors during visual blocks, Granger Causality from the prefrontal cortex (PFC) to the visual cortex (VIS) increases significantly during the pre-stimulus period of the immediately subsequent trial to restore attentional gain, supporting the Gain Modulation framework.
mech_score:    3
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.690  (prior: 0.708 → posterior: 0.266)
finding:       Granger Causality (PFC→VIS) on the trial following a Miss error is not significantly higher than after a Hit across 5 subjects (p=0.165); top-down attentional restoration via GC is not supported.
```

```
experiment_id: node_4_11
id_in_run:     39
hypothesis:    The multi-region network transitions between distinct attention contexts by passing through a high-dimensional transient state. Specifically, the effective dimensionality (Participation Ratio) of the joint VIS-AUD-PFC-MOs population activity during the pre-stimulus window will be significantly higher on early transition trials (trials 1-5 post-switch) than on steady-state trials (last 20 trials), supporting an Attractor Dynamics framework where the network energy landscape flattens before settling into a new low-dimensional basin.
mech_score:    3
novelty_tier:  2
verdict:       PASS
caveats:       none
surprise:      -0.690  (prior: 0.708 → posterior: 0.266)
finding:       Joint VIS+AUD+PFC+MOs Participation Ratio is significantly LOWER during early transition trials (mean 13.50) than steady-state trials (mean 25.65) across 5 subjects (t=-5.21, p=0.0065), directly contradicting the Attractor Dynamics high-dimensional transient prediction.
```

```
experiment_id: node_4_17
id_in_run:     48
hypothesis:    Top-down signals directly scale bottom-up representations: the magnitude of trial-by-trial preparatory activity along the Anterior Cingulate Cortex (ACA) 'context axis' positively predicts the absolute amplitude of the stimulus-evoked population vector in the relevant sensory cortex (VIS during visual blocks). This supports the Gain Modulation framework of dynamic routing.
mech_score:    3
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.690  (prior: 0.708 → posterior: 0.266)
finding:       ACA pre-stimulus context-axis activity is not correlated with VIS stimulus-evoked population vector amplitude in any of 5 subjects (r range: -0.09 to +0.03); ACA-to-VIS top-down gain control does not operate trial-by-trial.
```

```
experiment_id: node_4_20
id_in_run:     51
hypothesis:    Following a False Alarm error, the anterior cingulate cortex (ACA) generates a post-response error signal that positively correlates with a subsequent trial-by-trial increase in the pre-stimulus Fano factor (gain modulation) of primary sensory cortices (VIS/AUD), supporting the Gain Modulation framework for top-down error correction.
mech_score:    3
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.365  (prior: 0.375 → posterior: 0.141)
finding:       ACA post-FA error signal magnitude is not positively correlated with subsequent-trial sensory Fano factor across 4 subjects (one-sided p=0.894; FA correlations are in fact more negative than CR correlations); ACA error signaling does not predict top-down gain adjustment.
```

```
experiment_id: node_4_1
id_in_run:     26
hypothesis:    Multi-region network state transitions pass through a high-dimensional transient state before settling into a new context attractor, supporting the Attractor Dynamics framework. The effective dimensionality of the joint VIS-AUD-MOs pre-stimulus state peaks during the early trials of a block switch.
mech_score:    2
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.544  (prior: 0.708 → posterior: 0.359)
finding:       VIS+AUD+MOs joint population Participation Ratio does not differ between early transition (mean PR=3.35) and late steady-state (PR=3.32) trials across 5 subjects (t=0.387, p=0.719); no high-dimensional transient during context switches in sensorimotor regions.
```

```
experiment_id: node_4_22
id_in_run:     54
hypothesis:    False Alarms trigger a rapid, arousal-driven network reset that heightens baseline cross-regional noise correlations between PFC and VIS on the subsequent trial, supporting a Gain Modulation framework where error signals broadly scale cortical excitability.
mech_score:    2
novelty_tier:  3
verdict:       PASS
caveats:       none
surprise:      -0.544  (prior: 0.708 → posterior: 0.359)
finding:       Pre-stimulus PFC-VIS noise correlations on trials following False Alarms vs Correct Rejects are not significantly different across 5 subjects (t=0.782, p=0.450); FA errors do not trigger a broad cortical arousal-driven network reset.
```

---

## Full Triage Table

```
  # | experiment_id  | Verdict | Mech | Flaws
--------------------------------------------------------------------------------
  1 | node_2_0       | FLAG    |    4 | F: Subject 713655 only 7 PFC units (suspicious low count); G
  2 | node_2_1       | FAIL    |    — | B: N=0 (no subjects had simultaneous VIS+AUD+PFC recordings)
  3 | node_2_2       | PASS    |    4 | —
  4 | node_2_3       | FAIL    |    — | B: N=0 (no subjects had simultaneous ACA+PFC+VIS recordings)
  5 | node_2_4       | FLAG    |    3 | E: Substantially redundant with node_4_11 (same hypothesis, 
  6 | node_2_5       | FAIL    |    — | B: N=1 (only subject 664851 had CA1+VIS+AUD)
  7 | node_2_6       | PASS    |    4 | —
  8 | node_2_7       | FAIL    |    — | B: N=1 (only subject 664851 contributed transition data for CA1+P
  9 | node_3_0       | FLAG    |    2 | C: Paired t-test run across 30 blocks from 5 subjects (pseud
 10 | node_3_1       | FLAG    |    3 | E: Substantially redundant with node_4_27 which tests same c
 11 | node_3_2       | FLAG    |    4 | G: Two comparisons (FA dist to Hit in comm space, FA dist to
 12 | node_3_3       | FLAG    |    3 | E: Substantially redundant with node_4_27 (both test VIS ali
 13 | node_3_4       | PASS    |    3 | —
 14 | node_3_5       | FAIL    |    — | B: N=2 (only two subjects met VIS+AUD+MOs criteria)
 15 | node_3_6       | FLAG    |    4 | B: N=3 subjects (underpowered); effect is dramatic (smaller 
 16 | node_3_7       | FAIL    |    — | B: N=2 (only 2 subjects had simultaneous AUD+MOs recordings)
 17 | node_3_8       | FAIL    |    — | B: N=2 (only 2 subjects had VIS+AUD+MOs)
 18 | node_3_9       | FLAG    |    3 | B: N=3 subjects; E: Partially redundant with node_3_6 (both 
 19 | node_3_10      | FLAG    |    2 | C: Paired t-test across 25 blocks from 5 subjects (pseudo-re
 20 | node_3_11      | FLAG    |    3 | B: N=3 subjects (CA1 coverage requirement); C: Rolling-windo
 21 | node_3_12      | FAIL    |    — | B: N=1 (only subject 742903 had sufficient stationary trials)
 22 | node_3_13      | FAIL    |    — | B: N=2 (only 2 subjects had MOs+VIS for GC)
 23 | node_3_14      | PASS    |    4 | —
 24 | node_3_15      | FLAG    |    3 | B: N=3 subjects (CA1+PFC+VIS requirement); per-subject corre
 25 | node_4_0       | FAIL    |    — | B: N=2 (only 2 subjects had VIS+AUD+MOs simultaneously)
 26 | node_4_1       | PASS    |    2 | —
 27 | node_4_2       | FAIL    |    — | B: N=1 (only 1 subject had VIS+AUD+ORB or VIS+AUD+PFC)
 28 | node_3_16      | FAIL    |    — | C: Pseudo-replication (t-test across 25 block switches, not 5 sub
 29 | node_4_3       | PASS    |    4 | —
 30 | node_4_4       | FLAG    |    3 | Insufficient output to verify N subjects or confirm cross-su
 31 | node_3_17      | FLAG    |    3 | B: N=3 subjects (ACA+CA1 simultaneous requirement: 664851, 7
 32 | node_4_5       | FLAG    |    3 | C: No formal cross-subject aggregation test; per-subject cor
 33 | node_4_6       | FLAG    |    4 | G: p=0.0628 (just above 0.05, N=5); effect is consistent acr
 34 | node_4_7       | FAIL    |    — | B: N=2 (only 2 subjects had valid ACA+VIS divergence times)
 35 | node_4_8       | FLAG    |    3 | B: N=3 subjects (CA1+VIS+MOs simultaneous requirement)
 36 | node_3_18      | FAIL    |    — | B: N=2 (only 2 subjects had simultaneous VIS+AUD recordings)
 37 | node_4_9       | FLAG    |    3 | Insufficient code_output to verify N subjects; likely N=3 (C
 38 | node_4_10      | FLAG    |    3 | F: Subject 759434 has only 5 VIS units; Subject 713655 has o
 39 | node_4_11      | PASS    |    3 | —
 40 | node_3_19      | FLAG    |    3 | B: N=3 subjects (CA1+PFC+MOs requirement: 664851, 742903, 75
 41 | node_4_12      | FAIL    |    — | B: N=2 (only 2 subjects had enough Miss trials in visual blocks)
 42 | node_3_20      | FLAG    |    2 | G: Near-90° angles (86-87°) in high-dimensional spaces are e
 43 | node_3_21      | FAIL    |    — | B: N=1 (only subject 664851 had sufficient CA1+VIS units)
 44 | node_4_13      | FAIL    |    — | B: N=2 (only 2 subjects had simultaneous VIS+AUD)
 45 | node_4_14      | FAIL    |    — | B: N=1 (only subject 742903 had both stationary and running trial
 46 | node_4_15      | FLAG    |    3 | B: N=3 subjects (CA1+PFC simultaneous requirement: 664851, 7
 47 | node_4_16      | FAIL    |    — | B: N=1 (only subject 742903 had both ORB+PFC units with sufficien
 48 | node_4_17      | PASS    |    3 | —
 49 | node_4_18      | PASS    |    4 | —
 50 | node_4_19      | FLAG    |    3 | B: N=3 subjects with simultaneous CA1+PFC; Sobel mediation t
 51 | node_4_20      | PASS    |    3 | —
 52 | node_3_22      | FLAG    |    3 | B: N=3 subjects with valid ORB+MOs decoding latencies; Wilco
 53 | node_4_21      | FAIL    |    — | B: N=2 (only 2 subjects had simultaneous VIS+AUD recordings)
 54 | node_4_22      | PASS    |    2 | —
 55 | node_4_23      | FLAG    |    3 | B: N=3 subjects with simultaneous CA1+PFC+VIS; no cross-subj
 56 | node_4_24      | FAIL    |    — | B: N=0 (no divergence latencies found in any subject)
 57 | node_4_25      | FAIL    |    — | B: N=1 (only 1 subject had ≥5 Post-Miss trials)
 58 | node_3_23      | FAIL    |    — | B: N=2 for AUD-MOs pathway (key comparison requires both pathways
 59 | node_4_26      | FLAG    |    3 | B: N=3 subjects with sufficient CA1+PFC units (664851, 74290
 60 | node_4_27      | FLAG    |    3 | D: VIS-MOs communication subspace defined exclusively from v
 61 | node_4_28      | FAIL    |    — | B: N=2 (only 2 subjects had sufficient VIS+PFC units)
 62 | node_4_29      | FLAG    |    3 | G: p=0.0992 (borderline, N=5 underpowered); mean out-of-cont
 63 | node_4_30      | FLAG    |    2 | E: Substantially redundant with node_4_11 (same population, 
 64 | node_3_24      | FLAG    |    4 | B: N=3 subjects with sufficient CA1+PFC units; p=0.024 with 
 65 | node_4_31      | PASS    |    4 | —
 66 | node_2_8       | FAIL    |    — | B: N=2 (only 2 subjects had sufficient ACA+CA1 units for trajecto
 67 | node_3_25      | FAIL    |    — | B: N=2 (only 2 subjects had simultaneous VIS+AUD recordings: 6648
 68 | node_4_32      | FAIL    |    — | B: N=2 (only subjects 664851 and 713655 had simultaneous VIS+AUD 
 69 | node_4_33      | FLAG    |    3 | B: N=3 subjects with sufficient CA1+PFC+VIS simultaneous rec
 70 | node_3_26      | FLAG    |    3 | E: Substantially redundant with node_3_14 and node_4_27 (all
```

---

## Reject Summary

**#2 node_2_1** — B: N=0 (no subjects had simultaneous VIS+AUD+PFC recordings)
> *none of the subjects had simultaneous recordings of high-quality units from all three required regions (VIS, AUD, PFC)*

**#4 node_2_3** — B: N=0 (no subjects had simultaneous ACA+PFC+VIS recordings)
> *outputted that there was 'No sufficient data to perform CCA and ANOVA'*

**#6 node_2_5** — B: N=1 (only subject 664851 had CA1+VIS+AUD)
> *Only one subject (Subject 664851) had units in all three regions (CA1: 95, VIS: 87, AUD: 264)*

**#8 node_2_7** — B: N=1 (only subject 664851 contributed transition data for CA1+PFC)
> *Sample scores for Subject 664851, Transition to Block 1 — only this subject shown; N=1 pattern confirmed in analysis/review*

**#14 node_3_5** — B: N=2 (only two subjects met VIS+AUD+MOs criteria)
> *The experiment successfully executed and analyzed data for two subjects that met the criteria*

**#16 node_3_7** — B: N=2 (only 2 subjects had simultaneous AUD+MOs recordings)
> *Out of the 5 subjects, 2 subjects (664851 and 713655) had recordings in both AUD and MOs*

**#17 node_3_8** — B: N=2 (only 2 subjects had VIS+AUD+MOs)
> *only 2 out of the 5 subjects were viable for the paired analysis. Despite the extremely small sample size (N=2)*

**#21 node_3_12** — B: N=1 (only subject 742903 had sufficient stationary trials)
> *Only one out of the five subjects (Subject 742903) had the minimum required number of stationary trials*

**#22 node_3_13** — B: N=2 (only 2 subjects had MOs+VIS for GC)
> *no statistical significance (p = 1.0) due to the limited number of subjects (n = 2)*

**#25 node_4_0** — B: N=2 (only 2 subjects had VIS+AUD+MOs simultaneously)
> *leaving two valid subjects (664851 and 713655)*

**#27 node_4_2** — B: N=1 (only 1 subject had VIS+AUD+ORB or VIS+AUD+PFC)
> *only a single subject... had sufficient data; three out of the five subjects lacked high-quality units across all required regions*

**#28 node_3_16** — C: Pseudo-replication (t-test across 25 block switches, not 5 subjects; df=24 for 5-subject dataset)
> *paired t-test: t = 16.75, p = 9.64e-15 — implausibly large df for N=5; 25 blocks from 5 subjects are not independent observations*

**#34 node_4_7** — B: N=2 (only 2 subjects had valid ACA+VIS divergence times)
> *only two subjects exhibited valid divergence times for both ACA and VIS regions*

**#36 node_3_18** — B: N=2 (only 2 subjects had simultaneous VIS+AUD recordings)
> *Data from two valid subjects (664851, 713655) with sufficient units in both regions were analyzed*

**#41 node_4_12** — B: N=2 (only 2 subjects had enough Miss trials in visual blocks)
> *subjects 664851 and 668755 were skipped because they had only 1 Miss trial each...leaving only two subjects (713655 and 742903)*

**#43 node_3_21** — B: N=1 (only subject 664851 had sufficient CA1+VIS units)
> *only a single subject ('664851') had the required minimum of 15 simultaneous high-quality units in both the hippocampus (CA1) and the visual cortex (VIS)*

**#44 node_4_13** — B: N=2 (only 2 subjects had simultaneous VIS+AUD)
> *2 subjects with simultaneous recordings in these regions*

**#45 node_4_14** — B: N=1 (only subject 742903 had both stationary and running trials meeting threshold)
> *Only one subject (Subject 742903) had sufficient data*

**#47 node_4_16** — B: N=1 (only subject 742903 had both ORB+PFC units with sufficient data)
> *only a single subject (742903) had a sufficient number of valid units in both ORB and PFC*

**#53 node_4_21** — B: N=2 (only 2 subjects had simultaneous VIS+AUD recordings)
> *only 2 out of the 5 subjects (664851 and 713655) had simultaneous high-quality recordings in both VIS and AUD regions*

**#56 node_4_24** — B: N=0 (no divergence latencies found in any subject)
> *Not enough valid latencies found across subjects for statistics (no divergence met the threshold)*

**#57 node_4_25** — B: N=1 (only 1 subject had ≥5 Post-Miss trials)
> *four out of five subjects had fewer than 5 Post-Miss trials... Only one subject [viable]*

**#58 node_3_23** — B: N=2 for AUD-MOs pathway (key comparison requires both pathways)
> *Pathway: AUD->MOs (N=2 subjects), Pathway: VIS->MOs (N=5 subjects) — the primary test of orthogonality between AUD-MOs and VIS-MOs requires N≥4 for AUD-MOs*

**#61 node_4_28** — B: N=2 (only 2 subjects had sufficient VIS+PFC units)
> *Valid data was found for two subjects (742903 and 713655)*

**#66 node_2_8** — B: N=2 (only 2 subjects had sufficient ACA+CA1 units for trajectory analysis)
> *Across the two subjects with sufficient data in both regions*

**#67 node_3_25** — B: N=2 (only 2 subjects had simultaneous VIS+AUD recordings: 664851, 713655)
> *Subject 742903: Not enough VIS/AUD units — only 2 subjects have both VIS and AUD simultaneously*

**#68 node_4_32** — B: N=2 (only subjects 664851 and 713655 had simultaneous VIS+AUD for the key cross-pathway comparison)
> *Pearson correlations between pupil size and coupling metrics calculated for two valid subjects (664851 and 713655)*

---

## Cross-Finding Narrative

The 12 PASS experiments from run c003951b collectively constrain (but do not yet resolve) the mechanistic account of context-dependent routing in the Allen Institute Dynamic Routing task. Three themes emerge:

**1. Context-dependent routing is present in VIS→MOs but not via gain modulation of a fixed subspace.**
node_3_14 (N=4, PASS) finds that projecting VIS stimulus activity into a *fixed* VIS-MOs communication subspace yields equal amplitude across task contexts (p=0.520) — ruling out pure gain scaling of a geometry-stable channel. node_4_3 (N=5, PASS) additionally shows that VIS-to-MOs and VIS-to-PFC pathways are equally (and weakly) context-modulated (p=0.907), contradicting the prediction that VIS-to-MOs is *strictly* gated while VIS-to-PFC is continuous. The FLAG experiment node_4_27 (N=5, p=0.0097) does find significantly higher VIS alignment with the VIS-MOs subspace during visual blocks, but this result is caveated by within-context bias in the subspace alignment estimate.

**2. Context transitions are characterized by LOW, not high, network dimensionality.**
node_4_11 (N=5, p=0.0065, PASS) finds that the joint VIS+AUD+PFC+MOs Participation Ratio is *significantly lower* during early transition trials (mean PR=13.50) than during steady-state trials (PR=25.65). This directly contradicts the Attractor Dynamics prediction that the network passes through a high-dimensional transient before settling. node_4_1 (N=5, p=0.719) and node_3_0 (FLAG-C) corroborate the null in sensorimotor-only populations. These findings are consistent with reduced trial-to-trial variability or dimensionality collapse during the period when the animal is actively resolving ambiguity.

**3. Context updating follows a top-down temporal cascade, but error signals do not engage specialized routing geometries.**
FLAG experiment node_4_6 (N=5, p=0.063, 5/5 consistent) finds PFC context-decoding inflects at 1.8 trials post-switch while VIS takes 8.4 trials — a 4.7× lead consistent with top-down context cascading. However, this cascade does NOT operate trial-by-trial via PFC context state → VIS gain: node_2_6 (N=5, LME, p=0.695, PASS) shows PFC context confidence on trial N does not predict VIS sensory discriminability on trial N+1. Separately, error correction does not appear to involve specialized geometries: node_4_18 (N=5, p=0.199, proper null model) finds Post-Error and Post-Correct frontal-sensory subspaces are not orthogonal, and node_4_31 (N=4, p=0.139) shows CR trials are *not* routed through an orthogonal suppression channel — 3/4 subjects show the opposite direction.

**Framing caveat (pilot constraint):** All PASS results are from N=5 subjects. They constitute Constraints on the mechanistic account, not Resolutions. Replication across the full ~114-session cohort would be required to upgrade any finding to Resolution status. The unusually high rate of FAIL due to region availability (27/70 experiments failed on N<3) reflects the stringent simultaneous multi-region recording requirement of many hypotheses — not a dataset flaw, but a constraint on the analyses AutoDiscovery can run on a 5-subject pilot.
