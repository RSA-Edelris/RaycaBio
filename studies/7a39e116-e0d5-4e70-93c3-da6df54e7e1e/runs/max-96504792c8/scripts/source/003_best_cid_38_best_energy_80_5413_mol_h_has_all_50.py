
from rdkit.Chem import SDWriter, RWMol

# best_cid=38, best_energy=-80.5413, mol_h has all 50 conformers
# Build a clean copy retaining only the best conformer
mol_3d = RWMol(Chem.RWMol(mol_h))

# Remove every conformer except the best one
confs_to_remove = [cid for cid in range(mol_h.GetNumConformers()) if cid != best_cid]
for cid in sorted(confs_to_remove, reverse=True):
    mol_3d.RemoveConformer(cid)

# After removal the remaining conformer gets renumbered to 0
print(f"Conformers remaining: {mol_3d.GetNumConformers()}")
print(f"Atom count (with H): {mol_3d.GetNumAtoms()}")

# Copy properties from original mol
for prop_name in mol.GetPropNames():
    mol_3d.SetProp(prop_name, mol.GetProp(prop_name))
mol_3d.SetProp("_Name", "EL2003A-A2U1")
mol_3d.SetProp("MMFF94_energy_kcal_mol", f"{best_energy:.4f}")
mol_3d.SetProp("pIC50 PDK", "7.6")
mol_3d.SetProp("Note", "No stereocenters; single enantiomer (achiral molecule)")

# Write to SDF
out_path = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/ligand_clean_PDK1.sdf"
writer = SDWriter(out_path)
writer.write(mol_3d.GetMol())
writer.close()

print(f"Written: {out_path}")

# Quick verification - re-read and report
check = list(Chem.SDMolSupplier(out_path, removeHs=False))
print(f"Verification: {len(check)} molecule(s) in output SDF")
c = check[0].GetConformer()
coords = c.GetPositions()
print(f"  First atom coords: {coords[0]}")
print(f"  Z-range: {coords[:,2].min():.3f} to {coords[:,2].max():.3f}  (non-zero = true 3D)")
print(f"  Properties: {list(check[0].GetPropNames())}")
