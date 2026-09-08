
import sys, importlib.util, warnings
warnings.filterwarnings('ignore')
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors, Crippen

# ── Reload fixed adme_models ──────────────────────────────────────────────────
if "adme_models" in sys.modules:
    del sys.modules["adme_models"]
spec = importlib.util.spec_from_file_location(
    "adme_models",
    "/home/ubuntu/rayca-sessions/2e509818-0885-4168-a643-391abced7c93-8c1a5f76c087/adme_models.py")
adme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adme)
sys.modules["adme_models"] = adme

# ── Rebuild amine + reaction ───────────────────────────────────────────────────
amine = Chem.MolFromMolFile(
    '/home/ubuntu/rayca-artifacts/8c1a5f76c0879e6c03b61ed2/files/amine.mol',
    removeHs=True)
rxn = AllChem.ReactionFromSmarts(
    '[NH1;!$(N-C=O);!$(N-S=O);!a:1].[C:2](=O)[OH]>>[N:1][C:2]=O')

supplier = Chem.SDMolSupplier(
    '/home/ubuntu/rayca-artifacts/8c1a5f76c0879e6c03b61ed2/files/acid.sdf',
    removeHs=True)
products = []
for mol in supplier:
    if mol is None: continue
    name = ''
    for prop in ['Dotmatics_CR','Article','CAS','_Name']:
        if mol.HasProp(prop):
            v = mol.GetProp(prop).strip()
            if v: name = v; break
    cr_id = mol.GetProp('Dotmatics_CR') if mol.HasProp('Dotmatics_CR') else name
    try:
        prods = rxn.RunReactants((amine, mol))
        if prods:
            prod = prods[0][0]
            Chem.SanitizeMol(prod)
            products.append({'mol': prod, 'smiles': Chem.MolToSmiles(prod),
                             'acid_name': name, 'cr_id': cr_id})
    except: pass

print(f"Products rebuilt: {len(products)}")

# ── Verify fix ────────────────────────────────────────────────────────────────
d0 = adme.compute_base_descriptors(products[0]['mol'])
print(f"n_basic_n first product: {d0['n_basic_n']}  (expected 0 for pure amide scaffold)")

# ── Re-score ──────────────────────────────────────────────────────────────────
rows_fixed = []
errors = []
for p in products:
    mol = p['mol']
    try:
        d    = adme.compute_base_descriptors(mol)
        sol  = adme.pred_solubility(d)
        pam  = adme.pred_pampa(d)
        met  = adme.pred_met_stability(mol, d)
        cyp  = adme.pred_cyp(mol, d)
        ppb  = adme.pred_ppb(d)
        herg = adme.pred_herg(mol, d)
        row  = dict(cr_id=p['cr_id'], acid_name=p['acid_name'],
                    smiles=p['smiles'], mol=mol)
        row.update(d)
        row.update({f"sol_{k}":  v for k,v in sol.items()})
        row.update({f"pampa_{k}": v for k,v in pam.items()})
        row.update({f"met_{k}":  v for k,v in met.items()})
        row.update({f"cyp_{k}":  v for k,v in cyp.items()})
        row.update({f"ppb_{k}":  v for k,v in ppb.items()})
        row.update({f"herg_{k}": v for k,v in herg.items()})
        rows_fixed.append(row)
    except Exception as e:
        errors.append((p['cr_id'], str(e)))

assert len(rows_fixed) == len(products), \
    f"Count mismatch: {len(rows_fixed)} rows vs {len(products)} products"
print(f"\nScored: {len(rows_fixed)}, errors: {len(errors)}")

from collections import Counter
print("hERG after fix:", dict(Counter(r['herg_herg_risk'] for r in rows_fixed)))
print("ClearRoute:", dict(Counter(r['met_clearance_route'] for r in rows_fixed)))
