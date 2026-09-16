
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, inchi, rdMolDescriptors
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from rdkit.Chem.MolStandardize import rdMolStandardize

# ---- Parse and standardize all actives ----
normalizer = rdMolStandardize.Normalizer()
lfc = rdMolStandardize.LargestFragmentChooser()
uc = rdMolStandardize.Uncharger()
te = rdMolStandardize.TautomerEnumerator()

def standardize(smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None, None, "parse_fail"
    mol = normalizer.normalize(mol)
    mol = lfc.choose(mol)   # salt strip → keep largest fragment
    mol = uc.uncharge(mol)
    # canonical tautomer
    mol = te.Canonicalize(mol)
    std_smi = Chem.MolToSmiles(mol)
    inchi_key = inchi.MolToInchiKey(mol)
    return mol, std_smi, inchi_key

std_actives = []
for r in actives:
    mol, std_smi, ik = standardize(r['Smiles'])
    r2 = dict(r)
    r2['mol'] = mol
    r2['std_smi'] = std_smi
    r2['inchi_key'] = ik
    r2['parse_ok'] = mol is not None
    std_actives.append(r2)

failed = [r for r in std_actives if not r['parse_ok']]
print(f"Parsed OK: {len(std_actives)-len(failed)}/{len(std_actives)}, Failed: {len(failed)}")

# Also check a sample of inactives
std_inactive_sample = []
for r in inactives[:500]:
    mol, std_smi, ik = standardize(r['Smiles'])
    r2 = dict(r)
    r2['mol'] = mol; r2['std_smi'] = std_smi; r2['inchi_key'] = ik
    r2['parse_ok'] = mol is not None
    std_inactive_sample.append(r2)
# Check for duplicates between actives and inactives (full set)
print("\nChecking duplicate InChIKeys between actives and full inactive set...")
active_iks = set(r['inchi_key'] for r in std_actives if r['inchi_key'])
dup_count = 0
dup_ids = []
for r in inactives:
    mol, std_smi, ik = standardize(r['Smiles'])
    if ik and ik in active_iks:
        dup_count += 1
        dup_ids.append((r['EDS_Number'], ik))
print(f"Active–inactive InChIKey duplicates: {dup_count}")
for d in dup_ids:
    print(f"  {d}")
