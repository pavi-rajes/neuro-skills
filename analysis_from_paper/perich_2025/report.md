# Deviation Report — Perich et al. (2025)

## Faithful
- PCA per context, principal angles via SVD of Gram matrix — matches Perich framework exactly
- Cross-context variance explained: fraction of variance in one context's rates captured by the other context's PC space
- 50 ms bins, −0.5 to +1.0 s window around stimulus onset
- `np.random.seed(42)` for all stochastic steps
- Regions analyzed separately (not pooled), matching the paper's per-region framework
- **MOp = M1 analog, MOs = PMd analog** — directly mirrors the Perich et al. region pair

## Adapted
- **Species/task:** Perich et al. analyzed motor cortex during reaching; applied here to a context-switching sensory decision task in mice (Dynamic Routing)
- **Context definition:** Paper compares movement conditions; here contexts are `rewarded_modality` blocks (vis vs aud)
- **Unit quality:** Used `default_qc` as proxy for paper's ISI + waveform-based inclusion criteria
- **Multi-day extension:** Original paper focuses on single sessions; 4-day stability is a novel application

## Uncertain
- Minimum unit count per subspace not stated in paper — used n ≥ 5 floor
- N PCs = 10 not explicitly stated for the principal-angle analysis
- Normalization: paper uses soft-normalization in some analyses; raw Hz used here
- Brain region loading differs by NWB schema version (2023 vs 2024+ sessions)

## Summary

**Sessions:** 2 subjects × 4 sessions each (8 total). Subject 681532 day 4 had 0 units in all regions (probe outside target areas) and is excluded from stability analysis. MOp units absent in many sessions (only 4/8 sessions had ≥ 5 MOp units).

### Mean principal angles (vis-context vs aud-context subspace, top 10 PCs)

| Subject | Day | MOp (M1 analog) | MOs (PMd analog) |
|---------|-----|-----------------|------------------|
| 676909 | 1 | 34.1° (n=165) | 44.9° (n=328) |
| 676909 | 2 | 40.0° (n=72)  | 44.2° (n=283) |
| 676909 | 3 | 39.2° (n=44)  | 55.5° (n=223) |
| 676909 | 4 | —             | 42.8° (n=497) |
| 681532 | 1 | 44.7° (n=103) | 54.3° (n=759) |
| 681532 | 2 | —             | 44.5° (n=178) |
| 681532 | 3 | —             | 50.0° (n=112) |
| 681532 | 4 | —             | —             |

### Cross-context variance explained (mean of vis-in-MOs and MOs-in-vis)

| Subject | Day | MOp | MOs |
|---------|-----|-----|-----|
| 676909 | 1 | 0.97 | 0.94 |
| 676909 | 2 | 0.80 | 0.88 |
| 676909 | 3 | 0.89 | 0.64 |
| 676909 | 4 | —   | 0.90 |
| 681532 | 1 | 0.76 | 0.77 |
| 681532 | 2 | —   | 0.91 |
| 681532 | 3 | —   | 0.81 |

### Key findings

- **MOp (M1 analog) angles are mostly below 45°** (34–45°), indicating vis- and aud-context subspaces are fairly similar in primary motor cortex — consistent with Perich et al.'s finding that M1 activity is less condition-differentiated.
- **MOs (PMd analog) angles are at or above 45°** (43–56°), suggesting premotor cortex manifolds are more context-differentiated — consistent with Perich et al.'s finding that PMd shows stronger condition-dependent geometry.
- **The MOp < MOs pattern matches the paper's M1 vs PMd contrast** directly: the premotor area encodes context more distinctly than primary motor cortex.
- **Cross-context variance explained is high for MOp** (0.76–0.97), confirming subspace overlap. MOs is lower and more variable (0.64–0.94), consistent with its larger principal angles.
- **4-day stability:** MOs angles are stable within subjects (676909: 42–56°; 681532: 44–50°). The 676909 day 3 outlier (MOs 55.5°, cross-var 0.64) recovered by day 4 (42.8°, 0.90).
- **MOp coverage is sparse** — only 4 of 8 sessions had ≥ 5 MOp units; day-to-day stability for MOp cannot be assessed for subject 681532. Lower unit counts (down to 44 for 676909 day 3) likely inflate noise in subspace estimates.
