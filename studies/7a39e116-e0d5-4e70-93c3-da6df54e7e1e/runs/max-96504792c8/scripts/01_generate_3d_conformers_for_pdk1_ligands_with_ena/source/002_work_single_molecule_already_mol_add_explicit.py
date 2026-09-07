
from rdkit.Chem import AllChem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
import os

# Work with the single molecule already in 'mol'
# Add explicit hydrogens before 3D generation
mol_h = Chem.AddHs(mol)

# Set the name from the SDF property
mol_name = "EL2003A-A2U1"
mol_h.SetProp("_Name", mol_name)

# Generate multiple conformers and keep the lowest-energy one
params = AllChem.ETKDGv3()
params.randomSeed = 42
params.numThreads = 4

n_confs = 50
AllChem.EmbedMultipleConfs(mol_h, numConfs=n_confs, params=params)
print(f"Generated {mol_h.GetNumConformers()} conformers")

# Minimize all conformers with MMFF94 and collect energies
ff_props = AllChem.MMFFGetMoleculeProperties(mol_h, mmffVariant='MMFF94')
energies = []
for cid in range(mol_h.GetNumConformers()):
    ff = AllChem.MMFFGetMoleculeForceField(mol_h, ff_props, confId=cid)
    if ff is None:
        energies.append((float('inf'), cid))
        continue
    ff.Minimize(maxIts=2000)
    e = ff.CalcEnergy()
    energies.append((e, cid))

energies.sort()
best_cid = energies[0][1]
best_energy = energies[0][0]
print(f"Best conformer: id={best_cid}, MMFF94 energy={best_energy:.4f} kcal/mol")

# Keep only the best conformer
from rdkit.Chem import Chem as _C
best_conf = mol_h.GetConformer(best_cid)

# Create a clean molecule with only the best conformer
mol_3d = Chem.RWMol(mol_h)
# Remove all conformers except the best
for cid in reversed(range(mol_h.GetNumConformers())):
    if cid != best_cid:
        mol_3d.RemoveConformer(cid)

print(f"Final molecule has {mol_3d.GetNumConformers()} conformer(s)")
print(f"Atoms (with H): {mol_3d.GetNumAtoms()}")
