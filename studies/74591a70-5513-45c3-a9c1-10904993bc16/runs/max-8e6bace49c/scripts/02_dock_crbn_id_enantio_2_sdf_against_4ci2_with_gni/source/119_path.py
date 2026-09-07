
import json
from pathlib import Path

BASE     = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
RESULTS  = BASE / "docking2_results.json"

if RESULTS.exists():
    results = json.loads(RESULTS.read_text())
else:
    results = {}

# Test with first compound using /work/ paths
name = "Compound_1_ent1"
print(f"Test docking {name}...")
r = dispatch('gnina', {
    'proteinFile': '/work/4CI2_receptor_for_docking.pdb',
    'ligandFile':  f'/work/ligs2/{name}.sdf',
    'boxX': 85.06, 'boxY': 154.79, 'boxZ': 13.38,
    'width': 22.0, 'height': 22.0, 'depth': 22.0,
    'numModes': 5, 'cnnScoring': 'rescore', 'seed': 42
})
print(f"rc={r.get('rc')}")
print(f"output keys: {list(r.get('output', {}).keys())}")
print(f"stderr snippet: {r.get('stderr', '')[:300]}")
if r.get('rc', 1) == 0:
    out = r['output']
    print(f"affinity={out.get('best_affinity_kcal_mol')}, cnn={out.get('best_cnn_affinity')}, gpu={out.get('gpu_used')}")
