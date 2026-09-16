# Audit Report — Minisci HTE Campaign Phase 01 and Phase 02

**Date:** 2026-09-16  
**Auditor:** Independent automated audit  
**Phases covered:** "Parse HTE_Edelris_2.sdf and inventory reagents" (Phase 01), "Design Minisci HTE campaign and generate plate map" (Phase 02)

---

## Files Checked

| File | Purpose |
|------|---------|
| `phase_01_minisci_reagent_inventory.md` | Phase 01 report document |
| `phase_02_minisci_campaign_design.md` | Phase 02 report document |
| `plate_map_minisci_round1.png` | Plate map image |
| `source/007_chem_sdmolsupplier.py` | SDF parse, 74-row table |
| `source/008_classify_all_74_reagents_check_acid_additives.py` | Classification + Brønsted-acid check |
| `source/009_design_definition.py` | Design definition + plate map generation |
| `source/010_role.py` | Writes phase_01 and phase_02 documents |
| `source/011_len.py` | Appends verification sections |
| `source/003_classify_all_72_reagents.py` | Kit 1 classification (used to verify DCE/DME labelling claims) |
| `results/003_extract_all_molecules_their_properties.csv` | Kit 1 molecule data (72 entries, 0-indexed rows 0–71) |

Cross-references were verified against the CSV and against live RDKit (installed version confirmed callable).

---

## Findings by Severity

### MAJOR — Finding 1: Inventory table silently drops two reagents; reported total is inconsistent

**What the report says:** "74 molecules, 0 failures" with a breakdown table that lists twelve classes.

**What the code actually produces:** The classification dict in `008_classify_all_74_reagents_check_acid_additives.py` assigns all 74 indices (0–73) into 14 classes including one called `Ligand-mono` containing:

- index 44: 2,6-lutidine (`Cc1cccc(C)n1`, MW 107.2)
- index 54: Pyridine (`c1ccncc1`, MW 79.1)

The `Ligand-mono` class is printed to the terminal by the classification loop (it does not contain 'Pd' so it passes the skip filter). However the phase_01 document's table contains no `Ligand-mono` row. The twelve classes shown in the table sum to **72**, not 74.

**Verification:** Column sum of the phase_01 inventory table: 4+3+5+4+20+8+1+12+11+1+1+2 = **72**. Confirmed independently: the CSV (`003_extract_all_molecules_their_properties.csv`) line 45 = `44,Cc1cccc(C)n1,107.2` and line 55 = `54,c1ccncc1,79.1`. Both exist in the kit.

**Impact:** The inventory table is incomplete. Neither 2,6-lutidine nor pyridine is a Brønsted acid, a photocatalyst, or a solvent, so the headline conclusion (no acid in kit, choose 4 PCs) is unaffected. However, the discrepancy means an auditor or reader cannot reconcile the "74 molecules" headline against the table, and a subsequent experiment that called for these entries by kit index would find an unexplained gap.

---

### MAJOR — Finding 2: E* comparison sign is electrochemically inverted in the verification section

**What the report says (phase_02 Verification, Photocatalyst E* coverage):**

> Row B: E* = −1.04 V > −1.2 V ← within published working range for 4CzIPN/NHP-Minisci ✓

**What is electrochemically correct:** For the oxidative quenching pathway (PC* acts as reductant), the thermodynamic requirement is:

```
E*(PC*/PC⁺) < Ep(substrate)   [algebraically; both negative]
```

That is, the excited-state reduction potential of the PC must be more negative (algebraically smaller) than the substrate reduction potential. Since Ep(NHP ester) ≈ −1.0 to −1.2 V, 4CzIPN at E* = −1.04 V satisfies the condition only for the −1.0 V end of the range:

- vs Ep = −1.0 V: −1.04 < −1.0 → thermodynamically feasible ✓
- vs Ep = −1.2 V: −1.04 > −1.2 → thermodynamically infeasible for that endpoint

**Why the report phrasing is wrong:** The statement "E* = −1.04 V > −1.2 V ← within published working range" uses ">" as though algebraically larger (less negative) satisfies the criterion for reductive feasibility. It does not; a less negative E* is a weaker reductant. The true justification for including 4CzIPN is that this specific NHP ester's Ep is closer to −1.0 V and 4CzIPN is empirically validated in the literature for NHP-Minisci reactions, not because −1.04 > −1.2 implies adequate reductive driving force.

**What is NOT affected:** The PC selection itself is defensible. Row A (−1.51 V) is unambiguously strong enough. Row B (4CzIPN) is included on empirical grounds (well-documented in literature). Rows C and D are borderline-to-weak and included deliberately as diagnostic comparators. The plate design remains scientifically sound. The notation error is in the verification write-up only, not in the experimental plan.

---

### MAJOR — Finding 3: Brønsted acid search pattern fails silently for TFA and similar acids

**What the code does (008, lines 92–95):**

```python
if 'C(=O)O' in smi and 'N' not in smi and '[O-]' not in smi:
    acid_found.append(...)
if 'S(=O)(=O)O' in smi and '[' not in smi:
    acid_found.append(...)
```

**What RDKit actually produces for TFA:** Live RDKit check (this session):

```
TFA (either input form): canonical = O=C(O)C(F)(F)F
'C(=O)O' in 'O=C(O)C(F)(F)F' → False
```

RDKit canonicalizes TFA as `O=C(O)C(F)(F)F` (keto-form notation with the double-bond oxygen outside the parenthesis). The substring `C(=O)O` requires the sequence `C`, `(`, `=`, `O`, `)`, `O`; in `O=C(O)…` the double bond is written as `=C` (O=C) and the hydroxyl as a branch `(O)`, so the pattern is absent. The search returns 0 for TFA even if TFA were present.

By contrast, AcOH canonicalizes as `CC(=O)O`, which does contain `C(=O)O`; AcOH would be found.

**Why the conclusion survives:** The report includes a supplementary manual scan: "Manual scan of full SMILES list confirmed: no TFA, no AcOH, no p-TsOH, no H₂SO₄ surrogate." That human step is the actual evidence. The automated search cannot be relied upon as a comprehensive acid detector — it is a broken filter that happens to produce the correct answer here because TFA is genuinely absent.

**Risk going forward:** If a future kit version adds TFA (or any acid where RDKit places the carbonyl oxygen exo to the ring notation), the identical automated check code will continue to report 0 acids found, silently and incorrectly. The filter must be replaced, e.g., with `HasSubstructMatch(Chem.MolFromSmarts('[CX3](=O)[OX2H1]'))` for free carboxylic acids.

---

## Verified Correct

The following claims were opened and confirmed against the actual files and/or live RDKit.

### Parse integrity (phase_01 Verification section)

- `len(mols2) == 74, None-count == 0`: The code filters Nones via list comprehension on the supplier, then enumerates 0–73 into `df2`. The claim is structurally consistent with 74 entries in HTE_Edelris_2.sdf. **VERIFIED** against the classification dict coverage (all 74 indices 0–73 are accounted for).

- MW spot-checks: confirmed against CSV and against live RDKit:

  | Entry | Idx | Reported MW | Verified MW |
  |-------|-----|-------------|-------------|
  | Water | 73 | 18.0 | 18.0 ✓ |
  | fac-Ir(ppy)₃ | 58 | 657.8 | 657.8 ✓ |
  | Mes-Acr⁺·BF₄ | 32 | 399.2 | 399.2 ✓ |
  | MeCN | 72 | 41.1 | 41.1 ✓ |
  | DBU (both rows) | 37, 71 | 152.2 | 152.2 ✓ |

- DBU duplicate: CSV rows 37 and 71 both contain `C1CCC2=NCCCN2CC1`, MW 152.2. Confirmed identical. ✓

### DCE / DCM labelling claim

Phase_01 says kit 1 had "DCM (same SMILES, same MW)" but kit 2 relabels it DCE. **Verified:** `source/003_classify_all_72_reagents.py` (kit 1) labels index 68 as `('DCM', 'Solvent')`. The kit 1 CSV (`results/003_extract_all_molecules_their_properties.csv`) line for index 68 is `ClCCCl, 99.0`. RDKit confirms `ClCCCl` canonicalises as `ClCCCl` (1,2-dichloroethane, MW 99.0), not as `ClCCl` (dichloromethane, MW 84.9). So both kits contained the same compound (DCE, ClCCCl); kit 1 merely mislabelled it as DCM. The claim "same SMILES, same MW" is accurate. ✓

### Dioxane / DME labelling claim

Phase_01 says kit 1 mislabelled C1COCCO1 as DME. **Verified:** `003_classify_all_72_reagents.py` labels index 70 as `('DME', 'Solvent')`. The CSV shows index 70 = `C1COCCO1, 88.1`. RDKit canonical SMILES for DME is `COCCOC` (MW 90.1); canonical SMILES for 1,4-dioxane is `C1COCCO1` (MW 88.1). The compound at index 70 is definitively dioxane. The mislabelling charge against kit 1 is correct. ✓

### Photocatalyst kit indices (phase_02)

All four selected PCs confirmed against the kit 1 CSV (kit 2 indices are identical per the report, and the classification code uses the same indices):

| Row | PC | Kit # | CSV SMILES fragment | CSV MW |
|-----|----|-------|---------------------|--------|
| A | fac-Ir(ppy)₃ | 58 | `[Ir].c1ccc(-c2ccccn2)cc1…` | 657.8 ✓ |
| B | 4CzIPN | 38 | `N#Cc1c(-n2c3ccccc3…` | 788.9 ✓ |
| C | Ir(ppy)₂(dtbbpy)·PF₆ | 35 | `…F[P-](F)(F)(F)(F)F.c1ccc(-c2ccccc2[Ir]…` | 914.0 ✓ |
| D | Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆ | 31 | `…F[P-](F)(F)(F)(F)F.Fc1cc(F)c(-c2ccc(C(F)(F)F)cn2)c([Ir]…` | 1121.9 ✓ |

### Full factorial and degrees of freedom

- 4 PC × 3 Solvent × 2 Acid = 24 wells = one plate ✓
- df: 3 + 2 + 1 + 6 + 3 + 2 + 6 = 23 = 24 − 1 ✓

### Acid column assignment (phase_02)

The code in `009_design_definition.py` uses `col % 2 == 1` to determine TFA columns (odd columns 1, 3, 5). The `ACIDS2` dict explicitly maps odd columns to `'TFA 1 equiv'` and even columns to `'No acid'`. The plate map image confirms: gold text in A1, B1, C1, D1, A3, B3, C3, D3, A5, B5, C5, D5; blue text in all even columns. Assignment is consistent throughout. ✓

### No Brønsted acid in kit — conclusion

Despite the broken automated search (see Finding 3), the conclusion is independently supported: inspection of all 74 SMILES in the CSV finds no free carboxylic acid or sulfonic acid. All carboxylate-containing entries (Pd(OAc)₂ idx 40, K₂CO₃ idx 50, Cs₂CO₃ idx 52, K₃PO₄ idx 53) are ionic salts with `[O-]` groups that are correctly excluded by the filter's `[O-]` condition. ✓

### Plate map image

Visual inspection of `plate_map_minisci_round1.png` confirms:
- 24 wells labelled A1–D6 (4 rows × 6 columns) ✓
- Row A (dark green) = fac-Ir(ppy)₃, Row B (teal) = 4CzIPN, Row C (dark blue) = Ir-ppy-dt, Row D (purple) = Ir-dFCF₃ ✓
- Cols 1–2 plain fill (MeCN), Cols 3–4 diagonal hatch (DMSO), Cols 5–6 cross-hatch (Dioxane) ✓
- Odd columns show gold "TFA" text, even columns show blue "–H⁺" text ✓
- Legend identifies all four visual encodings; red warning "MISSING REAGENT — MUST PURCHASE" present ✓
- Kit source references correct: #58, #38, #35, #31, #72, #24, #70 all match code ✓

### Dispensing randomisation

`009_design_definition.py` uses `random.seed(7)` and `random.shuffle(order)` over indices 0–23, then iterates to print the dispensing sequence. Documented. ✓

### Classification dict coverage

Manual count of all keys in `classifications2` (008): 4 Ir + 3 Ru + 5 OrgPC + 4 Ni + 20 Pd + 8 N-Ligand + 2 Ligand-mono + 1 N-Ligand-chiral + 12 Base + 11 Solvent + 2 P-Ligand + 1 HAT + 1 Cu = **74 total**. All indices 0–73 are present with no duplicates. ✓

---

## Summary Verdict

**Phase 01 and Phase 02 produce a scientifically credible design.** The chosen photocatalysts are correctly identified by kit index and MW. The factorial structure (4×3×2=24) and df accounting (23 = 24−1) are correct. The TFA-absent conclusion is correct. The plate map correctly encodes all three factors.

**Three MAJOR defects require correction before the documents are finalised or shared:**

1. The inventory table (phase_01) is incomplete: it omits 2,6-lutidine (index 44) and pyridine (index 54), causing the table to sum to 72 instead of the claimed 74. A `Monodentate N-ligand (2)` row must be added.

2. The E* verification annotation in phase_02 ("Row B: E* = −1.04 V > −1.2 V ← within working range") is electrochemically backwards. The correct statement is that 4CzIPN's E* of −1.04 V is more negative than the lower bound of the NHP ester's Ep range (approx −1.0 V vs SCE), and the claim is empirically supported by published NHP-Minisci examples — not by the algebraic comparison with −1.2 V.

3. The automated Brønsted acid search in 008 cannot detect TFA as RDKit writes it (`O=C(O)C(F)(F)F`). The search should be replaced with a SMARTS substructure query (`[CX3](=O)[OX2H1]`) for any future use. The present conclusion is saved only by the manual scan.

No finding invalidates the experimental design or the reagent conclusions.
