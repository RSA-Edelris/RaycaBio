
import json, os

output = result['output']
print("best_affinity_kcal_mol:", output['best_affinity_kcal_mol'])
print("affinities_kcal_mol:", output['affinities_kcal_mol'])
print("num_poses:", output['num_poses'])
poses_pdbqt = output['poses_pdbqt']
print("poses_pdbqt type:", type(poses_pdbqt).__name__)
if isinstance(poses_pdbqt, str):
    print("poses_pdbqt length:", len(poses_pdbqt))
    first_line = poses_pdbqt.split('\n')[0]
    print("first line:", first_line)
