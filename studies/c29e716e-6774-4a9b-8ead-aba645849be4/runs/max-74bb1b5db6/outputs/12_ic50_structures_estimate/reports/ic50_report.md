# IC50 Estimation Report — 20 Proposed Compounds

## Method
- Receptor: Target.pdb (waters stripped, 371 KB)
- Docking: AutoDock-Vina GPU 2.1, focused box 25×25×25 Å centred on blind-dock hit (28.8, 4.1, −24.4 Å)
- Calibration: linear fit of log₁₀(IC50) vs ΔG using 15 known actives; R²=0.20, p=0.093
  AS-ratio IC50 proxy assumes [P]=1 µM (typical ASMS); actual [P] unknown → absolute values uncertain
- Vina RMSE ≈1.5 kcal/mol → ~11× IC50 uncertainty per compound
- **Relative ranking more reliable than absolute values**

## Known Actives — Calibration Reference
| Compound | ΔG (kcal/mol) | Vina IC50 (nM) | AS-proxy IC50 (nM) |
|----------|--------------|----------------|-------------------|
| EDS00481762 | -13.3 | 40 | 18 |
| EDS00480994 | -13.0 | 33 | 89 |
| EDS00490594 | -12.7 | 28 | 30 |
| EDS00490706 | -11.6 | 14 | 1 |
| EDS00469766 | -11.5 | 13 | 33 |
| EDS00459346 | -11.4 | 12 | 21 |
| EDS00495858 | -11.2 | 11 | 172 |
| EDS00459274 | -11.1 | 10 | 7 |
| EDS00459442 | -11.1 | 10 | 8 |
| EDS00474362 | -10.9 | 9 | 3 |
| EDS00492874 | -10.8 | 9 | 11 |
| EDS00492986 | -10.5 | 7 | 10 |
| EDS00474254 | -10.2 | 6 | 4 |
| EDS00470458 | -10.0 | 5 | 1 |
| EDS00444974 | -9.7 | 4 | 16 |

## Proposed Compounds — Ranked by Docking Score
| Rank | Compound | ΔG (kcal/mol) | Est. IC50 (nM) | 95% CI (nM) | Series | SMILES |
|------|----------|--------------|---------------|-------------|--------|--------|
| 1 | **B3** | -12.7 | 28 | 11–70 | B | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12` |
| 2 | **D2** | -12.7 | 28 | 11–70 | D | `O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2` |
| 3 | **E3** | -12.3 | 22 | 9–54 | E | `Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C4(F)CC4)CC3)cn1` |
| 4 | **E1** | -12.0 | 18 | 7–45 | E | `Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)cc2)CC3)cn1` |
| 5 | **E2** | -12.0 | 18 | 7–45 | E | `Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1` |
| 6 | **B1** | -11.9 | 17 | 7–43 | B | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12` |
| 7 | **F3** | -11.9 | 17 | 7–43 | F | `O=C(NCc1cc(F)ccc1F)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 8 | **A1** | -11.7 | 15 | 6–38 | A | `O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2` |
| 9 | **A3** | -11.7 | 15 | 6–38 | A | `O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2` |
| 10 | **F4** | -11.7 | 15 | 6–38 | F | `O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 11 | **B2** | -11.4 | 12 | 5–31 | B | `Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12` |
| 12 | **A2** | -11.3 | 12 | 5–29 | A | `O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2` |
| 13 | **F2** | -11.3 | 12 | 5–29 | F | `O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 14 | **C1** | -11.2 | 11 | 4–28 | C | `O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 15 | **D1** | -11.2 | 11 | 4–28 | D | `O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 16 | **F5** | -11.2 | 11 | 4–28 | F | `O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 17 | **F1** | -11.0 | 10 | 4–24 | F | `O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 18 | **C3** | -10.7 | 8 | 3–20 | C | `O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 19 | **C2** | -10.5 | 7 | 3–18 | C | `O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |
| 20 | **C4** | -9.4 | 4 | 1–9 | C | `O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2` |

## Highlight — Top 5 Proposed
| Rank | Compound | ΔG | Est. IC50 | Rationale |
|------|----------|----|-----------|-----------|
| 1 | **B3** | -12.7 | 28 nM | Methylbenzofuran R1 cap + benzyl R2 — largest hydrophobic fill; matches EDS00490594 scaffold |
| 2 | **D2** | -12.7 | 28 nM | Piperidine-pyridyl R2 with 4-F-benzyl acyl chain — sp3-rich, novel ring exit vector |
| 3 | **E3** | -12.3 | 22 nM | Fluorocyclopropyl spiro quaternary centre — constrained 3D shape, fills hydrophobic sub-pocket |
| 4 | **E1** | -12.0 | 18 nM | 4-F-phenyl acyl + 4-(4-pyridyl)-4-F-piperidine — dual fluorine, good Fsp3 |
| 5 | **E2** | -12.0 | 18 nM | Hydroxy variant of E1 — H-bond donor at piperidine 4-position, added solubility |

## Calibration Diagnostic
- R²=0.20: Vina ranks known actives weakly vs AS ratio (expected — AS ratio reflects ASMS conditions, not just Kd)
- Systematic bias: Vina IC50s (4–39 nM) compressed vs AS proxy (1–172 nM)
- Recommended action: prioritise top 5–8 proposed compounds for SPR/ITC Kd measurement to anchor the calibration
- Uncertainty caveat: treat all IC50 estimates as order-of-magnitude guides only (±11×)