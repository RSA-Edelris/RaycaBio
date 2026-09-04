
import json, os

results_path = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/docking_results.json'

def dock_one(name, smi):
    res = dispatch('autodock-vina', {
        'receptorFile': 'protein.pdb',
        'ligandSmiles': smi,
        'boxX': cx, 'boxY': cy, 'boxZ': cz,
        'width': 25, 'height': 25, 'depth': 25,
        'exhaustiveness': 8, 'num_modes': 3, 'seed': 42
    }, files={'protein.pdb': pdb_clean_content})
    jf = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/autodock-vina-results.json'
    if os.path.exists(jf):
        with open(jf) as f:
            d = json.load(f)
        return {'name': name, 'affinity': d.get('best_affinity_kcal_mol'), 'affinities': d.get('affinities_kcal_mol')}
    return {'name': name, 'affinity': None}

# Load existing results if any
docking_results = {}
if os.path.exists(results_path):
    with open(results_path) as f:
        docking_results = json.load(f)
    print(f"Loaded {len(docking_results)} existing results")

# Batch 1: known actives 1-5 (skip EDS00444974 already done)
batch_1 = [(n, s) for n,s,r in known_actives[:5]]
# Add EDS00444974 manually (already docked)
docking_results['EDS00444974'] = {'name': 'EDS00444974', 'affinity': -9.70, 'affinities': [-9.7, -9.6, -9.3]}

for name, smi in batch_1:
    if name in docking_results:
        print(f"  {name}: cached {docking_results[name]['affinity']}")
        continue
    r = dock_one(name, smi)
    docking_results[name] = r
    print(f"  {name}: {r['affinity']}")

with open(results_path, 'w') as f:
    json.dump(docking_results, f)
print(f"\nSaved {len(docking_results)} results")
