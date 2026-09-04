
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

job_score = dispatch('gnina', {
    'proteinFile': f'{WS}/receptor_prepared.pdb',
    'ligandFile':  f'{WS}/ctx_ref.sdf',
    'boxX': BOX_X, 'boxY': BOX_Y, 'boxZ': BOX_Z,
    'width': BOX_W, 'height': BOX_H, 'depth': BOX_D,
    'scoreOnly': True,
    'cnnScoring': 'rescore',
    'seed': 42
}, gpu=True)

print("Docking job:", job_dock)
print("Scoring job:", job_score)
