
import numpy as np
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import rdFingerprintGenerator

# ASMS actives SMILES (from prior analysis)
asms_active_smiles = [
    'O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2',
    'Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)oc2ccccc12',
    'COc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)ccc2ccccc12',
    'CN1CCN(c2ccc(CNC(=O)c3ccc4c(n3)CN(C(=O)c3cc5ccccc5s3)CC4)cc2)CC1',
    'O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ncccc1Cl)CC2',
    'Cc1cc(C(=O)N2CCc3ccc(C(=O)NCc4cccc(N5CCOCC5)n4)nc3C2)nn1C',
    'Cc1cc(C(=O)N2CCc3ccc(C(=O)NCc4c(F)ccc(F)c4Cl)nc3C2)nn1C',
    'Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C(C)C)CC3)cn1',
    'CCOC(=O)N1CCC(NC(=O)c2ccc3c(n2)CN(C(=O)CCCC(=O)Nc2ccccc2)CC3)CC1',
    'Cc1cc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2cc(C)n(C)n2)CC3)c(C(F)(F)F)o1',
    'COc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccccc4)nc3C2)ccc2ccccc12',
    'CC(C)(CNC(=O)c1ccc2c(n1)CN(C(=O)CCCC(=O)Nc1ccccc1)CC2)c1ccncc1',
    'COc1cscc1C(=O)N1CCc2ccc(C(=O)NCC3(c4ccccc4)CCOCC3)nc2C1',
    'COc1ccc(C)cc1C(=O)N1CCc2ccc(C(=O)NCc3ccsc3)nc2C1',
    'COc1ccc(C)cc1C(=O)N1CCc2ccc(C(=O)NCc3cccc(S(C)(=O)=O)c3)nc2C1',
]
asms_mols = [Chem.MolFromSmiles(s) for s in asms_active_smiles if Chem.MolFromSmiles(s)]

# Morgan fingerprint generator (r=2, 1024 bits = ECFP4)
fpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)
asms_fps = [fpgen.GetFingerprint(m) for m in asms_mols]

def max_tanimoto(mol_fp, ref_fps):
    from rdkit.DataStructs import BulkTanimotoSimilarity
    sims = BulkTanimotoSimilarity(mol_fp, ref_fps)
    return max(sims) if sims else 0.0

# PAINS filter
params_pains = FilterCatalogParams()
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A)
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B)
params_pains.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C)
pains_cat = FilterCatalog(params_pains)

# Enumerate final products
def apply_rxn_cooh(n_smi, amine_mol):
    try:
        n_mol = Chem.MolFromSmiles(n_smi)
        if n_mol is None: return None
        prods = rxn_cooh_am.RunReactants((n_mol, amine_mol))
        if not prods: return None
        p = prods[0][0]
        Chem.SanitizeMol(p)
        return Chem.MolToSmiles(p)
    except:
        return None

print("Enumerating products...")
products = []
amines_df = dfs['acid_amine_140']

for n_int in n_intermediates_dedup:
    n_smi = n_int['n_smi']
    for _, am_row in amines_df.iterrows():
        prod_smi = apply_rxn_cooh(n_smi, am_row['Mol'])
        if prod_smi is None:
            continue
        prod_mol = Chem.MolFromSmiles(prod_smi)
        if prod_mol is None:
            continue
        mw  = Descriptors.MolWt(prod_mol)
        lp  = Descriptors.MolLogP(prod_mol)
        hbd = Descriptors.NumHDonors(prod_mol)
        hba = Descriptors.NumHAcceptors(prod_mol)
        rotb = Descriptors.NumRotatableBonds(prod_mol)
        # Drug-like filter
        if mw > 650 or lp > 5.5 or hbd > 3: 
            continue
        # PAINS
        if pains_cat.GetFirstMatch(prod_mol):
            continue
        fp = fpgen.GetFingerprint(prod_mol)
        sim = max_tanimoto(fp, asms_fps)
        products.append({
            'smiles': prod_smi,
            'r1_smi': n_int['r1_smi'],
            'r1_id': n_int['r1_id'],
            'rxn_type': n_int['rxn_type'],
            'r2_smi': am_row['SMILES'],
            'r2_id': am_row.get('Dotmatics_CR',''),
            'MW': round(mw,1), 'LogP': round(lp,2),
            'HBD': hbd, 'HBA': hba, 'RotB': rotb,
            'asms_sim': round(sim,4)
        })

print(f"Products passing drug-like filter + no PAINS: {len(products)}")
