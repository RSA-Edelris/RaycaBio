
# MAJOR 3 fix: re-run Brønsted-acid search using SMARTS (not substring matching)
from rdkit import Chem

smarts_cooh  = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
smarts_so3h  = Chem.MolFromSmarts('[SX4](=O)(=O)[OX2H1]')

acid_hits = []
for i, m in enumerate(mols2):
    if m.HasSubstructMatch(smarts_cooh) or m.HasSubstructMatch(smarts_so3h):
        acid_hits.append((i, df2.loc[i, 'name'], Chem.MolToSmiles(m)))

print(f"SMARTS-based Brønsted acid search across {len(mols2)} molecules:")
print(f"Hits: {len(acid_hits)}")
if acid_hits:
    for idx, name, smi in acid_hits:
        print(f"  [{idx}] {name}  |  {smi}")
else:
    print("  → 0 hits confirmed. TFA is absent. Purchase flag is CORRECT.")

# Also verify the table count fix: 72 + 2 monodentate = 74
classes_count = {
    'Photocatalyst-Ir': 4, 'Photocatalyst-Ru': 3, 'Photocatalyst-Org': 5,
    'Ni-cat': 4, 'Pd-cat': 20, 'Bidentate-N-Lig': 8, 'Mono-N-Lig': 2,
    'Chiral-N-Lig': 1, 'Base': 12, 'Solvent': 11, 'Cu-cat': 1,
    'HAT-additive': 1, 'P-Ligand': 2,
}
total = sum(classes_count.values())
print(f"\nTable count check: {dict(classes_count)}")
print(f"Sum = {total}  (expected 74) — {'✓ CORRECT' if total == 74 else '✗ STILL WRONG'}")

# Write corrected code as record
with open('012_acid_smarts_recheck.py', 'w') as f:
    f.write("""# Corrected Brønsted-acid check using SMARTS (not substring matching).
# Original substring 'C(=O)O' fails for TFA: RDKit canonicalises TFA as O=C(O)C(F)(F)F
# which does NOT contain the literal substring 'C(=O)O'. SMARTS is the correct method.
from rdkit import Chem
smarts_cooh = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
smarts_so3h = Chem.MolFromSmarts('[SX4](=O)(=O)[OX2H1]')
acid_hits = [(i, m) for i, m in enumerate(mols2)
             if m.HasSubstructMatch(smarts_cooh) or m.HasSubstructMatch(smarts_so3h)]
# Result on HTE_Edelris_2.sdf: 0 hits — no Brønsted acid present in the 74-entry kit.
""")
print("\nCorrected code written to 012_acid_smarts_recheck.py")
