
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

batch6 = [
    ('E1','O=C(c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2)N1CCC(F)(c2ccncc2)CC1'),
    ('E2','O=C(c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2)N1CCC(O)(c2ccncc2)CC1'),
    ('E3','O=C(c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2)N1CCC(c2ccncc2)(C4(F)CC4)CC1'),  # fixed ring numbering
    ('F1','O=C(N1CCc2ccc(C(=O)NC3CCN(C)CC3)nc2C1)c1ccc(F)cc1'),
    ('F2','O=C(N1CCc2ccc(C(=O)NC3CCN(CC(F)(F)F)CC3)nc2C1)c1ccc(F)cc1'),
]
print("=== Batch 6 ===")
for name, smi in batch6:
    if name not in docking_results:
        docking_results[name] = dock_and_read(name, smi)
print(f"Total: {len(docking_results)}")
