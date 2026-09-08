
from rdkit import Chem

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
supp = list(Chem.SDMolSupplier(f'{wd}/ligands_3d.sdf', removeHs=False))

actives_batch  = [m for m in supp if m and m.GetProp('type') == 'active']
designed_batch = [m for m in supp if m and m.GetProp('type') == 'designed']
print(f"Actives: {len(actives_batch)}, Designed: {len(designed_batch)}")

def write_sdf(mols, path):
    w = Chem.SDWriter(path)
    for m in mols:
        w.write(m)
    w.close()
    print(f"  wrote {len(mols)} mols → {path.split('/')[-1]}")

write_sdf(actives_batch,         f'{wd}/batch_actives.sdf')
write_sdf(designed_batch[:19],   f'{wd}/batch_des1.sdf')
write_sdf(designed_batch[19:],   f'{wd}/batch_des2.sdf')
