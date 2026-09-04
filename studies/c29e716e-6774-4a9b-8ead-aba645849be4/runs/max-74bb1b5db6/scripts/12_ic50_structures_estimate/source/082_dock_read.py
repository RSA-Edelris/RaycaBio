
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

batch7 = [
    ('F3','O=C(N1CCc2ccc(C(=O)NC3CCN(Cc4ccccc4)CC3)nc2C1)c1ccc(F)cc1'),
    ('F4','O=C(N1CCc2ccc(C(=O)NC3CCN(C(C)=O)CC3)nc2C1)c1ccc(F)cc1'),
    ('F5','O=C(N1CCc2ccc(C(=O)NC3CCN(S(C)(=O)=O)CC3)nc2C1)c1ccc(F)cc1'),
]
print("=== Batch 7 (final) ===")
for name, smi in batch7:
    if name not in docking_results:
        docking_results[name] = dock_and_read(name, smi)
print(f"Total docked: {len(docking_results)}")
print("All results:", docking_results)
