
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem, Draw
from rdkit.Chem.Scaffolds import MurckoScaffold
import re, collections

SDF_PATH = "/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf"

actives, inactives = [], []

suppl = Chem.SDMolSupplier(SDF_PATH, removeHs=True, sanitize=True)

def props(mol, sdf_mol):
    name = sdf_mol.GetProp('EDS_Number') if sdf_mol.HasProp('EDS_Number') else ''
    smiles = sdf_mol.GetProp('Smiles') if sdf_mol.HasProp('Smiles') else Chem.MolToSmiles(mol)
    hit = sdf_mol.GetProp('HIT P841') if sdf_mol.HasProp('HIT P841') else ''
    as1 = float(sdf_mol.GetProp('AS ratio')) if sdf_mol.HasProp('AS ratio') else 0
    as2 = float(sdf_mol.GetProp('AS ratio 2')) if sdf_mol.HasProp('AS ratio 2') else 0
    avg_br = float(sdf_mol.GetProp('Avg BR')) if sdf_mol.HasProp('Avg BR') else 0
    hit_rank = int(sdf_mol.GetProp('Hit_rank')) if sdf_mol.HasProp('Hit_rank') else None
    try:
        mw   = Descriptors.ExactMolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd  = rdMolDescriptors.CalcNumHBD(mol)
        hba  = rdMolDescriptors.CalcNumHBA(mol)
        tpsa = Descriptors.TPSA(mol)
        rot  = rdMolDescriptors.CalcNumRotatableBonds(mol)
        arom = rdMolDescriptors.CalcNumAromaticRings(mol)
        hac  = mol.GetNumHeavyAtoms()
    except:
        return None
    return dict(name=name, smiles=smiles, hit=hit, as1=as1, as2=as2,
                avg_br=avg_br, hit_rank=hit_rank,
                mw=mw, logp=logp, hbd=hbd, hba=hba, tpsa=tpsa, rot=rot, arom=arom, hac=hac)

for mol in suppl:
    if mol is None:
        continue
    try:
        sdf_mol = mol  # properties attached to same mol object
        p = props(mol, sdf_mol)
        if p is None:
            continue
        if p['hit'] == 'Active':
            actives.append(p)
        else:
            inactives.append(p)
    except:
        pass

print(f"Actives: {len(actives)}")
print(f"Inactives: {len(inactives)}")
print()
print("=== ACTIVES ===")
for a in actives:
    print(f"  {a['name']}  MW={a['mw']:.1f}  logP={a['logp']:.2f}  HBD={a['hbd']}  HBA={a['hba']}  TPSA={a['tpsa']:.0f}  rot={a['rot']}  HAC={a['hac']}  AS1={a['as1']:.4f}  AS2={a['as2']:.4f}  rank={a['hit_rank']}")
