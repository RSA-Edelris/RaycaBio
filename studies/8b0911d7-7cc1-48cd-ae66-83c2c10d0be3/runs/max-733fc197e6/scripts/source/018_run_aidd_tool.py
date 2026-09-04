
from modulon.governance.toolkit import run_aidd_tool

result2 = run_aidd_tool('autodock-vina', {
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

print('rc:', result2.get('rc'))
print('staged_files:', result2.get('staged_files'))
print('files_written:', result2.get('files_written'))
print('output_saved_to:', result2.get('output_saved_to'))
print('path_rewrites:', result2.get('path_rewrites'))
print()
# Print full output to find RMSD
out = result2.get('output', '')
if isinstance(out, str):
    print(out[:3000])
elif isinstance(out, dict):
    import json
    print(json.dumps(out, indent=2)[:3000])
