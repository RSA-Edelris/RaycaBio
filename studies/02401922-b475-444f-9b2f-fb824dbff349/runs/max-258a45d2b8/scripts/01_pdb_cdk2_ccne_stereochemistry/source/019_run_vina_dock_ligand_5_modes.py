
import subprocess, json

# Run Vina: dock ligand (5 modes)
vina_cmd = [
    'vina',
    '--receptor', 'receptor.pdbqt',
    '--ligand',   'ligand.pdbqt',
    '--out',      'docked_poses.pdbqt',
    '--center_x', str(BOX_X), '--center_y', str(BOX_Y), '--center_z', str(BOX_Z),
    '--size_x',   str(BOX_W), '--size_y',   str(BOX_H), '--size_z',   str(BOX_D),
    '--num_modes', '5',
    '--exhaustiveness', '16',
    '--energy_range', '5',
    '--seed', '42',
    '--cpu', '4'
]

print("Running Vina docking...")
r_dock = subprocess.run(vina_cmd, capture_output=True, text=True, cwd=WS)
print(r_dock.stdout)
if r_dock.returncode != 0:
    print("STDERR:", r_dock.stderr)
