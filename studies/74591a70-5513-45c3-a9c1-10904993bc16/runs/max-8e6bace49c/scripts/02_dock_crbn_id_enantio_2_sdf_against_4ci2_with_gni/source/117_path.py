
import json
from pathlib import Path

BASE     = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
LIG_DIR  = BASE / "ligs2"
REC      = str(BASE / "4CI2_receptor_for_docking.pdb")
RESULTS  = BASE / "docking2_results.json"

# LVY binding site centre
CX, CY, CZ = 85.06, 154.79, 13.38
BOX = 22.0

# Load existing results if any
if RESULTS.exists():
    results = json.loads(RESULTS.read_text())
else:
    results = {}

names = ['Compound_1_ent1', 'Compound_1_ent2', 'Compound_4_s1', 'Compound_4_s4',
         'Compound_4_s5', 'Compound_4_s8', 'Compound_4_s9', 'Compound_4_s12']

for name in names:
    if name in results:
        print(f"  {name}: already done, skipping"); continue
    lig = str(LIG_DIR / f"{name}.sdf")
    print(f"  Docking {name}...", flush=True)
    r = dispatch('gnina', {
        'proteinFile': REC, 'ligandFile': lig,
        'boxX': CX, 'boxY': CY, 'boxZ': CZ,
        'width': BOX, 'height': BOX, 'depth': BOX,
        'numModes': 5, 'cnnScoring': 'rescore', 'seed': 42
    })
    if r.get('rc', 1) != 0:
        print(f"    FAILED: {r.get('stderr','')[:200]}")
        results[name] = {'error': r.get('stderr', 'unknown')}
    else:
        out = r.get('output', {})
        results[name] = {
            'affinity': out.get('best_affinity_kcal_mol'),
            'cnn_affinity': out.get('best_cnn_affinity'),
            'cnn_pose_score': out.get('best_cnn_pose_score'),
            'num_poses': out.get('num_poses'),
            'gpu_used': out.get('gpu_used'),
            'output_file': out.get('output_file'),
        }
        print(f"    affinity={results[name]['affinity']:.2f} kcal/mol, "
              f"cnn_pKd={results[name]['cnn_affinity']:.2f}, "
              f"gpu={results[name]['gpu_used']}")
    RESULTS.write_text(json.dumps(results, indent=2))

print(f"\nBatch 1 done. {len(results)} results saved.")
