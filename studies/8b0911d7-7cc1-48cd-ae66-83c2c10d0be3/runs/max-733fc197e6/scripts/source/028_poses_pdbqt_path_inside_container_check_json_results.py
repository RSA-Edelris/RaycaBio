
# poses_pdbqt is a path inside container - check the JSON results file for full content
import json, os

results_file = os.path.join(WORKDIR, 'autodock-vina-results-4.json')
print("Results file exists:", os.path.exists(results_file))

with open(results_file) as f:
    saved = json.load(f)

print("Saved keys:", list(saved.keys()))
print("best_affinity:", saved.get('best_affinity_kcal_mol'))
print("affinities:", saved.get('affinities_kcal_mol'))
print("num_poses:", saved.get('num_poses'))
pdbqt_val = saved.get('poses_pdbqt', '')
print("poses_pdbqt type:", type(pdbqt_val).__name__, "len:", len(str(pdbqt_val)))
print("poses_pdbqt first 200 chars:", str(pdbqt_val)[:200])
