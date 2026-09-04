
from modulon.governance.toolkit import run_aidd_tool

result = run_aidd_tool('autodock-vina', {
    'receptorFile': '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/9C56_receptor.pdb',
    'ligandFile': '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/ligands/EDS00760714-1.sdf',
    'ligandFormat': 'sdf',
    'boxX': 28.48,
    'boxY': 12.33,
    'boxZ': 4.22,
    'width': 22,
    'height': 28,
    'depth': 24,
    'num_modes': 5,
    'exhaustiveness': 16
})

print('rc:', result.get('rc'))
print('summary:', result.get('summary'))
print('best_affinity_kcal_mol:', result.get('best_affinity_kcal_mol'))
print('affinities_kcal_mol:', result.get('affinities_kcal_mol'))
print('num_poses:', result.get('num_poses'))
print('poses_pdbqt keys:', list(result.keys()))
