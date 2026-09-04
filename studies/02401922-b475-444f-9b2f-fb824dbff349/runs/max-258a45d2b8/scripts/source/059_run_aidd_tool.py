
from modulon.governance.toolkit import run_aidd_tool

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

result = run_aidd_tool('easy-md', {
    'protein_file':           f'{wd}/receptor_noh2.pdb',
    'ligand_file':            f'{wd}/ligand_prepared.sdf',
    'md_npt':                 True,
    'md_steps':               10_000_000,   # 20 ns at 2 fs
    'md_save_interval':       50_000,       # frame every 100 ps → 200 frames
    'emin_target_temp':       300,
    'integrator_temperature': 300,
    'integrator_timestep':    0.002,
    'md_pressure':            1.0,
    'solv_ionic_strength':    0.15,
    'solv_pH':                7.4,
    'platform_name':          'CUDA',
    'platform_precision':     'mixed',
    'run_analysis':           True,
}, gpu=True)

import json
# Show outputs dict + key file paths
out = result if isinstance(result, dict) else {}
print("RC:", out.get('rc'))
print("Duration:", out.get('duration_s'), 's')
print("Output:", json.dumps(out.get('output', {}), indent=2))
print("Files written:", out.get('files_written', [])[:30])
