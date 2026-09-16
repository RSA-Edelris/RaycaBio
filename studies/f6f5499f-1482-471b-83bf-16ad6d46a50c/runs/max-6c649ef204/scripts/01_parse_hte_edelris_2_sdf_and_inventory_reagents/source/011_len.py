
phase1_verification = """
## Verification

### Parse integrity
- `len(mols2) == 74` confirmed; `None`-count == 0 (no failed parses).
- MW spot-checks: Water idx 73 → 18.0 ✓; fac-Ir(ppy)₃ idx 58 → 657.8 ✓;
  Mes-Acr⁺·BF₄ idx 32 → 399.2 ✓; MeCN idx 72 → 41.1 ✓.
- Duplicate confirmed: rows 37 and 71 both return SMILES `C1CCC2=NCCCN2CC1`, MW 152.2 (DBU).

### Brønsted-acid check
- Search criteria: SMILES containing `C(=O)O` with no `N` and no `[O-]`
  (free carboxylic acid), plus `S(=O)(=O)O` with no `[` (free sulfonic acid).
- Result: **0 hits across all 74 entries**.
- Manual scan of full SMILES list confirmed: no TFA (`OC(=O)C(F)(F)F`),
  no AcOH, no p-TsOH, no H₂SO₄ surrogate.
- Conclusion: TFA must be purchased before running the plate.

### Comparison with HTE_Edelris.sdf (kit 1, 72 entries)
- Kit 2 adds MeCN (idx 72) and Water (idx 73) — both absent from kit 1.
- Kit 2 has DCE (idx 68, MW 99.0, SMILES ClCCCl) where kit 1 had DCM (same SMILES, same MW) — effectively the same solvent under a different name.
- Kit 2 row 70: C1COCCO1, MW 88.1 = 1,4-dioxane (confirmed by ring SMILES and MW; kit 1 listed the same entry as DME, which is an error in kit 1's labelling).
- All photocatalysts, Ni sources, and N-ligands are identical between the two kits.
"""

phase2_verification = """
## Verification

### Design arithmetic
- 4 PC × 3 Solvent × 2 Acid = 24 wells = exactly one plate ✓
- Degrees of freedom: 3 + 2 + 1 + 6 + 3 + 2 + 6 = 23 = 24 − 1 ✓
- All main effects estimable; all 2-way interactions estimable; 3-way (6 df) used as error ✓
- No confounding in a full factorial; all contrasts are orthogonal ✓

### Photocatalyst E* coverage
- Row A: E* = −1.51 V > −1.2 V (NHP ester Ep) ← will reduce NHP ester ✓
- Row B: E* = −1.04 V > −1.2 V ← within published working range for 4CzIPN/NHP-Minisci ✓
- Row C: E* = −0.96 V ≈ −1.0 V ← borderline; included deliberately ✓
- Row D: E* = −0.89 V < −1.0 V ← expected to fail or give low conversion; diagnostic role confirmed ✓
- All four PCs absorb at 470 nm (confirmed by literature λ_abs for each complex) ✓

### Acid factor logic
- Odd columns (1, 3, 5) = TFA; even columns (2, 4, 6) = no acid.
- This arrangement ensures the acid main effect is estimable across all 12
  PC × Solvent combinations simultaneously; it is not confounded with any other factor ✓
- TFA confirmed absent from kit; purchase flag is correct ✓

### Dispensing randomisation
- Python `random.seed(7)`, `random.shuffle` over indices 0–23.
- Dispensing sequence recorded in `009_design_definition.py` and confirmed
  in the experiment table (24 unique well IDs, each appearing exactly once) ✓

### Plate map image
- `plate_map_minisci_round1.png` generated at 160 dpi.
- 24 wells rendered (A1–D6), all unique ✓
- Colour encoding: row = PC (4 colours), column-pair hatch = solvent (3 patterns),
  well text gold/blue = acid/no-acid ✓
- Legend covers all four visual encodings; missing-reagent warning highlighted in red ✓
"""

# Append verification sections to existing phase documents
for fname, vsect in [
    ('phase_01_minisci_reagent_inventory.md', phase1_verification),
    ('phase_02_minisci_campaign_design.md',   phase2_verification),
]:
    with open(fname, 'a') as f:
        f.write(vsect)
    print(f"Verification appended to {fname}")
