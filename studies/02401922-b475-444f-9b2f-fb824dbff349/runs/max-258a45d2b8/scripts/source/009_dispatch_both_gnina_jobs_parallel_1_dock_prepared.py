
# Dispatch both gnina jobs in parallel:
# 1. Dock prepared ligand (5 modes, exhaustiveness=16)
# 2. Score CTX in crystal pose (score_only)

WS = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Box from CTX centroid
BOX_X, BOX_Y, BOX_Z = 31.99, 4.68, -26.16
BOX_W = BOX_H = BOX_D = 25.0

job_dock = dispatch('gnina', {
    'proteinFile': f'{WS}/receptor_prepared.pdb',
    'ligandFile':  f'{WS}/ligand_prepared.sdf',
    'boxX': BOX_X, 'boxY': BOX_Y, 'boxZ': BOX_Z,
    'width': BOX_W, 'height': BOX_H, 'depth': BOX_D,
    'numModes': 5,
    'exhaustiveness': 16,
    'cnnScoring': 'rescore',
    'seed': 42
}, gpu=True, label='dock_ligand')

job_score = dispatch('gnina', {
    'proteinFile': f'{WS}/receptor_prepared.pdb',
    'ligandFile':  f'{WS}/ctx_ref.sdf',
    'boxX': BOX_X, 'boxY': BOX_Y, 'boxZ': BOX_Z,
    'width': BOX_W, 'height': BOX_H, 'depth': BOX_D,
    'scoreOnly': True,
    'cnnScoring': 'rescore',
    'seed': 42
}, gpu=True, label='score_ctx_crystal')

print("Docking job:", job_dock)
print("Scoring job:", job_score)
