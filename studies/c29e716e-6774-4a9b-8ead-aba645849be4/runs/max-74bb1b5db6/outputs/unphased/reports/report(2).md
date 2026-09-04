
## Method

| Parameter | Value |
|-----------|-------|
| Receptor | Target.pdb, waters stripped (371 KB) |
| Docking engine | AutoDock-Vina GPU 2.1 |
| Binding site | Blind-dock centroid: (28.8, 4.1, −24.4 Å); box 25×25×25 Å |
| Exhaustiveness | 8; 3 poses per compound; seed 42 |
| Calibration | Linear fit log₁₀(IC50) = −0.269·ΔG − 1.971; R²=0.20, p=0.093 (n=15 known actives) |
| IC50 proxy | AS-ratio × 1000 nM (assumes [Protein]=1 µM ASMS; [P] unknown → absolute values uncertain) |
| Uncertainty | Vina RMSE ≈1.5 kcal/mol → **~11× per-compound IC50 uncertainty** |

> **Relative ranking is more reliable than absolute IC50 values.** The weak calibration R²=0.20 reflects ASMS AS-ratio capturing assay conditions beyond pure Kd. Treat IC50 estimates as order-of-magnitude guides.

---

## Known Actives — Calibration Reference

| Compound | ΔG (kcal/mol) | Vina IC50 (nM) | AS-proxy IC50 (nM) |
|----------|:---:|:---:|:---:|
| EDS00481762 | −13.3 | 40 | 18 |
| EDS00480994 | −13.0 | 33 | 89 |
| EDS00490594 | −12.7 | 28 | 30 |
| EDS00490706 | −11.6 | 14 | 1 |
| EDS00469766 | −11.5 | 13 | 33 |
| EDS00459346 | −11.4 | 12 | 21 |
| EDS00495858 | −11.2 | 11 | 172 |
| EDS00459274 | −11.1 | 10 | 7 |
| EDS00459442 | −11.1 | 10 | 8 |
| EDS00474362 | −10.9 | 9 | 3 |
| EDS00492874 | −10.8 | 9 | 11 |
| EDS00492986 | −10.5 | 7 | 10 |
| EDS00474254 | −10.2 | 6 | 4 |
| EDS00470458 | −10.0 | 5 | 1 |
| EDS00444974 | −9.7 | 4 | 16 |

*Range: Vina 4–40 nM vs AS proxy 1–172 nM; Vina compresses dynamic range.*

---

## Proposed Compounds — Ranked by Docking Score

| Rank | Compound | ΔG (kcal/mol) | Est. IC50 (nM) | 95% CI (nM) | Series | Design rationale |
|:----:|----------|:---:|:---:|:---:|:---:|:---|
| **1** | **B3** | −12.7 | **28** | 11–70 | B | Methylbenzofuran R1 + 4-F-benzyl R2; largest hydrophobic fill; matches EDS00490594 scaffold |
| **2** | **D2** | −12.7 | **28** | 11–70 | D | Piperidine-pyridyl at R2 + 4-F-phenylacetyl R1; sp³-rich, novel vector |
| **3** | **E3** | −12.3 | **22** | 9–54 | E | Fluorocyclopropyl spiro quaternary; constrained 3D shape fills hydrophobic sub-pocket |
| **4** | **E1** | −12.0 | **18** | 7–45 | E | 4-F-phenyl acyl + 4-(4-pyridyl)-4-F-piperidine; dual fluorine, high Fsp³ |
| **5** | **E2** | −12.0 | **18** | 7–45 | E | Hydroxy variant of E1; H-bond donor at C4, added aqueous solubility |
| 6 | B1 | −11.9 | 17 | 7–43 | B | Methylbenzofuran R1 + 4-pyridylmethyl R2; hinge-like H-bond acceptor |
| 7 | F3 | −11.9 | 17 | 7–43 | F | 2,4-di-F-benzyl R2 + 2,2,2-trifluoroethoxy pyridine R1; bi-fluorinated |
| 8 | A1 | −11.7 | 15 | 6–38 | A | Ortho-pyrrolo-benzyl R2; constrained ortho vector, no Brenk flag |
| 9 | A3 | −11.7 | 15 | 6–38 | A | Trifluoromethyl-pyridine R1 variant of A1 |
| 10 | F4 | −11.7 | 15 | 6–38 | F | Methylsulfonyl-benzyl R2; polar tail for solubility |
| 11 | B2 | −11.4 | 12 | 5–31 | B | Methylbenzofuran R1 + THP-methyl R2; saturated ring reduces cLogP |
| 12 | A2 | −11.3 | 12 | 5–29 | A | OCF₃-pyridine R1 + ortho-pyrrolo-benzyl R2 |
| 13 | F2 | −11.3 | 12 | 5–29 | F | Thiophen-3-yl-methyl R2; bioisostere for phenyl |
| 14 | C1 | −11.2 | 11 | 4–28 | C | Morpholino-pyridyl R2; basic nitrogen, improved aqueous solubility |
| 15 | D1 | −11.2 | 11 | 4–28 | D | 4,4-di-F-cyclohexyl R2; gem-difluoro conformational lock |
| 16 | F5 | −11.2 | 11 | 4–28 | F | Methylsulfonyl-piperidine R2; sulfonamide H-bond acceptor |
| 17 | C3 | −10.7 | 8 | 3–20 | C | Pyridylmethyl R2; less lipophilic than benzyl |
| 18 | C2 | −10.5 | 7 | 3–18 | C | THP-methyl R2; fully saturated, high Fsp³ |
| 19 | F1 | −11.0 | 10 | 4–24 | F | N-methyl-piperidine R2 (simplest F-series baseline) |
| 20 | C4 | −9.4 | 4 | 1–9 | C | Ethanolamine R2; weakest score, likely solvent-exposed |

---

## Top 5 — Synthesis Priority

| Priority | Compound | ΔG | IC50 est. | Key feature |
|:--------:|----------|----|-----------|-------------|
| 1 | **B3** | −12.7 | 28 nM | Benzofuran + 4-F-benzyl; direct scaffold extension of two strong actives |
| 2 | **D2** | −12.7 | 28 nM | Piperidine-pyridyl; new sp³ exit vector, high 3D character |
| 3 | **E3** | −12.3 | 22 nM | Fluorocyclopropyl quaternary; rigid shape, novel chemical space |
| 4 | **E1** | −12.0 | 18 nM | Dual-F piperidine; clean PAINS/Brenk profile |
| 5 | **E2** | −12.0 | 18 nM | Hydroxy-E1; H-bond donor, solubility handle |

---

## Calibration Diagnostic

- **R²=0.20**: Vina ↔ AS-ratio correlation weak (expected; AS ratio reflects ASMS incubation conditions, not Kd alone)
- **Vina compresses range**: scores cluster in −9.4 to −12.7 kcal/mol; AS proxy spans 1–172 nM
- **Next step**: SPR or fluorescence polarisation Kd for top 5 compounds to anchor the calibration; replace order-of-magnitude IC50s with measured values
- **All 20 proposed compounds score ≥ EDS00444974** (−9.7 kcal/mol, AS ratio 0.016), the weakest known active — none predicted weaker than the training floor

---

*Docking: AutoDock-Vina GPU 2.1. Calibration anchored to 15 ASMS confirmed actives. IC50 estimates ±11× (1.5 kcal/mol Vina RMSE). Intended for synthetic prioritisation only.*
