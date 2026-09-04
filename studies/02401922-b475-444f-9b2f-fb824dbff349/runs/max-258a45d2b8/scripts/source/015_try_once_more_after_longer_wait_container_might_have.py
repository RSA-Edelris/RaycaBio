
# Try once more after a longer wait - the container might have a timeout
import time
print("Waiting 15s for sandbox container cleanup...")
time.sleep(15)

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

print(job_dock.get('summary'))
print("error:", job_dock.get('error'))
if job_dock.get('output'):
    print("best_affinity:", job_dock['output'].get('best_affinity_kcal_mol'))
    print("num_poses:", job_dock['output'].get('num_poses'))
    print("gpu_used:", job_dock['output'].get('gpu_used'))
