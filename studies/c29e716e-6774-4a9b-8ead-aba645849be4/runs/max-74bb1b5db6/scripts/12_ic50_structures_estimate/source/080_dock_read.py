
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

batch5 = [
    ('C2','O=C(NCC1CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('C3','O=C(NCc1ccncc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('C4','O=C(NCCO)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('D1','O=C(c1ccc2c(n1)CN(C(=O)Cc1ccc(F)cc1)CC2)N1CCCC1c1ccncc1'),
    ('D2','O=C(c1ccc2c(n1)CN(C(=O)Cc1ccc(F)cc1)CC2)N1CCC(c2ccncc2)CC1'),
]
print("=== Batch 5 ===")
for name, smi in batch5:
    if name not in docking_results:
        docking_results[name] = dock_and_read(name, smi)
print(f"Total: {len(docking_results)}")
