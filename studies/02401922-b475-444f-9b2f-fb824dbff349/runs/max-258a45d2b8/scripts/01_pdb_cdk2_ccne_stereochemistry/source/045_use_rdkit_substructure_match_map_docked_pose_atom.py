
# Use RDKit substructure match to map docked-pose atom coords → template mol2 atom indices
# Template: ligand_prepared.sdf (correct 3D, same atom order as ligand.mol2)
# Docked:   docked_poses_all5.sdf pose 1

from rdkit.Chem import rdFMCS

suppl_t = Chem.SDMolSupplier('ligand_prepared.sdf', removeHs=False)
suppl_d = Chem.SDMolSupplier('docked_poses_all5.sdf', removeHs=False)
mol_t = list(suppl_t)[0]   # template (SDF → ETKDG coords, same atom order as ligand.mol2)
mol_d = list(suppl_d)[0]   # docked pose 1

print(f"Template: {mol_t.GetNumAtoms()} atoms")
print(f"Docked:   {mol_d.GetNumAtoms()} atoms")

# Find full MCS (should be entire molecule since they're the same)
mcs = rdFMCS.FindMCS(
    [Chem.RemoveHs(mol_t), Chem.RemoveHs(mol_d)],
    atomCompare=rdFMCS.AtomCompare.CompareElements,
    bondCompare=rdFMCS.BondCompare.CompareOrder,
    timeout=30
)
print(f"MCS: {mcs.numAtoms} heavy atoms, {mcs.numBonds} bonds")

patt = Chem.MolFromSmarts(mcs.smartsString)

# Get atom maps: template_idx → docked_idx
t_match = mol_t.GetSubstructMatch(patt)   # template heavy atom indices
d_match = mol_d.GetSubstructMatch(patt)   # docked heavy atom indices
print(f"Template match: {len(t_match)} atoms, Docked match: {len(d_match)} atoms")

# Build full atom map including H (match H by proximity to matched heavy atom)
# For each template atom (incl H), find corresponding docked atom coord
conf_t = mol_t.GetConformer()
conf_d = mol_d.GetConformer()

# t_match[i] = template atom index that corresponds to d_match[i] = docked atom index
t2d_heavy = {t_match[i]: d_match[i] for i in range(len(t_match))}
print(f"Heavy atom map entries: {len(t2d_heavy)}")

# Build coordinate array for template atoms in template-index order, with docked coords
import numpy as np
new_coords = {}
for t_idx, d_idx in t2d_heavy.items():
    pos = conf_d.GetAtomPosition(d_idx)
    new_coords[t_idx] = (pos.x, pos.y, pos.z)

# Handle H atoms: map by attached heavy atom
for atom in mol_t.GetAtoms():
    tidx = atom.GetIdx()
    if tidx in new_coords: continue  # already mapped (heavy atom)
    if atom.GetAtomicNum() == 1:
        # Find the heavy atom this H is attached to
        for bond in atom.GetBonds():
            heavy_t = bond.GetOtherAtomIdx(tidx)
            if heavy_t in t2d_heavy:
                # Find corresponding H in docked mol attached to d_match heavy
                heavy_d = t2d_heavy[heavy_t]
                # Find H neighbors of heavy_d not yet assigned
                d_h_neighbors = [b.GetOtherAtomIdx(heavy_d) for b in mol_d.GetAtomWithIdx(heavy_d).GetBonds()
                                 if mol_d.GetAtomWithIdx(b.GetOtherAtomIdx(heavy_d)).GetAtomicNum() == 1]
                if d_h_neighbors:
                    dh = d_h_neighbors[0]
                    pos = conf_d.GetAtomPosition(dh)
                    new_coords[tidx] = (pos.x, pos.y, pos.z)
                break

print(f"Total mapped atoms: {len(new_coords)} / {mol_t.GetNumAtoms()}")
unmapped = [i for i in range(mol_t.GetNumAtoms()) if i not in new_coords]
print(f"Unmapped: {unmapped}")
