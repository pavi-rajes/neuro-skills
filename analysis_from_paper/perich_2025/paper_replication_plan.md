# Replication Plan — Perich et al. (2025)

**Citation:** Perich, M.G. et al. (2025). A neural manifold view of the brain. *Nature Neuroscience*.  
**Dataset:** Allen Institute Dynamic Routing — `s3://aind-scratch-data/dynamic-routing/cache/nwb/v0.0.273/`  
**Target analysis:** Neural manifold similarity between visual-context and auditory-context population activity  
**Target figures:** Principal angles between context subspaces; cross-context variance explained; population trajectories

---

## Paper → NWB Variable Mapping (confirmed by user)

| Paper variable | NWB field | Notes |
|---|---|---|
| Visual context trials | `intervals/trials.rewarded_modality == "vis"` | Context block label |
| Auditory context trials | `intervals/trials.rewarded_modality == "aud"` | Context block label |
| Alignment event | `intervals/trials.stim_start_time` | Stim onset = time 0 |
| Analysis window | −0.5 to +1.0 s | 50 ms bins |
| Population activity | Good units (`default_qc == True`) in VIS, AUD, MO regions | Analyzed per region independently |
| Brain region filter | `electrodes.location.starts_with("VIS" / "AUD" / "MO")` | Via `peak_electrode` join for 2024+ sessions |
| Core analysis | PCA per context → principal angles via SVD of Gram matrix | Matches Perich framework |
| Cross-context overlap | Fraction of variance in one context explained by other context's PCs | |

## Subjects

Two subjects with 4 recording sessions each, confirmed to have VIS + AUD + MO electrode coverage.  
*(Subject IDs to be filled once electrodes scan completes.)*

## Parameters

| Parameter | Value | Source |
|---|---|---|
| Bin size | 50 ms | Paper |
| Window | −0.5 to +1.0 s | Paper |
| N PCs | 10 | Paper (assumed — not explicitly stated) |
| Random seed | 42 | Fixed for reproducibility |

## Assumptions

- Spike times are in seconds
- `default_qc` is a valid proxy for paper's unit quality criteria
- `stim_start_time` is the correct alignment event (stim onset)
- Context blocks are defined by `rewarded_modality`; blocks switch at `block_index` boundaries

## Open questions / gaps

- Paper's minimum unit count per subspace not stated — using n ≥ 5 floor
- Normalization: paper uses soft-normalization in some analyses; raw Hz rates used here
- AUD electrode counts are sparse in some sessions — noted as a caveat in notebook
