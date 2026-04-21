# Deviation Report — Gallego et al. (2020)

**Paper:** "Long-term stability of cortical population dynamics underlying consistent behavior"
Gallego JA, Perich MG, Chowdhury RH, Solla SA, Miller LE. *Nature Neuroscience* 23, 260–270 (2020).
DOI: 10.1038/s41593-019-0555-4

## Faithful
- 30 ms bins, 50 ms Gaussian smooth (σ), square-root transform before binning — exact paper values
- CCA-based normalized similarity: across-day mean(top-4 CCs) / within-day mean(top-4 CCs)
- Within-day upper bound via 100 random trial splits on the same session
- FR > 1 Hz unit exclusion criterion

## Adapted
- **Species/task:** Macaque center-out reaching (8 targets) → mouse context-switching sensory decision (Dynamic Routing)
- **Brain region:** Macaque M1 → mouse MOp (rough structural homolog; no reaching in this task)
- **Trial alignment:** Movement onset → lick onset (`response_time`); miss trials excluded (no lick)
- **N PCs:** Paper's fixed M1=10 → chosen per subject to explain ≥85% variance (676909: 16 PCs)
- **Unit tracking:** Paper tracked same Utah array implant across days (some neuron turnover); DR uses daily Neuropixels re-insertions with entirely new unit sets. CCA on PC subspace does not require matched neurons — still valid.
- **Conditions:** Paper equalized trials per reach direction across days; here all lick-present trials pooled for PCA

## Uncertain
- Whether `default_qc` matches paper's waveform/ISI quality criteria
- Paper used ~100 channels/session (Utah array); MOp in DR ranged 44–165 units — lower counts increase noise in CCA estimates
- `response_time` in DR is time of first lick after stimulus; whether this is the right motor onset analog is debatable (lick could occur during ongoing sensory processing, not purely as a motor output)

---

## Results

**Sessions:** Subject 676909, 3 eligible sessions (Dec 11–13, 2023). Subject 681532 had only 1 MOp-eligible session — cross-day stability could not be assessed.

### Normalized similarity (lick-aligned, MOp, 16 PCs)

| Pair | Days apart | Normalized similarity |
|---|---|---|
| Dec 11 ↔ Dec 12 | 1 | 0.85 |
| Dec 12 ↔ Dec 13 | 1 | 0.97 |
| Dec 11 ↔ Dec 13 | 2 | 0.92 |

### Key findings

- **MOp latent dynamics are stable across 1–2 days** in subject 676909: normalized similarity 0.85–0.97, all near the within-day bound of 1.0. This is broadly consistent with Gallego et al.'s macaque M1 result (~0.93 normalized similarity).
- **First canonical dimension is highly stable (~0.97)** across all pairs — one dominant mode is preserved day-to-day. Higher canonical dimensions drop off faster across days than within-day, indicating some drift in the lower-variance structure.
- **2-day gap (0.92) is not clearly worse than 1-day gaps (0.85, 0.97)** — small sample precludes any trend conclusion; the spread within 1-day pairs is larger than the 1- vs 2-day difference.
- **N PCs = 16 is higher than paper's M1=10**, likely because mouse MOp unit populations in DR have more variance distributed across dimensions (different task, different neural dynamics) or because unit count variability inflates apparent dimensionality.
- **Subject 681532 is unavailable** for this analysis — only 1 MOp-eligible session. The finding is therefore limited to a single subject with 3 days.
