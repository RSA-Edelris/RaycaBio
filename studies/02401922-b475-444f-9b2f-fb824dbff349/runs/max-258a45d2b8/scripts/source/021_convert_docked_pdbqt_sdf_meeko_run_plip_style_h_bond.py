
# Convert docked PDBQT → SDF (meeko), then run PLIP-style H-bond/contact analysis

from meeko import PDBQTMolecule, RDKitMolCreate

# Parse all 5 poses from docked_poses.pdbqt
with open('docked_poses.pdbqt') as f:
    pdbqt_str_docked = f.read()

pdbqt_mol = PDBQTMolecule(pdbqt_str_docked, is_dlg=False, skip_typing=False)

# Write each pose as SDF
writer = Chem.SDWriter('docked_poses_all5.sdf')
pose_mols = []
for i, pose in enumerate(pdbqt_mol):
    rdmol, failures = RDKitMolCreate.from_pdbqt_mol(pose)
    if rdmol is not None:
        rdmol.SetProp('_Name', f'CDK2-CCNE_ligand_pose{i+1}')
        rdmol.SetProp('Vina_affinity', str([-12.61,-12.20,-11.14,-10.66,-10.39][i]))
        writer.write(rdmol)
        pose_mols.append(rdmol)
        print(f"Pose {i+1}: {rdmol.GetNumAtoms()} atoms, affinity={[-12.61,-12.20,-11.14,-10.66,-10.39][i]} kcal/mol")
    else:
        print(f"Pose {i+1}: conversion failed", failures)
writer.close()
print(f"\nTotal poses written: {len(pose_mols)}")
