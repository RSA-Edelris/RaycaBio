
from rdkit.Chem import AllChem
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from rdkit.Chem import rdFingerprintGenerator

# Scaffold
scaffold = Chem.MolFromSmiles('OC(=O)c1ccc2CCNCc2n1')
print("Scaffold valid:", scaffold is not None)
print("Scaffold SMILES:", Chem.MolToSmiles(scaffold))

# Verify the two reactive sites
nh_patt = Chem.MolFromSmarts('[NH1;R]')     # ring secondary NH
cooh_patt = Chem.MolFromSmarts('[C](=O)[OH]')  # carboxylic acid
print(f"NH matches: {len(scaffold.GetSubstructMatches(nh_patt))}")
print(f"COOH matches: {len(scaffold.GetSubstructMatches(cooh_patt))}")

# Define reactions
rxn_n_acyl = AllChem.ReactionFromSmarts('[NH1;R:1].[C:2](=O)[Cl,OH]>>[N:1][C:2]=O')
rxn_n_redAm = AllChem.ReactionFromSmarts('[NH1;R:1].[C;H1:2]=O>>[N:1][CH2:2]')
rxn_cooh_am = AllChem.ReactionFromSmarts('[C:1](=O)[OH].[N;H1,H2:2]>>[C:1](=O)[N:2]')

print("\nReactions valid:", 
      rxn_n_acyl is not None, 
      rxn_n_redAm is not None,
      rxn_cooh_am is not None)

# Test each reaction
test_acyl = Chem.MolFromSmiles('O=C(Cl)C1CCOCC1')
test_ald  = Chem.MolFromSmiles('O=Cc1ccccc1')
test_am   = Chem.MolFromSmiles('CN1CCC(N)CC1')

for rxn, reagent, name in [(rxn_n_acyl, test_acyl, 'N-acylation'),
                            (rxn_n_redAm, test_ald, 'N-RedAm'),
                            (rxn_cooh_am, test_am, 'COOH-amide')]:
    prods = rxn.RunReactants((scaffold, reagent))
    if prods:
        try:
            p = prods[0][0]
            Chem.SanitizeMol(p)
            print(f"{name}: {Chem.MolToSmiles(p)}")
        except Exception as e:
            print(f"{name}: sanitize error {e}")
    else:
        print(f"{name}: no products")
