
## Scope

This document records what was done, what inputs were used, what outputs were produced, what failed and how it was recovered, and what the known limitations of each step are. It is an audit trail, not a scientific narrative — the science is in `report.md`.

---

## Inputs

| File | Source | Hash / Size | Used for |
|---|---|---|---|
| `ASMS.sdf` | User-supplied | 53,967,091 bytes | Screen actives/inactives |
| `CDK2-CCNE.pdb` | User-supplied | 784,165 bytes | Receptor structure, binding site, docking box |

No public databases, public structures, or internet lookups were used at any point.

---

## Stage-by-stage record

### Stage 1 — Screen triage
**Status**: Complete. Documented in `stage1_screen_triage.md`.

- Loaded 15 actives from `ASMS.sdf` using RDKit `SDMolSupplier`. Inactives were not fully profiled (empty `Hit_rank` field caused silent drop; not material to the design).
- MCS computed over 15 actives: 15-atom, 16-bond THN core.
- 13/15 actives classified as THN scaffold; 2/15 as alternate piperidinyl-succinamide chemotype.
- AS-ratio range: 0.0012–0.172.

**Known gap**: Inactive structural profile was not computed. No scaffold enrichment analysis vs inactive set was performed; the THN scaffold occurrence rate among inactives is unknown.

---

### Stage 2 — Binding site characterisation
**Status**: Complete.

- CTX ligand (HETATM B401, 39 heavy atoms) extracted from `CDK2-CCNE.pdb`.
- Pocket residues within 4.5 Å of any CTX atom enumerated: 23 residues across both chains.
- Confirmed PPI glue: CTX contacts residues in both chain A (CDK2) and chain B (Cyclin E).
- H-bond analysis: HIS121-A backbone C=O ← CTX N2 (3.12 Å); LYS108-B NZ → CTX O2 (3.27 Å).
- TRP102-B and TRP234-B identified as aromatic sandwich for R1 cap.

**Known gap**: No MD or minimisation was run to check whether the stripped receptor (CTX removed) relaxes significantly. The apo pocket geometry is assumed to be that of the holo crystal.

---

### Stage 3 — SAR derivation from screen
**Status**: Complete.

- Two R-group positions identified on THN core (R1: N-acyl aromatic cap; R2: NH–CH₂–Ar arm).
- All 13 THN actives have unique R1 and R2 combinations — no SAR from pairwise comparisons within the screen data is possible.
- HBD=1 (ring NH) present in 14/15 actives; identified as pharmacophoric anchor to HIS121-A.
- AS ratio does not correlate with Vina score (Spearman rank order diverges; EDS00495858 highest AS but 11th by Vina).

**Known gap**: No dose-response data — AS ratio is a single-point binding signal; potency rank is uncertain. No counterscreen data to exclude false positives.

---

### Stage 4 — Analogue design
**Status**: Complete. 38 compounds designed in 10 series (A–J).

- Template: `O=C(R1)N1Cc2nc(C(=O)NCC_R2)ccc2CC1` (THN core, two variable positions).
- R1 variation: 10 different aromatic/heteroaromatic capping groups including fused bicyclics, CF₃-pyridines, monocyclic phenyl.
- R2 variation: 4,4-difluorocyclohexyl, benzyl variants (4-F, 2-pyrrolyl, piperazino, morpholino, cyano), pyrimidyl/pyridyl methyls.
- All 38 SMILES validated by RDKit `MolFromSmiles`; 0 invalid.

**Known gap**: 38 compounds covers 10 R1 groups × 4 R2 groups in an incomplete matrix. Several R1×R2 combinations were not designed; the SAR matrix is sparse. R2=4,4-diF-cyclohexyl was designed specifically for ADME, not from structural precedent in the actives.

---

### Stage 5 — Docking
**Status**: Complete after one infrastructure failure and re-run.

**Failure**: First dispatch of all 53 compounds as a single SDF failed after 884 s with `host_unreachable`. No output was written.

**Recovery**: Split into three batches (15 actives; 19 designed; 19 designed). All three batches completed successfully on GPU (246 s, 295 s, 381 s, 369 s wall time).

**Error found and corrected**: In the first successful batch run, `proteinFile` was accidentally set to `batch_actives.sdf` instead of `receptor_stripped.pdb`. This produced Vina affinities of 0.0 kcal/mol for all poses. Detected immediately; re-run with correct receptor; real affinities recovered (−9 to −14 kcal/mol range).

**Parameters used**:
- Receptor: `receptor_stripped.pdb` (CDK2-CCNE with all HETATM removed)
- Box centre: (30.57, 5.37, −25.80) Å (CTX centroid)
- Box size: 24 × 20 × 20 Å (CTX bbox + 8 Å padding)
- Exhaustiveness: 8, numModes: 9, cnnScoring: rescore, seed: 42

**Output**: 477 poses total (53 compounds × 9 poses each). Parsed from three `.sdf.gz` files. Best pose per compound selected by most-negative Vina.

**Known limitations**:
- gnina CNN was trained on standard protein-ligand complexes, not PPI glue interfaces. CNN scores may be unreliable at the two-chain pocket.
- Two actives (EDS00480994, EDS00490594) have anomalously high CNN scores (0.97, 0.94) vs all others (≤0.53). This may reflect these compounds adopting a genuinely high-confidence pose, or it may be a CNN artefact at this interface geometry.
- Vina/AS-ratio rank discordance (Spearman r estimated < 0.3) means docking score is used for analogue ranking, not for retrospective validation of the screen result.
- Receptor geometry is from the holo crystal. Induced-fit or ensemble effects are not modelled.

---

### Stage 6 — ADME filtering
**Status**: Complete.

**Criteria applied**: Lipinski RO5 (0 violations: MW ≤ 500, logP ≤ 5, HBD ≤ 5, HBA ≤ 10), TPSA ≤ 140 Å², rotatable bonds ≤ 10, no PAINS alerts (RDKit PAINS-A catalog).

**Result**: 16/38 designed compounds pass; 22/38 fail.

**Dominant failure modes**:
- MW > 500: 11 compounds (mostly from piperazino/morpholino R2 groups)
- PAINS alert: 18 compounds (para-aminobenzyl, N-arylpiperazines flagged by PAINS-A)
- Both MW and PAINS: 9 compounds

**Caveat on PAINS**: 9/15 ASMS actives pass ADME on the same criteria; 6/15 fail (4 by PAINS, 2 by MW). Given that these 15 are confirmed binders, the PAINS filter is over-aggressive for this scaffold class. The 22 ADME-failing designed compounds are not discarded — the highest Vina scorers (D02, C02, B03, at −13 to −12 kcal/mol) are candidates for re-design with ADME-improving substitutions.

---

### Stage 7 — Ranked delivery and SAR claims
**Status**: Complete. Output in `report.md`.

- 16 ADME-passing compounds ranked by Vina affinity.
- 6 explicit falsifiable SAR claims stated with matched pairs, predicted effect sizes, and explicit declaration of which claims are most damaging if wrong.
- No experimental SAR was consulted before or during claim generation.

---

## Files produced

| File | Content |
|---|---|
| `ligands_3d.sdf` | 53 compounds (15 actives + 38 designed) with ETKDG+MMFF 3D coordinates |
| `receptor_stripped.pdb` | CDK2-CCNE receptor, HETATM removed |
| `batch_actives.sdf` | 15 actives only (docking input) |
| `batch_des1.sdf` | Designed compounds 1–19 (docking input) |
| `batch_des2.sdf` | Designed compounds 20–38 (docking input) |
| `actives_docked.sdf.gz` | 135 poses for 15 actives |
| `des1_docked.sdf.gz` | 171 poses for first 19 designed |
| `des2_docked.sdf.gz` | 171 poses for last 19 designed |
| `report.md` | Full scientific deliverable (synthesis list + SAR claims) |
| `stage1_screen_triage.md` | Stage 1 phase document |
| `audit_hit_to_lead_cycle.md` | This document |

---

## Unresolved issues and follow-on work

1. **ADME-failing high-scorers** (D02, C02, B03): warrant re-design with reduced MW/PAINS substitutions (e.g., replace piperazino-Bn with diF-cHex or compact neutral R2).
2. **Inactive scaffold profile**: needed to confirm THN enrichment is real and not a library-composition artefact.
3. **Apo receptor relaxation**: a brief energy minimisation of the stripped pocket would confirm whether the CTX-bound geometry is a reasonable docking target.
4. **Counterscreen data**: the 15 ASMS actives have not been filtered against orthogonal assays; some may be non-specific binders.
5. **Experimental SAR comparison**: once experimental potency data is available for the synthesised compounds, Claims 1–6 in `report.md` can be scored directly against prediction.
