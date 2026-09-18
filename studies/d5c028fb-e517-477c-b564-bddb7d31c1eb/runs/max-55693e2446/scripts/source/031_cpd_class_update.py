
import os
from rdkit import Chem
from rdkit.Chem import AllChem, rdmolops

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
md = f'{wd}/md_prep'

cpd_ids = ['EDS00495858','EDS00480994','EDS00444974','EDS00481054','EDS00441134','EDS00445742']
cpd_class = {c:'active' for c in cpd_ids[:3]}
cpd_class.update({c:'inactive' for c in cpd_ids[3:]})

charges = {}
smiles_map = {}
for cid in cpd_ids:
    m = Chem.SDMolSupplier(f'{md}/{cid}_pose.sdf', removeHs=True)[0]
    # Formal charge
    fc = rdmolops.GetFormalCharge(m)
    charges[cid] = fc
    smiles_map[cid] = Chem.MolToSmiles(m)
    print(f"{cid} ({cpd_class[cid]}): formal_charge={fc}  SMILES={smiles_map[cid][:80]}")

print("\nAll charges:", charges)
