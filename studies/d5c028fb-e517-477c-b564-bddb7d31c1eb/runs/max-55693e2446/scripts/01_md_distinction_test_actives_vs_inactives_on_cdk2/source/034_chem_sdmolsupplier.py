
import os
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdmolops

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
md = f'{wd}/md_prep'

cpd_ids = ['EDS00495858','EDS00480994','EDS00444974','EDS00481054','EDS00441134','EDS00445742']

ATOMIC_NUM = {'H':1,'C':6,'N':7,'O':8,'F':9,'P':15,'S':16,'Cl':17,'Br':35,'I':53}

for cid in cpd_ids:
    # Read pose with H
    m_wH = Chem.SDMolSupplier(f'{md}/{cid}_pose.sdf', removeHs=False)[0]
    # Read without H, re-add cleanly
    m_noH = Chem.SDMolSupplier(f'{md}/{cid}_pose.sdf', removeHs=True)[0]
    m_reH = Chem.AddHs(m_noH)
    AllChem.EmbedMolecule(m_reH, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(m_reH)

    fc = rdmolops.GetFormalCharge(m_reH)
    n_elec = sum(a.GetAtomicNum() for a in m_reH.GetAtoms()) - fc
    n_elec_orig = sum(a.GetAtomicNum() for a in m_wH.GetAtoms()) - fc

    print(f"{cid}: orig_electrons={n_elec_orig} ({'EVEN' if n_elec_orig%2==0 else 'ODD'})  "
          f"reH_electrons={n_elec} ({'EVEN' if n_elec%2==0 else 'ODD'})")

    # Write clean SDF for acpype
    out = f'{md}/{cid}_clean.sdf'
    w = Chem.SDWriter(out)
    w.SetKekulize(False)
    m_reH.SetProp('_Name', cid)
    w.write(m_reH)
    w.close()

print("\nClean SDFs written. Electron counts fixed via re-hydrogenation.")
