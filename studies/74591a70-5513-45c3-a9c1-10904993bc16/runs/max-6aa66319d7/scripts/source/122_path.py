
import json, shutil, gzip
from pathlib import Path

BASE     = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
RESULTS  = BASE / "docking2_results.json"
POSES_DIR = BASE / "best_poses2"
POSES_DIR.mkdir(exist_ok=True)

# Load existing results
results = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}

# Read receptor once
rec_content = (BASE / "4CI2_receptor_for_docking.pdb").read_text()

ALL_NAMES = [
    'Compound_1_ent1','Compound_1_ent2',
    'Compound_4_s1','Compound_4_s4','Compound_4_s5','Compound_4_s8',
    'Compound_4_s9','Compound_4_s12',
]

for name in ALL_NAMES:
    if name in results and results[name].get('affinity') is not None:
        print(f"  {name}: already done ({results[name]['affinity']:.2f}), skip")
        continue
    lig = (BASE / "ligs2" / f"{name}.sdf").read_text()
    print(f"  Docking {name}...", flush=True)
    r = dispatch('gnina',
        {'proteinFile':'receptor.pdb','ligandFile':'ligand.sdf',
         'boxX':85.06,'boxY':154.79,'boxZ':13.38,
         'width':22.0,'height':22.0,'depth':22.0,
         'numModes':5,'cnnScoring':'rescore','seed':42},
        files={'receptor.pdb': rec_content, 'ligand.sdf': lig}
    )
    if r.get('rc') == 0:
        out = r['output']
        results[name] = {
            'affinity': out.get('best_affinity_kcal_mol'),
            'cnn_affinity': out.get('best_cnn_affinity'),
            'cnn_pose_score': out.get('best_cnn_pose_score'),
            'num_poses': out.get('num_poses'),
            'poses': out.get('poses', []),
        }
        # Save pose SDF
        gz = BASE / "gnina_docked.sdf.gz"
        if gz.exists():
            with gzip.open(gz, 'rb') as f:
                sdf_content = f.read().decode('utf-8', errors='replace')
            (POSES_DIR / f"{name}_poses.sdf").write_text(sdf_content)
        print(f"    OK: affinity={results[name]['affinity']:.2f}, cnn={results[name]['cnn_affinity']:.2f}")
    else:
        results[name] = {'error': r.get('output',{}).get('summary','failed')}
        print(f"    FAILED: {results[name]['error'][:100]}")
    RESULTS.write_text(json.dumps(results, indent=2))

done = sum(1 for v in results.values() if v.get('affinity') is not None)
print(f"\nBatch 1 complete: {done}/22 compounds docked")
