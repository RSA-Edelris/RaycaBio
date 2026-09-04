
affinities = [-12.61, -12.20, -11.14, -10.66, -10.39]

writer = Chem.SDWriter('docked_poses_all5.sdf')
pose_mols = []

for i, pose in enumerate(poses_list):
    mols = RDKitMolCreate.from_pdbqt_mol(pose)
    rdmol = mols[0]
    if rdmol is not None:
        rdmol.SetProp('_Name', f'CDK2-CCNE_ligand_pose{i+1}')
        rdmol.SetProp('Vina_affinity_kcal_mol', str(affinities[i]))
        writer.write(rdmol)
        pose_mols.append(rdmol)
        print(f"Pose {i+1}: {rdmol.GetNumAtoms()} atoms, {affinities[i]} kcal/mol")

writer.close()
print(f"\nWrote {len(pose_mols)} poses to docked_poses_all5.sdf")

# Also write best pose (pose 1) separately as PDB for PLIP/MM-GBSA
import subprocess
r = subprocess.run(
    ['obabel', 'docked_poses_all5.sdf', '-O', 'best_pose.pdb', '-f', '1', '-l', '1'],
    capture_output=True, text=True, cwd=WS
)
print("Best pose PDB:", r.stderr.strip())
