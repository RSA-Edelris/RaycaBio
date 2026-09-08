# Phase: Kinome Selectivity Profile — 6 PDK1 Ligands

**Date:** 2026-09-07  
**Tool:** KinaseDocker2 (AutoDock Vina-GPU + DNN scorer, PLEC fingerprint, pIC50 units)  
**Compounds:** BX912, EL2003A, EL2003A-A2U1, EL2003A-A4U1, EL5001A, EL5003A  
**Kinases profiled:** 43 (AGC full family + targeted clinical panel across CMGC, TK, TKL, CAMK, STE, CK1, Other)

---

## Objective

Profile the predicted kinome-wide engagement of all six PDK1-directed ligands to: (1) identify clinically relevant off-targets, (2) determine which off-targets are common to all six compounds vs. compound-specific, and (3) rank compounds by selectivity.

---

## Inputs

| File | Description |
|:---|:---|
| `ligand_smiles.json` | Six compound SMILES + physicochemical properties |
| KinaseDocker2 (platform tool) | AutoDock Vina-GPU docking against KLIFS X-ray structures, DNN pIC50 scorer |
| KLIFS database (via tool) | ~80 representative kinase structures across 43 kinases |

---

## Methods

### Kinase panel selection

KinaseDocker2 accepts either `kinase_families` (expands to all KLIFS structures in that family) or `accessions` (UniProt IDs, expands to all KLIFS structures for those kinases). The full-kinome family approach was attempted first:

- AGC family (full): completed in 1397 s (25 KLIFS structures)
- CMGC family (full): timed out at 1800 s — too many structures

Strategy switched to `accessions`-based targeted runs. Each UniProt accession maps to 1–4 KLIFS representative structures; 5 accessions ≈ 14 KLIFS structures ≈ 1143 s. Batch size capped at 7 accessions per call (~980–1050 s, safely under the 1800 s MCP idle timeout).

### Docking runs

| Run name | Accessions / family | KLIFS structures | Time (s) |
|:---|:---|:---|:---|
| `PDK1_AGC` | AGC family | ~25 | 1397 |
| `PDK1_probe5` | CDK2, GSK3B, EGFR, ABL1, AURKA | 14 | 1143 |
| `PDK1_batch2` | CDK1, CDK4, CDK6, ERK1, ERK2, p38α, JNK1 | 11 | 981 |
| `PDK1_batch3` | KDR, FGFR1, MET, SRC, BTK, JAK2, FLT3 | 19 | 1044 |
| `PDK1_batch4` | CHEK1, CHEK2, PLK1, MEK1, BRAF, CK1d | 11 | 598 |

Total: 6 compounds × 43 kinases = 258 compound–kinase pairs; 475 raw rows (some kinases have multiple KLIFS structures per compound).

### Score aggregation

`avg_score` (mean DNN pIC50 of top-3 Vina poses) was used throughout. For kinases with multiple KLIFS structures, the maximum `avg_score` per compound–kinase pair was taken as the representative value, consistent with a best-case binding estimate.

### Selectivity metrics

- **Common off-targets**: kinases with pIC50 ≥ 6.90 in all six compounds
- **Compound-specific off-targets**: kinases with max pIC50 ≥ 7.05 and std ≥ 0.12 across compounds
- **Δ vs PDK1**: off-target score minus that compound's PDK1 score (per-compound reference)

---

## Results

### PDK1 engagement

| Compound | PDK1 pIC50 |
|:---|:---|
| BX912 | 6.89 |
| EL2003A | 6.47 |
| EL2003A-A2U1 | 6.86 |
| EL2003A-A4U1 | 6.91 |
| EL5001A | 6.87 |
| EL5003A | 6.93 |

EL2003A has notably weak PDK1 engagement (6.47), the lowest in the series.

### Global kinase landscape

All compounds show a flat promiscuity profile across 43 kinases (range 6.5–7.4 pIC50), typical of ATP-competitive pyrimidine/purine scaffolds. PDK1 mean across six compounds = **6.82**.

Top kinases by mean pIC50 (all six compounds):

| Kinase | Mean pIC50 | Δ vs PDK1 mean | CV | Family |
|:---|:---|:---|:---|:---|
| AurA | 7.28 | +0.46 | 0.025 | Other |
| FLT3 | 7.04 | +0.22 | 0.021 | TK |
| JAK2 | 7.04 | +0.21 | 0.014 | TK |
| FGFR1 | 7.03 | +0.20 | 0.028 | TK |
| MET | 6.96 | +0.13 | 0.016 | TK |
| CDK4 | 6.95 | +0.13 | 0.029 | CMGC |
| BRAF | 6.95 | +0.12 | 0.034 | TKL |
| EGFR | 6.95 | +0.12 | 0.008 | TK |
| ROCK2 | 6.94 | +0.12 | 0.031 | AGC |
| p38α | 6.93 | +0.11 | 0.014 | CMGC |

### Universal off-targets (pIC50 ≥ 6.90 in ALL 6 compounds)

**AurA is the only kinase meeting this criterion** (min 6.98, max 7.40, mean 7.28, CV 0.025). It is hard-wired to the shared hinge pharmacophore and cannot be removed by peripheral substitution.

### Compound-specific off-targets (max ≥ 7.05, std ≥ 0.12)

AurA satisfies these criteria (max 7.40, std 0.18) but is listed under the universal section above; it is excluded from this table to avoid double-counting.

| Kinase | Max pIC50 | Top compound | Structural driver |
|:---|:---|:---|:---|
| FGFR1 | 7.32 | EL2003A-A4U1 | CF₃ hydrophobic back-pocket |
| BRAF | 7.28 | EL2003A-A4U1 | CF₃ hydrophobic back-pocket |
| CDK4 | 7.23 | EL2003A-A4U1 | CF₃ expansion |
| ROCK2 | 7.23 | EL2003A-A2U1 | ortho-methyl tolyl |
| FLT3 | 7.21 | EL5003A | cyclopentyl ring geometry |
| PKACa | 7.08 | EL5001A | linear ethylene linker |
| BTK | 7.06 | EL2003A-A2U1 | ortho-methyl tolyl |
| ABL1 | 7.05 | EL2003A-A2U1 | ortho-methyl tolyl |

### Per-compound selectivity ranking

1. **EL5001A** — most selective; top off-targets PKACa (+0.21) and JAK2 (+0.20) are within scorer uncertainty (±0.3) of each other
2. **EL5003A** — best PDK1 pIC50 (6.93); FLT3 main concern (+0.28)
3. **BX912** — clean except AurA (+0.51)
4. **EL2003A-A2U1** — ROCK2/BRAF/BTK from tolyl group
5. **EL2003A-A4U1** — worst selectivity profile; CF₃ group drives FGFR1, BRAF, CDK4 above PDK1
6. **EL2003A** — weakest PDK1 (6.47); AurA gap +0.89; ROCK1/2 dominant; requires re-optimisation

---

## Clinical significance of top off-targets

| Off-target | Clinical risk | Reversible by SAR? |
|:---|:---|:---|
| AurA | Mitotic arrest, neutropenia, mucositis | No — scaffold-level |
| FLT3 | Myelosuppression; opportunity in FLT3-ITD AML | Partially (EL2003A-A2U1 spared) |
| JAK2 | Anaemia, thrombocytopenia, immune effects | No — scaffold-level |
| FGFR1 | Hyperphosphataemia, retinal toxicity | Yes — remove CF₃ |
| BRAF | Paradoxical MAPK activation, secondary SCC | Yes — remove CF₃ |
| CDK4 | Neutropenia, G1 arrest | Yes — remove CF₃ |
| EGFR | Dermatological effects | No — scaffold-level |
| ROCK1/2 | BP reduction; dominant for EL2003A | Partially |
| PKACa | cAMP pathway disruption | Yes — modify linker |

---

## Recommendations

1. **AurA biochemical counter-screen** is mandatory for the whole series before any in vivo work. Predicted IC50 ~50 nM is pharmacologically active.
2. **EL2003A needs potency rescue** — PDK1 pIC50 6.47 with ROCK1/2 dominant engagement; not a selective PDK1 tool compound in its current form.
3. **EL2003A-A4U1's CF₃ group** simultaneously worsens selectivity vs. FGFR1, BRAF, and CDK4. BRAF paradoxical activation is the most serious clinical concern.
4. **Advance EL5001A and EL5003A** as primary candidates pending AurA confirmation.
5. **FLT3 dual engagement** (EL2003A, EL5003A) warrants evaluation in FLT3-ITD AML cell lines — potential opportunity.

---

## Output Files

| File | Description |
|:---|:---|
| `kd2_out/PDK1_AGC/docking_results/PDK1_AGC_vina_results.csv` | AGC family results (18 kinases × 6 compounds) |
| `kd2_out/PDK1_probe5/docking_results/PDK1_probe5_vina_results.csv` | CDK2, GSK3B, EGFR, ABL1, AurA |
| `kd2_out/PDK1_batch2/docking_results/PDK1_batch2_vina_results.csv` | CMGC core (CDK1/4/6, ERK1/2, p38α, JNK1) |
| `kd2_out/PDK1_batch3/docking_results/PDK1_batch3_vina_results.csv` | TK panel (KDR, FGFR1, MET, SRC, BTK, JAK2, FLT3) |
| `kd2_out/PDK1_batch4/docking_results/PDK1_batch4_vina_results.csv` | CHEK1/2, PLK1, MEK1, BRAF, CK1d |
| `kinome_selectivity_matrix.csv` | Aggregated 6×43 pIC50 matrix |
| `kinome_heatmap.png` | Full kinome heatmap (43 kinases × 6 compounds) |
| `kinome_per_compound.png` | Per-compound top-8 off-targets vs. PDK1 |
| `kinome_selectivity_profile.md` | Full narrative report |

---

## Limitations

1. **DNN scorer uncertainty** ≈ ±0.3 pIC50 units (KLIFS benchmark). Differences < 0.2 between compounds should not be over-interpreted.
2. **Static docking only** — no MD relaxation; induced-fit effects and allosteric states not captured.
3. **43/~500 kinases covered** — full kinome scan was not performed due to compute timeout constraints. The AGC family was fully covered; other families were covered via a targeted clinical panel. Non-covered kinases include full CMGC, full TK, STE, remaining Other/CAMK/TKL.
4. **One representative KLIFS structure per kinase** in most cases — conformation-dependent selectivity (e.g. DFG-out vs. DFG-in) not fully explored.
5. **No cellular permeability or PK correction** — predicted IC50 values are biochemical; cellular activity depends on membrane permeability, efflux, and intracellular concentration.

## Verification

| Check | Method | Result |
|:---|:---|:---|
| All 5 docking runs completed rc=0 | Checked rc field in dispatch return value | ✓ All rc=0 |
| Row counts internally consistent | `df_all` 475 rows = 43 kinases × ~6 compounds × ~1.7 structures/kinase | ✓ |
| PDK1 present in AGC results | `pivot["PDK1"]` non-null for all 6 compounds | ✓ |
| AurA universal claim | `pivot["AurA"].min()` = 6.98 ≥ 6.90 threshold | ✓ |
| EL2003A PDK1 weakest | `pivot["PDK1"].idxmin()` = EL2003A (6.47) | ✓ |
| EL2003A-A4U1 top FGFR1 score | `pivot.loc["EL2003A-A4U1","FGFR1"]` = 7.32 | ✓ |
| Heatmap and per-compound figures written | `os.path.getsize(kinome_heatmap.png)` = 256 KB; `kinome_per_compound.png` = 176 KB | ✓ |
| Matrix CSV saved | `kinome_selectivity_matrix.csv` 4216 bytes, 6 rows × 44 columns | ✓ |
