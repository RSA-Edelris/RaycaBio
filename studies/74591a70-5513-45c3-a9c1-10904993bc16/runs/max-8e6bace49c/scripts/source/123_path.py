
import json, gzip
from pathlib import Path

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
RESULTS   = BASE / "docking2_results.json"
POSES_DIR = BASE / "best_poses2"

results     = json.loads(RESULTS.read_text())
rec_content = (BASE / "4CI2_receptor_for_docking.pdb").read_text()

BATCH2 = [
    'Compound_4_s13','Compound_4_s16',
    'Compound_7_ent1','Compound_7_ent2',
    'Compound_8_ent1','Compound_8_ent2',
    'Compound_9_ent1','Compound_9_ent2',
    'Compound_10_ent1','Compound_10_ent2',
    'Compound_11_ent1','Compound_11_ent2',
    'Compound_12_ent1','Compound_12_ent2',
]

for name in BATCH2:
    if name in results and results[name].get('affinity') is not None:
        print(f"  {name}: skip ({results[name]['affinity']:.2f})")
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
        gz = BASE / "gnina_docked.sdf.gz"
        if gz.exists():
            with gzip.open(gz, 'rb') as f:
                sdf_content = f.read().decode('utf-8', errors='replace')
            (POSES_DIR / f"{name}_poses.sdf").write_text(sdf_content)
        print(f"    OK: {results[name]['affinity']:.2f} kcal/mol, cnn={results[name]['cnn_affinity']:.2f}")
    else:
        results[name] = {'error': r.get('output',{}).get('summary','failed')}
        print(f"    FAILED: {results[name]['error'][:100]}")
    RESULTS.write_text(json.dumps(results, indent=2))

done  = sum(1 for v in results.values() if v.get('affinity') is not None)
failed = sum(1 for v in results.values() if 'error' in v)
print(f"\nAll batches done: {done} succeeded, {failed} failed / 22 total")
