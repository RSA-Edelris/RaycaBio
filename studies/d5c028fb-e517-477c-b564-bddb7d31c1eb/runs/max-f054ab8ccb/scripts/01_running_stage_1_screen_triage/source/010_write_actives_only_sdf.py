
from rdkit import Chem
from rdkit.Chem import AllChem

# Write actives-only SDF
actives_mols = [m for m in all_cpds if m.GetProp('type') == 'active']
designed_mols = [m for m in all_cpds if m.GetProp('type') == 'designed']
print(f"Actives: {len(actives_mols)}  Designed: {len(designed_mols)}")

w = Chem.SDWriter('/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/actives_3d.sdf')
for m in actives_mols:
    w.write(m)
w.close()
print("Written actives_3d.sdf")

# Write designed in two batches of ~19
w1 = Chem.SDWriter('/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/designed_batch1.sdf')
w2 = Chem.SDWriter('/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/designed_batch2.sdf')
for i, m in enumerate(designed_mols):
    if i < 19:
        w1.write(m)
    else:
        w2.write(m)
w1.close(); w2.close()
print("Written designed_batch1.sdf (19 cpds)  designed_batch2.sdf (19 cpds)")
