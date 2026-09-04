
import subprocess, time

# Clean up stale gnina container
r = subprocess.run(
    ['docker', 'rm', '-f', 'rayca-norun-gnina-1'],
    capture_output=True, text=True
)
print("docker rm:", r.stdout.strip(), r.stderr.strip())
time.sleep(2)

# Dock ligand (5 poses)
print("Dispatching docking job...")
job_dock = dispatch('gnina', {
    'proteinFile': f'{WS}/receptor_prepared.pdb',
    'ligandFile':  f'{WS}/ligand_prepared.sdf',
    'boxX': BOX_X, 'boxY': BOX_Y, 'boxZ': BOX_Z,
    'width': BOX_W, 'height': BOX_H, 'depth': BOX_D,
    'numModes': 5,
    'exhaustiveness': 16,
    'cnnScoring': 'rescore',
    'seed': 42
}, gpu=True)

print("Dock result:", job_dock.get('summary'))
print("Error:", job_dock.get('error'))
print("Best affinity:", job_dock.get('output', {}).get('best_affinity_kcal_mol') if job_dock.get('output') else None)
