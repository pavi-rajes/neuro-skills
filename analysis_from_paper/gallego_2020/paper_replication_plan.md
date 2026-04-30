---
paper: "Long-term stability of cortical population dynamics underlying consistent behavior"
authors: Gallego JA, Perich MG, Chowdhury RH, Solla SA, Miller LE
journal: Nature Neuroscience 23, 260–270 (2020)
doi: 10.1038/s41593-019-0555-4
target_figure: Fig. 4 analog — normalized CCA similarity across days
confirmed: true
---

# Replication Plan — Gallego et al. (2020)

## Population sampling decision

| Paper region | DR region used | Match quality | Decision |
|---|---|---|---|
| M1 (macaque primary motor) | `MOp` (mouse primary motor) | rough structural homolog; task completely different | **Use MOp — user confirmed** |
| PMd (macaque dorsal premotor) | not analyzed | — | **excluded — user wants MOp only** |
| S1 Area 2 | not analyzed | — | **excluded** |

**Co-recording:** Paper requires same-array multi-day recordings. DR subjects have daily Neuropixels re-insertions — different neurons each day. CCA operates on PC subspace (not individual neurons), so cross-day alignment is still valid.

**Subjects:** 676909 and 681532 (4 consecutive sessions each, 2023 format).

**Known limitation:** MOp coverage is sparse (from prior scan — 4/8 sessions have ≥5 MOp units). Subject 681532 has only 1 eligible day → cross-day stability cannot be computed for that subject.

---

## Variable mapping

| Paper variable | NWB / DR equivalent | Notes |
|---|---|---|
| Movement onset alignment (M1 window: −120 to +420 ms) | `response_time` (lick onset, −120 to +420 ms) | **Adapted**: no reach onset in DR; lick onset is closest motor output analog. Miss trials (no lick) excluded. |
| 8 reach target directions (condition labels) | all trials concatenated | PCA is fit on all trials pooled — no condition averaging |
| 30 ms bins | 30 ms bins | **Faithful** |
| 50 ms Gaussian smooth (σ) | `gaussian_filter1d`, σ=50/30=1.67 bins | **Faithful** |
| Square-root transform | `np.sqrt(counts)` before smoothing | **Faithful** |
| FR > 1 Hz exclusion | FR > 1 Hz computed over session duration | **Faithful** |
| `default_qc` | proxy for paper's waveform/ISI criteria | **Adapted** |
| N PCs = 10 (M1) | chosen per session to explain ≥85% variance | **Adapted** — paper's fixed 10 was tuned to macaque M1 (~100 units/array); mouse MOp unit counts vary (44–165) |
| CCA normalized similarity | across-day mean(top-4 CCs) / within-day mean(top-4 CCs) | **Faithful** |
| Within-day upper bound | 100 random trial splits, same-day CCA | **Faithful** |

## Open questions / caveats

- Subject 681532 has only 1 MOp-eligible session → stability analysis only possible for 676909
- N PCs will be capped at `min(n_pcs_across_days)` per subject for fair CCA comparison
- Different neurons are recorded each day (Neuropixels re-insertion) — paper tracked same implant with some neuron turnover; our adaptation uses the PC subspace approach which does not require matching neurons
- Task difference (reaching vs. sensory decision) is large — results reflect latent dynamics stability in a sensory/cognitive context, not motor preparation
