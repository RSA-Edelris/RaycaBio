# Pocket Detection Tool Survey & Cryptic Pocket Workflow Design
**Date:** 2026-09-18  
**Session type:** Discovery / Q&A

---

## Platform Pocket Detection Tools (Confirmed)

| Tool ID | Name | Method | Druggability Score | GPU Required |
|---|---|---|---|---|
| `fpocket` | fpocket | Geometry-based (Voronoi / alpha-sphere). Detects all pockets: main, secondary, potential allosteric. | Yes — `top_pocket_druggability`, `top_pocket_score` | No (CPU) |
| `pykvfinder` | pyKVFinder | Geometry-based cavity detection — binding sites, clefts, buried pockets | No | No (CPU) |
| `pickpocket` | PickPocket | Ligand-specific pocket detection. Runs fpocket2 + STRIDE secondary structure. Best when a reference ligand class is known. | No | No (CPU) |
| `grasp` | GrASP | Graph Attention Site Prediction — ML-based druggable site identification, per-atom druggability scores | Yes — `max_druggability`, `mean_surface_druggability` | **Yes** |

**Also found (generative / downstream tools, not pocket finders):**
- `pocketgen` — re-designs residues within a known binding site given protein + ligand
- `pocketflow` — grows novel molecules from a pocket PDB

---

## Recommended Tool by Use Case

| Goal | Tool |
|---|---|
| Quick scan of all pockets on a new target | `fpocket` |
| ML-based druggability scoring | `GrASP` (requires GPU) |
| Ligand-class-guided pocket detection | `PickPocket` |
| Cryptic / allosteric pockets | MD ensemble + per-frame `fpocket` (see workflow below) |

---

## Proposed Workflow: Cryptic / Allosteric Pocket Discovery

**Applicability:** targets where the pocket of interest is not visible (or not open) in the static crystal structure.

### 4-Phase Pipeline

```
Phase 1 — Structure Preparation
  - Clean PDB (remove waters, ligands, crystal contacts)
  - Assign protonation states (PROPKA / pdb2pqr)
  - Select force field (CHARMM36m or a99SB-disp for disorder-balanced systems)
  - If membrane protein: embed in bilayer (CHARMM-GUI / insane.py)

Phase 2 — Enhanced Sampling MD
  - Baseline unbiased MD (50–100 ns): confirm stability, collect Vmax/Vmin/mean/SD
  - Enhanced sampling (choose one):
      a) GaMD dual-boost  — CV-free, general conformational sampling
      b) Cosolvent MD / SWISH — maps energetically favourable probe sites
         (use when pocket type is completely unknown)
  - Run ≥3 independent replicas
  - Stop criterion: convergence of cavity volume time series

Phase 3 — Per-Frame Pocket Detection
  - Run fpocket on every trajectory frame
  - Build MDpocket density grid (persistence / occupancy map)
  - Track cavity volume per frame (Epock-style volume time series)
  - Flag pockets open in >10% of frames as candidates

Phase 4 — Persistence Scoring & Ranking
  - Rank by: open fraction × mean druggability score (fpocket or GrASP on open frames)
  - Cross-check hits against known orthosteric and cofactor sites
  - Confirm top candidates under a second force field (force-field-conditional pockets are not real hits)
  - Return ranked hypotheses with confidence flags — NOT validated sites
```

### Key Rules
- A pocket that opens in only one force field → **force-field-conditional, flag and deprioritise**
- Always cross-check against the DNA-bound / partner-bound complex state (pocket may be occluded in functional state)
- Report open fraction and residence time, not just existence

### MD Engine (TBD)
Available engines on platform cluster not yet confirmed — need to run `list_compute` + `query_cluster` for GROMACS / AMBER / OpenMM availability.

---

## Next Steps
1. Confirm target type (soluble / GPCR / transcription factor / other membrane protein)
2. Check available MD engine on cluster
3. Run structure preparation + baseline MD
4. Deploy enhanced sampling + MDpocket analysis
