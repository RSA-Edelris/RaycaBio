
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, FilterCatalog
import pandas as pd

wd = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d'

# Re-read the full ligand SDF to get SMILES and metadata
supp = list(Chem.SDMolSupplier(f'{wd}/ligands_3d.sdf', removeHs=False))
mol_dict = {}
for m in supp:
    if m:
        name = m.GetProp('_Name')
        mol_dict[name] = m

# PAINS catalog
params = FilterCatalog.FilterCatalogParams()
params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.PAINS)
pains_catalog = FilterCatalog.FilterCatalog(params)

def adme_props(mol):
    mw   = Descriptors.ExactMolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd  = rdMolDescriptors.CalcNumHBD(mol)
    hba  = rdMolDescriptors.CalcNumHBA(mol)
    tpsa = Descriptors.TPSA(mol)
    rotb = rdMolDescriptors.CalcNumRotatableBonds(mol)
    pains= pains_catalog.HasMatch(mol)
    ro5_viol = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
    return dict(mw=round(mw,1), logp=round(logp,2), hbd=hbd, hba=hba,
                tpsa=round(tpsa,1), rotb=rotb, pains=pains, ro5_viol=ro5_viol)

rows = []
for name, mol in mol_dict.items():
    p = adme_props(mol)
    p['name'] = name
    p['cpd_type'] = mol.GetProp('type')
    if mol.HasProp('AS_ratio'):
        p['as_ratio'] = float(mol.GetProp('AS_ratio'))
    else:
        p['as_ratio'] = None
    rows.append(p)

adme_df = pd.DataFrame(rows)

# ADME pass criteria: no RO5 violations, TPSA ≤140, rotb ≤10, no PAINS
adme_df['adme_pass'] = (adme_df.ro5_viol == 0) & (adme_df.tpsa <= 140) & \
                       (adme_df.rotb <= 10)   & (~adme_df.pains)

# Summarise designed vs actives
des = adme_df[adme_df.cpd_type == 'designed'].copy()
act = adme_df[adme_df.cpd_type == 'active'].copy()
print(f"Designed: {len(des)} total | {des.adme_pass.sum()} pass ADME")
print(f"Actives:  {len(act)} total | {act.adme_pass.sum()} pass ADME\n")

# Show failures
fail_des = des[~des.adme_pass][['name','mw','logp','hbd','hba','tpsa','rotb','pains','ro5_viol']]
print("Designed ADME failures:")
print(fail_des.to_string(index=False))
