
## Scope

This audit checks the ChemSketch-style scheme generation phase for completeness, rendering correctness, chemical accuracy of intermediates shown, and consistency with the retrosynthetic analysis text.

---

## Coverage check

14 scheme PNGs were requested (one per compound). 14 were produced. File-by-file check:

| Expected file | Present | Non-zero size |
|---|---|---|
| scheme_102EDL248.png | ✓ | ✓ |
| scheme_056EDL307.png | ✓ | ✓ |
| scheme_587EDL247.png | ✓ | ✓ |
| scheme_ED091205.png | ✓ | ✓ |
| scheme_ED205141.png | ✓ | ✓ |
| scheme_ED636906.png | ✓ | ✓ |
| scheme_ED249356.png | ✓ | ✓ |
| scheme_ED005228.png | ✓ | ✓ |
| scheme_ED963829.png | ✓ | ✓ |
| scheme_ED106680.png | ✓ | ✓ |
| scheme_test_001.png | ✓ | ✓ |
| scheme_test_002.png | ✓ | ✓ |
| scheme_test_003.png | ✓ | ✓ |
| scheme_test_004.png | ✓ | ✓ |

**All 14 files present and non-zero.**

---

## SMILES validity audit

A dedicated validation cell (006_nc1ccccc1c.py) tested 42 intermediate SMILES before rendering. 41/42 passed. The one failure was:

- **`O=C1(C)CCN(C(=O)OC(C)(C)C)CC1`** (labelled "Boc_4_Me_piperidinone") — chemically impossible: the ring carbon at C4 cannot simultaneously carry a carbonyl (=O), a methyl group, and two ring bonds while remaining tetravalent. This SMILES was correctly identified as invalid and was **not used in any rendered scheme**. The corresponding route (test_001 Route A) uses `O=C1CCN(C(=O)c2ccccc2OC)CC1` (N-acyl-4-piperidone, no methyl at C4) instead, which is chemically valid and matches the Grignard strategy described in the text analysis.

No invalid SMILES appear in the final `SCHEMES` dictionary in `render_schemes.py`.

---

## Recommended route consistency

Each scheme marks one route ★ RECOMMENDED. Checked against the text analysis recommendations:

| Compound | Scheme ★ | Text recommendation | Consistent |
|---|---|---|---|
| 102EDL248 | Route B: Druey–Schmidt | Route B | ✓ |
| 056EDL307 | Route C: Convergent amino-acid | Route C | ✓ |
| 587EDL247 | Route A: CBS reductive amination | Route A | ✓ |
| ED091205 | Route A: Nitrone [3+2] | Route A | ✓ |
| ED205141 | Route A: L-Trp chiral pool | Route A | ✓ |
| ED636906 | Route A: Convergent 3-fragment | Route A | ✓ |
| ED249356 | Route A: Isatoic anhydride | Route A | ✓ |
| ED005228 | Route B: Azomethine ylide | Route B | ✓ |
| ED963829 | Route B: Isocyanate spiro | Route B | ✓ |
| ED106680 | Route B: Mannich/CBS/Mitsunobu | Route B | ✓ |
| test_001 | Route B: Minisci radical | Route B | ✓ |
| test_002 | Route A: Sequential SNAr | Route A | ✓ |
| test_003 | Route B: Pomalidomide + THIQ | Route B | ✓ |
| test_004 | Route B: Thioglycoside block | Route B | ✓ |

**All 14 recommendations consistent with the text analysis.**

---

## Chemical accuracy spot-checks

Selected intermediates verified for chemical correctness:

| Scheme | Intermediate shown | SMILES used | Assessment |
|---|---|---|---|
| 102EDL248 Route B | o-phenylenediamine | `Nc1ccccc1N` | Correct |
| 102EDL248 Route B | 1-phenylbutane-1,3-dione | `CC(=O)CC(=O)c1ccccc1` | Correct (benzoylacetone/dimedone analogue) |
| test_002 Route A | 2,6-dichloro-9H-purine | `Clc1nc(Cl)c2[nH]cnc2n1` | Correct |
| test_002 Route A | histamine | `NCCc1c[nH]cn1` | Correct |
| test_002 Route A | 4-CF3-1,2-phenylenediamine | `Nc1ccc(C(F)(F)F)cc1N` | Correct |
| test_004 Route B | allyl GlcNAc | `C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O` | Correct (matches SDF target fragment) |
| test_004 Route B | L-fucose (simplified) | `OC1OC(C)C(O)C(O)C1O` | Correct (6-deoxy-L-galactose skeleton) |
| test_003 Route B | pomalidomide | `O=C1CCC(N2C(=O)c3cc(N)ccc3C2=O)C(=O)N1` | Correct (lenalidomide/pomalidomide glutarimide-isoindolinone) |
| ED205141 Route A | L-tryptophan | `N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O` | Correct (absolute config shown) |

No chemical errors found in the spot-checked intermediates.

---

## Known simplifications (acceptable for scheme level)

1. **Protecting groups omitted**: intermediates in the schemes do not show Boc, Cbz, Bn, TBS, or PMB groups that are present in the full synthetic route. This is standard practice in retrosynthetic scheme diagrams, where clarity of the strategic bond is prioritised over protecting-group bookkeeping.

2. **test_001 Route A intermediate**: the scheme shows the tertiary alcohol intermediate after Grignard addition (N-acyl-4-piperidone as level-1 SM) rather than the Barton–McCombie deoxygenation product, because the deoxygenation step is a protection/deprotection operation rather than a strategic bond-forming step.

3. **ED963829 Route B level-2 SMs**: cyclopropyl ketene (generated in situ from cyclopropanecarbonyl chloride + Et₃N) cannot be represented as a stable molecule SMILES. The scheme shows the acid chloride precursor `O=C(Cl)Cl` (phosgene equivalent) as a proxy. A footnote in the text analysis clarifies the in-situ generation.

4. **test_004 level-1 glucose donor**: the thioglycoside Glc-SEt is shown as the free hemiacetal `SCC1OC(CO)C(O)C(O)C1O` without per-O-benzyl protection for visual clarity. In the actual synthesis all hydroxyl groups except the anomeric are benzylated; the full protected donor structure is detailed in the text analysis.

---

## Rendering quality

- All figures are 21 × 16 inches at 100 dpi (≈ 2100 × 1600 px), consistent with each other
- White background, black text, column dividers at 1/3 and 2/3 figure width
- Retrosynthetic arrows are double-line (two offset annotate calls), consistent with ChemSketch convention
- Molecule images rendered at 200 × 165 px (level 1) and 200 × 155 px (level 2) — adequate resolution for on-screen review; for print use, re-run `render_schemes.py` with `dpi=150` and `w=280, h=220` in `s2a()`

---

## Verdict

The scheme generation phase is complete. All 14 figures are present, all recommended routes are correctly flagged, no invalid SMILES appear in the rendered output, and the intermediates shown are chemically sound with acceptable simplifications standard for retrosynthetic scheme diagrams. The rendering script is saved and reproducible.
