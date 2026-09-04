
import json, glob, os, re

ws = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02'

def dock_and_read(name, smi):
    before = set(glob.glob(f'{ws}/autodock-vina-results*.json'))
    dispatch('autodock-vina', {
        'receptorFile': 'protein.pdb', 'ligandSmiles': smi,
        'boxX': cx, 'boxY': cy, 'boxZ': cz,
        'width': 25, 'height': 25, 'depth': 25,
        'exhaustiveness': 8, 'num_modes': 3, 'seed': 42
    }, files={'protein.pdb': pdb_clean_content})
    after = set(glob.glob(f'{ws}/autodock-vina-results*.json'))
    new_files = after - before
    if new_files:
        nf = list(new_files)[0]
        with open(nf) as f:
            d = json.load(f)
        aff = d.get('best_affinity_kcal_mol')
        print(f"  {name}: {aff}")
        return aff
    # fallback: newest file
    all_f = sorted(glob.glob(f'{ws}/autodock-vina-results*.json'), key=os.path.getmtime)
    with open(all_f[-1]) as f:
        d = json.load(f)
    aff = d.get('best_affinity_kcal_mol')
    print(f"  {name}: {aff} (fallback)")
    return aff

# Batch 2: remaining known actives 6-10
batch2 = [(n, s) for n, s, *_ in known_actives[5:10]]
print("=== Batch 2 (known actives 6-10) ===")
for name, smi in batch2:
    if name not in docking_results:
        aff = dock_and_read(name, smi)
        docking_results[name] = aff
