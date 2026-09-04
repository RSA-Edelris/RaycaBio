
# === LIGAND PREPARATION ===
# 1. Load SDF (2D V3000), standardize, resolve tautomers, enumerate stereo
# 2. Generate 3D coordinates
# 3. Protonate at pH 7.4

from rdkit import Chem
from rdkit.Chem import AllChem, Draw, rdMolDescriptors, MolStandardize
from rdkit.Chem.MolStandardize import rdMolStandardize
import subprocess, os

SDF_IN = '/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/Ligand.sdf'

# Load
suppl = Chem.SDMolSupplier(SDF_IN, removeHs=False, sanitize=True)
mols_raw = [m for m in suppl if m is not None]
print(f"Molecules loaded: {len(mols_raw)}")

for i, m in enumerate(mols_raw):
    name = m.GetProp('_Name') if m.HasProp('_Name') else f'mol_{i}'
    print(f"  [{i}] {name}  atoms={m.GetNumAtoms()}  MW={rdMolDescriptors.CalcExactMolWt(m):.2f}")
    print(f"       SMILES: {Chem.MolToSmiles(m)}")
