
import os, copy
from rdkit import Chem
from rdkit.Chem import AllChem, rdmolops, rdForceFieldHelpers
from rdkit.Chem import rdMolTransforms
from rdkit.Geometry import rdGeometry

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'
md = f'{wd}/md_prep'
cpd_ids = ['EDS00495858','EDS00480994','EDS00444974','EDS00481054','EDS00441134','EDS00445742']

for cid in cpd_ids:
    # Load docked pose, strip all explicit H
    m_heavy = Chem.SDMolSupplier(f'{md}/{cid}_pose.sdf', removeHs=True, sanitize=True)[0]
    
    # Add H with correct valence (no 3D yet for H)
    m_wH = Chem.AddHs(m_heavy, addCoords=False)
    
    # Embed only the H atoms — keep heavy atoms at their docked positions
    AllChem.EmbedMolecule(m_wH, AllChem.ETKDGv3())
    
    # Copy docked heavy-atom coordinates back
    conf_new = m_wH.GetConformer()
    conf_heavy = m_heavy.GetConformer()
    # Map heavy atom indices
    ha_idx = [a.GetIdx() for a in m_wH.GetAtoms() if a.GetAtomicNum() != 1]
    for i, hi in enumerate(ha_idx):
        pos = conf_heavy.GetAtomPosition(i)
        conf_new.SetAtomPosition(hi, pos)
    
    # Minimize only H positions (fix heavy atoms via constraints)
    ff = AllChem.MMFFGetMoleculeForceField(m_wH, AllChem.MMFFGetMoleculeProperties(m_wH))
    if ff:
        for hi in ha_idx:
            ff.MMFFAddPositionConstraint(hi, 0.0, 1e4)  # very stiff = fixed
        ff.Minimize(maxIts=500)
    
    # Verify electron count
    fc = rdmolops.GetFormalCharge(m_wH)
    n_e = sum(a.GetAtomicNum() for a in m_wH.GetAtoms()) - fc
    
    # Write
    out = f'{md}/{cid}_fixed.sdf'
    w = Chem.SDWriter(out)
    m_wH.SetProp('_Name', cid)
    w.write(m_wH)
    w.close()
    print(f"{cid}: {m_wH.GetNumAtoms()} atoms  charge={fc}  electrons={n_e} ({'EVEN' if n_e%2==0 else 'ODD'})  -> {cid}_fixed.sdf")

print("\nAll fixed SDFs written with docked heavy-atom coords + clean H positions")
