
# Fix: create docked-pose mol2 with correct GAFF2 atom types
# Strategy: extract coords from docked pose, apply to antechamber mol2 via RDKit atom mapping

from rdkit.Chem import rdMolAlign

# Load template mol2 (has GAFF2 types)
mol_template = Chem.MolFromMol2File('ligand.mol2', removeHs=False)
# Load docked pose 1
mol_docked = pose_mols[0]   # already in memory, 73 atoms with H

print(f"Template mol2: {mol_template.GetNumAtoms()} atoms")
print(f"Docked pose 1: {mol_docked.GetNumAtoms()} atoms")

# Both should be same molecule — use MCS to get atom map
from rdkit.Chem import rdFMCS
mcs = rdFMCS.FindMCS([Chem.RemoveHs(mol_template), Chem.RemoveHs(mol_docked)],
                     atomCompare=rdFMCS.AtomCompare.CompareElements,
                     bondCompare=rdFMCS.BondCompare.CompareAny,
                     timeout=30)
print(f"MCS: {mcs.numAtoms} heavy atoms matched out of {Chem.RemoveHs(mol_template).GetNumAtoms()}")

# Align docked pose onto template using MCS atom map
patt = Chem.MolFromSmarts(mcs.smartsString)
tmatch = mol_template.GetSubstructMatch(patt)
dmatch = mol_docked.GetSubstructMatch(patt)
atom_map = list(zip(dmatch, tmatch))

# Create conformer-replaced mol2: copy template but update conformer from docked
from rdkit.Chem import Chem as C2
from rdkit.Geometry import rdGeometry
import copy

mol_out = copy.deepcopy(mol_template)
conf_t = mol_template.GetConformer()
conf_d = mol_docked.GetConformer()

# Build heavy-atom coordinate map
for di, ti in atom_map:
    pt = conf_d.GetAtomPosition(di)
    mol_out.GetConformer().SetAtomPosition(ti, pt)

# Write updated mol2 via obabel (save as SDF first, convert)
Chem.MolToMolFile(mol_out, 'ligand_docked_pose1.sdf')
r = subprocess.run(
    ['obabel', 'ligand_docked_pose1.sdf', '-O', 'ligand_docked_pose1.mol2'],
    capture_output=True, text=True, cwd=WS
)
print("mol2 convert:", r.stderr.strip())

# Also create fixed PDB: rename UNL → LIG
with open('best_pose.pdb') as f:
    pdb_content = f.read()
pdb_fixed = pdb_content.replace('UNL', 'LIG')
with open('best_pose_lig.pdb','w') as f:
    f.write(pdb_fixed)
print("best_pose_lig.pdb written (UNL→LIG)")
