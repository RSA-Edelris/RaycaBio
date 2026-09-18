
from rdkit import Chem

# Read back the SDF to get names
wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
supp = list(Chem.SDMolSupplier(f'{wd}/ligands_3d.sdf', removeHs=False))
print(f"Total mols in SDF: {len(supp)}")
for i, m in enumerate(supp[:20]):
    if m:
        print(f"  [{i:2d}] name={m.GetProp('_Name')!r:30s}  props={list(m.GetPropsAsDict().keys())}")
