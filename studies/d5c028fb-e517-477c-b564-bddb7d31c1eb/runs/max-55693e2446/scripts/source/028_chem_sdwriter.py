
from rdkit import Chem
from rdkit.Chem import AllChem
import os

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'

# Build 3D SDF for the 3 selected inactives
sel_ina_recs = [(sim, cid, smi, mol) for sim, cid, smi, mol in sim_rows[:3]]

w = Chem.SDWriter(f'{wd}/inactives_for_dock.sdf')
for sim, cid, smi, mol in sel_ina_recs:
    # Add Hs, embed
    mh = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    ok = AllChem.EmbedMolecule(mh, params)
    if ok == -1:
        print(f"  ETKDG failed for {cid}, trying with random coords")
        AllChem.EmbedMolecule(mh, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(mh, maxIters=2000)
    mh.SetProp('_Name', cid)
    mh.SetProp('type', 'inactive')
    w.write(mh)
    print(f"  {cid}: Tanimoto={sim:.3f} — 3D OK")
w.close()

sz = os.path.getsize(f'{wd}/inactives_for_dock.sdf')
print(f"\nWrote inactives_for_dock.sdf ({sz:,} bytes)")
