
import json, glob, os

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
    new = after - before
    rf = list(new)[0] if new else sorted(glob.glob(f'{ws}/autodock-vina-results*.json'), key=os.path.getmtime)[-1]
    with open(rf) as f:
        d = json.load(f)
    aff = d.get('best_affinity_kcal_mol')
    print(f"  {name}: {aff}")
    return aff

# Batch 3: known actives 10-15 + top-priority proposed
batch3 = [(n, s) for n, s, *_ in known_actives[9:]] + [
    ('A1', 'O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2'),
    ('A2', 'O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2'),
]
print("=== Batch 3 ===")
for name, smi in batch3:
    if name not in docking_results:
        aff = dock_and_read(name, smi)
        docking_results[name] = aff
print(f"Total so far: {len(docking_results)}")
