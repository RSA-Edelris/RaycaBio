
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
    with open(rf) as f: d = json.load(f)
    aff = d.get('best_affinity_kcal_mol')
    print(f"  {name}: {aff}")
    return aff

batch4 = [
    ('A3','O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2'),
    ('B1','Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12'),
    ('B2','Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12'),
    ('B3','Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12'),
    ('C1','O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
]
print("=== Batch 4 ===")
for name, smi in batch4:
    if name not in docking_results:
        docking_results[name] = dock_and_read(name, smi)
print(f"Total: {len(docking_results)}")
