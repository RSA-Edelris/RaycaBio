
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, inchi, rdMolDescriptors
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from collections import Counter

SDF_PATH = '/home/ubuntu/rayca-artifacts/70045e3ed20155a95e1cafc3/files/ASMS.sdf'

# ---- Re-parse raw records ----
records = []
current = {}
current_field = None
in_mol = True
with open(SDF_PATH, 'r', errors='replace') as f:
    for line in f:
        line = line.rstrip('\n')
        if line.startswith('$$$$'):
            records.append(current); current = {}; current_field = None; in_mol = True
        elif line.startswith('>') and '<' in line:
            in_mol = False
            current_field = line.split('<')[1].split('>')[0].strip()
            current[current_field] = ''
        elif not in_mol and current_field:
            if line.strip():
                current[current_field] = (current.get(current_field,'') + line.strip() + ' ').strip()
        elif line.strip() == 'M  END':
            in_mol = False

actives = [r for r in records if r.get('HIT P841') == 'Active']
print(f"Actives: {len(actives)}")

# ---- Standardise ----
normalizer = rdMolStandardize.Normalizer()
lfc        = rdMolStandardize.LargestFragmentChooser()
uc         = rdMolStandardize.Uncharger()
te         = rdMolStandardize.TautomerEnumerator()

def standardize(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None: return None, None, 'parse_fail'
    mol = normalizer.normalize(mol)
    mol = lfc.choose(mol)
    mol = uc.uncharge(mol)
    mol = te.Canonicalize(mol)
    return mol, Chem.MolToSmiles(mol), inchi.MolToInchiKey(mol)

# ---- PAINS / BRENK filters ----
params_p = FilterCatalogParams(); params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B); params_p.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
pains_cat = FilterCatalog(params_p)
params_b = FilterCatalogParams(); params_b.AddCatalog(FilterCatalogParams.FilterCatalogs.BRENK)
brenk_cat = FilterCatalog(params_b)

def physchem(mol):
    return {
        'MW':    round(Descriptors.ExactMolWt(mol),2),
        'cLogP': round(Descriptors.MolLogP(mol),2),
        'HBD':   rdMolDescriptors.CalcNumHBD(mol),
        'HBA':   rdMolDescriptors.CalcNumHBA(mol),
        'TPSA':  round(rdMolDescriptors.CalcTPSA(mol),1),
        'RotBonds': rdMolDescriptors.CalcNumRotatableBonds(mol),
    }

results = []
for r in actives:
    mol, std_smi, ik = standardize(r['Smiles'])
    pc = physchem(mol)
    pains_str = '; '.join(e.GetDescription() for e in pains_cat.GetMatches(mol)) or '-'
    brenk_str = '; '.join(e.GetDescription() for e in brenk_cat.GetMatches(mol)) or '-'
    react_str = '-'  # already audited; no true reactive groups
    r2 = dict(r); r2.update({'mol':mol,'std_smi':std_smi,'inchi_key':ik,'pc':pc,
                              'pains':pains_str,'brenk':brenk_str,'react':react_str})
    results.append(r2)

print(f"Rebuilt results: {len(results)}")
