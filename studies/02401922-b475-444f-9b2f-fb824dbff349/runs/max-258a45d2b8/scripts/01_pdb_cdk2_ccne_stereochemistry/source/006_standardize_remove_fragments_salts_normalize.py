
# Standardize: remove fragments/salts, normalize, canonical tautomer
# Then enumerate stereocenters, generate 3D, protonate pH 7.4

from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import rdMolDescriptors, EnumerateStereoisomers

mol = mols_raw[0]

# --- 1. Standardize ---
normalizer   = rdMolStandardize.Normalizer()
uncharger    = rdMolStandardize.Uncharger()
largest_frag = rdMolStandardize.LargestFragmentChooser()
te           = rdMolStandardize.TautomerEnumerator()

mol = Chem.RWMol(mol)
mol = normalizer.normalize(mol)
mol = largest_frag.choose(mol)   # remove any counter-ions/salts
mol = Chem.RemoveHs(mol)

# Canonical tautomer
mol_tauto = te.Canonicalize(mol)
print(f"Canonical tautomer SMILES: {Chem.MolToSmiles(mol_tauto)}")

# --- 2. Stereocenters ---
si = rdMolDescriptors.CalcNumAtomStereoCenters(mol_tauto)
ui = rdMolDescriptors.CalcNumUnspecifiedAtomStereoCenters(mol_tauto)
print(f"Stereocenters: {si} total, {ui} unspecified")

# Enumerate if unspecified
if ui > 0:
    opts = EnumerateStereoisomers.StereoEnumerationOptions(unique=True, onlyUnassigned=True)
    isomers = list(EnumerateStereoisomers.EnumerateStereoisomers(mol_tauto, options=opts))
    print(f"  → {len(isomers)} stereoisomers to dock")
else:
    isomers = [mol_tauto]
    print("  → stereochemistry fully defined")

print(f"Proceeding with {len(isomers)} ligand(s)")
