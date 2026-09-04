
from modulon.governance.toolkit import run_aidd_tool
import json

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

result = run_aidd_tool('easy-md', {
    'protein_file':           f'{wd}/receptor_ab.pdb',
    'ligand_file':            f'{wd}/ligand_prepared.sdf',
    'md_npt':                 True,
    'md_steps':               250_000,   # 500 ps production
    'md_save_interval':       5_000,     # every 10 ps → 50 frames
    'NVTEquilibrationTime':   0.05,      # 50 ps NVT
    'NPTEquilibrationTime':   0.05,      # 50 ps NPT
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

out = result if isinstance(result, dict) else {}
print("RC:", out.get('rc'))
print("Duration:", out.get('duration_s'), 's')
print("Summary:", str(out.get('output', {}).get('summary', ''))[:600])
print("Error:", str(out.get('output', {}).get('error', ''))[:400])
print("Files:", out.get('files_written', [])[:30])
