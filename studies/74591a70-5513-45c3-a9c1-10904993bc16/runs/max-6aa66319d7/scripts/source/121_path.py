
from pathlib import Path
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

name = "Compound_1_ent1"
rec_content = (BASE / "4CI2_receptor_for_docking.pdb").read_text()
lig_content  = (BASE / "ligs2" / f"{name}.sdf").read_text()

print(f"Receptor: {len(rec_content)} bytes, Ligand: {len(lig_content)} bytes")
print("Dispatching gnina with files={}...")

r = dispatch('gnina',
    {
        'proteinFile': 'receptor.pdb',
        'ligandFile':  'ligand.sdf',
        'boxX': 85.06, 'boxY': 154.79, 'boxZ': 13.38,
        'width': 22.0, 'height': 22.0, 'depth': 22.0,
        'numModes': 5, 'cnnScoring': 'rescore', 'seed': 42
    },
    files={
        'receptor.pdb': rec_content,
        'ligand.sdf':   lig_content,
    }
)

print(f"rc={r.get('rc')}, gpu={r.get('gpu')}, duration={r.get('duration_s'):.1f}s")
if r.get('rc') == 0:
    out = r['output']
    print(f"affinity={out.get('best_affinity_kcal_mol'):.2f}, cnn={out.get('best_cnn_affinity'):.2f}, poses={out.get('num_poses')}")
else:
    print(f"Error: {r.get('output', {}).get('summary', 'unknown')[:300]}")
