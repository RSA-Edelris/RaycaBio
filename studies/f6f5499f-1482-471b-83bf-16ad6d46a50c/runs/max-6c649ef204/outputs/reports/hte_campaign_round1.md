
## Summary

Campaign to optimise the Ni/photoredox dual-catalytic decarboxylative C(sp³)–C(sp³) cross-coupling between N-Cbz-4-bromopiperidine (electrophile) and N-Boc-1-azaspiro[5.2]octane-4-carboxylic acid (radical precursor) at fixed 470 nm irradiation, 24-well plate format.

| Item | Value |
|------|-------|
| Substrate 1 (electrophile) | BrC1CCN(CC1)C(=O)OCc2ccccc2 — N-Cbz-4-bromopiperidine |
| Substrate 2 (acid) | CC(C)(C)OC(=O)N1CC2(CC2)CC1C(=O)O — N-Boc-spirocyclic α-amino acid |
| Mechanism | Ni(I/II/III) + PC*(oxidative quench) decarboxylative radical cross-coupling |
| Reagent file | HTE_Edelris.sdf — 72 molecules, properties: MOL_NAME, CAS_NUMBER, Role |

---

## Phase 1 — Reagent Inventory

### Parse output

The SDF file was read with RDKit (`SDMolSupplier`). All 72 molecules were extracted; properties available: `MOL_NAME`, `CAS_NUMBER`, `Role` (all three columns blank in this file — names were inferred from SMILES and MW).

**Code:** `001_chem_sdmolsupplier.py`, `002_extract_all_molecules_their_properties.py`  
**Table:** `003_extract_all_molecules_their_properties.csv` (72 rows × 4 columns: index, name, CAS, SMILES, MW)

### Classification summary (72 reagents)

| Class | Count | Kit indices |
|-------|-------|-------------|
| Photocatalyst — Ir | 4 | 12, 31, 35, 58 |
| Photocatalyst — Ru | 3 | 13, 15, 33 |
| Photocatalyst — Organic | 5 | 5, 6, 32, 38, 60 |
| Ni catalyst | 4 | 10, 21, 34, 55 |
| Pd catalyst (not used) | 20 | 0, 2, 3, 7–9, 14, 16–19, 30, 36, 39–40, 47, 56, 59, 61, 63 |
| Bidentate N-Ligand for Ni | 8 | 1, 4, 11, 22, 26, 27, 46, 57 |
| Chiral N-ligand | 1 | 62 |
| Inorganic base | 4 | 50, 51, 52, 53 |
| Alkoxide / silyl base | 3 | 23, 42, 43 |
| Amine / amidine base | 5 | 29, 37, 41, 48, 71 |
| Solvent | 9 | 24, 25, 64, 65, 66, 67, 68, 69, 70 |
| Cu catalyst | 1 | 49 |
| Amine / HAT additive | 1 | 28 (quinuclidine) |

### Audit — Phase 1

- All 72 entries parsed without error; 0 `None` returns from `SDMolSupplier`.
- Role field is blank for all 72 molecules in the source SDF; classification was performed by SMILES and MW cross-reference.
- Duplicate entry confirmed: rows 37 and 71 are both DBU (C1CCC2=NCCCN2CC1, MW 152.2).
- **Absolutely necessary reagents check:** photocatalyst ✓, Ni catalyst ✓, bidentate N-ligand ✓, inorganic base ✓, polar aprotic solvent (DMA kit #66) ✓. Nothing essential is absent.
- MeCN is absent (not in any of the 72 entries). This is the most common solvent gap for this reaction class.

---

## Phase 2 — HTE Campaign Design

### Response

| Item | Decision |
|------|----------|
| Response | Relative conversion (%): product area / (product + SM areas) × 100 |
| Measurement | UPLC with internal standard (1,3,5-trimethoxybenzene, 1 equiv) |
| Assay precision | ±3–5% absolute (well-to-well handling CV dominates) |
| Decision threshold | ≥30% = hit for Round 2; ≥60% = direct optimisation candidate |

### Factors varied — all categorical

| Factor | Levels | Source |
|--------|--------|--------|
| Photocatalyst | 4 | See table below |
| Ni bidentate N-ligand | 3 | dtbbpy (kit #27), 4,4′-dMe-bpy (kit #1), 1,10-phen (kit #46) |
| Inorganic base | 2 | Cs₂CO₃ (kit #52), K₃PO₄ (kit #53) |

**Photocatalyst selection rationale (E\* must exceed Ep(ox) ≈ 0.9–1.1 V for the N-Boc α-amino acid carboxylate):**

| Row | PC | E\* vs SCE | Notes |
|-----|----|-----------|-------|
| A | Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆ (kit #31) | +1.32 V | MacMillan reference; most precedented for this class |
| B | 4CzIPN (kit #38) | +1.52 V | Organic PC; cost-effective; widely validated |
| C | Mes-Acr⁺·BF₄ (kit #32) | +2.00 V | Highly oxidising; risk of over-oxidation side reactions |
| D | Ir[dF(4-tBupy)]₂(dtbbpy) (kit #12) | ~+1.10 V | Borderline for this carboxylate; internal low-E\* reference |

### Factors held constant

NiBr₂·dme 10 mol% (kit #21) · DMA 0.1 M (kit #66) · electrophile 1.0 equiv · acid 1.5 equiv · base 2.0 equiv · PC 1 mol% · 470 nm · rt · 16 h · N₂.

### Design type

**Full 4 × 3 × 2 factorial = 24 runs = one plate.** Selected because:
1. All factors are categorical — RSM and DSD are inappropriate.
2. 4 × 3 × 2 = 24 exactly fills one plate with zero waste.
3. All main effects (6 df) and all 2-way interactions (11 df) are estimable; 3-way PC×Lig×Base (6 df) serves as error surrogate.

No dedicated control wells (all 24 needed for factorial). SM recovery tracked as mass-balance proxy.

### Pre-registered model

```
Y_ijk = µ + α_i(PC) + β_j(Lig) + γ_k(Base) + (αβ)_ij + (αγ)_ik + (βγ)_jk + ε_ijk
```

Error = PC×Lig×Base (6 df), assuming negligible 3-way interaction. Response transformed with arcsin√(p/100) if data cluster near 0 or 100%.

### Round structure and Bayesian comparison

| Round | Plate | Variables | Decision rule |
|-------|-------|-----------|---------------|
| 1 | This plate | PC × Lig × Base | ≥1 well ≥30%: go to Round 2; 0 wells ≥10%: re-examine mechanism |
| 2 (if hit) | 1 plate | Concentration, base stoichiometry, temperature, time (2⁴ CCD + 4 centre points + 4 axial) | ≥60%: scale up; 30–60%: Round 3 stoichiometry sweep |
| 3 (if needed) | 1 plate | Acid equiv (1.0–2.5), quinuclidine HAT additive | ≥60%: scale up |

**Bayesian BO vs. full factorial:** BO offers no advantage for Round 1 because the entire candidate space (24 conditions) equals the plate capacity — nothing to sub-sample. BO becomes beneficial in Round 2+ when continuous variables expand the search space beyond one plate.

### Audit — Phase 2

- Design is estimable: 23 df assigned (3 + 2 + 1 + 6 + 3 + 2 + 6 = 23 ✓).
- No confounding in the full factorial; all contrasts are orthogonal.
- PC Row D (E\* ≈ +1.10 V) is deliberately included as a borderline reference; expected low conversion validates the E\* threshold.
- Dispensing order randomised (Python `random.seed(42)`); sequence recorded in `005_full_experiment_table_randomised_dispensing_order.py`.

---

## Phase 3 — Plate Map

**Output:** `plate_map_round1.png`

![Round 1 plate map](plate_map_round1.png)

**Colour key:**
- Deep blue (Row A) = Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆
- Green (Row B) = 4CzIPN
- Red (Row C) = Mes-Acr⁺·BF₄
- Purple (Row D) = Ir[dF(4-tBupy)]₂(dtbbpy)
- No hatch (Cols 1–2) = dtbbpy
- Diagonal hatch (Cols 3–4) = 4,4′-dMe-bpy
- Cross hatch (Cols 5–6) = 1,10-phen
- Text "Cs" = Cs₂CO₃ · Text "K₃P" = K₃PO₄

### Audit — Phase 3

- 24 wells rendered; well IDs A1–D6 all present and unique.
- Row and column assignments consistent with design table.
- Legend covers all four visual encodings: PC colour, ligand hatch, base text, fixed-condition footer.
- Image resolution 160 dpi; font sizes legible at print.

---

## Reagents to Purchase

| Reagent | Gap it fills | Priority |
|---------|-------------|----------|
| Acetonitrile (MeCN) | Most used solvent for Ni/photoredox; absent from kit | High |
| [Ir(dF(CF₃)ppy)₂(bpy)]PF₆ | Decouples PC ancillary ligand from Ni ligand (kit #31 uses dtbbpy in both) | Medium |
| 4,4′-di-CF₃-2,2′-bipyridine | Completes electron-poor Ni-ligand series; kit has only 5,5′-dCF₃ (kit #11) | Medium |
| Phenylsilane (PhSiH₃) | HAT catalyst for radical chain; entirely absent from kit | Medium |
| HFIP or TFE | Fluorinated alcohol cosolvent for Ni intermediate stabilisation | Low |
