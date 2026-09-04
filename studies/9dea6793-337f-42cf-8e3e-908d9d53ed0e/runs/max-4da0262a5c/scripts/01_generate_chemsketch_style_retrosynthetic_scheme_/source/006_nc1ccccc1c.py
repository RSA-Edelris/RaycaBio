
from rdkit import Chem

test_smi = {
    'oPDA': 'Nc1ccccc1N',
    'benzalacetone': 'CC(=O)/C=C/c1ccccc1',
    'phenyl_1_3_diketone': 'CC(=O)CC(=O)c1ccccc1',
    'anthranilic_acid': 'Nc1ccccc1C(=O)O',
    'isatoic_anhydride': 'O=c1[nH]c2ccccc2oc1=O',
    'L_alanine': 'C[C@@H](N)C(=O)O',
    'L_tryptophan': 'N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O',
    '1_indanone': 'O=C1CCc2ccccc21',
    'indane_1_2_dione': 'O=C1C(=O)c2ccccc21',
    'isoindolinone': 'O=C1CNc2ccccc21',
    'phthalimide': 'O=C1c2ccccc2C(=O)N1',
    'tyramine': 'NCCc1ccc(O)cc1',
    'dichloropurine': 'Clc1nc(Cl)c2[nH]cnc2n1',
    'histamine': 'NCCc1c[nH]cn1',
    '4_CF3_aniline_diamine': 'Nc1ccc(C(F)(F)F)cc1N',
    'pyrrolidine': 'C1CCNC1',
    'pomalidomide': 'O=C1CCC(N2C(=O)c3cc(N)ccc3C2=O)C(=O)N1',
    'GlcNAc_allyl': 'C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O',
    'Glc_SEt': 'SCC1OC(CO)C(O)C(O)C1O',
    'L_fucose': 'OC1OC(C)C(O)C(O)C1O',
    'BDZ_dihydro_int': 'C1CN=C(c2ccccc2)CNc2ccccc21',
    'isoquinolinone': 'O=c1cc(-c2ccccc2OC)[nH]c2ccccc12',
    'N_acyl_piperidone': 'O=C1CCN(C(=O)c2ccccc2OC)CC1',
    'glutarimide_amine': 'O=C1CCC(N)C(=O)N1',
    'isoindolinone_core': 'O=C1CNc2ccccc21',
    'Boc_piperazine': 'O=C(OC(C)(C)C)N1CCNCC1',
    '2_MeO_benzoyl_Cl': 'COc1ccccc1C(=O)Cl',
    'benzaldehyde': 'O=Cc1ccccc1',
    'o_HOBn_amine': 'NCc1cccc(O)c1',
    'chloro_isoquinoline': 'Clc1nc(-c2ccccc2OC)cc2ccccc12',
    'proline': 'OC(=O)C1CCCN1',
    'piperazine': 'C1CNCCN1',
    'spiro_azetidine_int': 'O=C1NC2(CC2)C(=O)O1',
    'Boc_4_Me_piperidinone': 'O=C1(C)CCN(C(=O)OC(C)(C)C)CC1',
    'CHO_tyramine': 'NCCc1ccc(O)cc1',
    'phenylacetaldehyde': 'O=CCc1ccccc1',
    'indanone_2': 'O=C1Cc2ccccc21',
    'aminoindanol': 'OC1Cc2ccccc21',
    'Cbz_amino_aldehyde': 'O=CC(N)CC(=O)OCC',
    'isatoic': 'O=C1OC(=O)c2ccccc2N1',
    'NHMe_pyrrolidine': 'CNCC1CCCC1',
    'diamine_CF3': 'Nc1ccc(C(F)(F)F)cc1',
}

ok, fail = [], []
for name, smi in test_smi.items():
    mol = Chem.MolFromSmiles(smi)
    if mol: ok.append(name)
    else: fail.append((name, smi))

print(f"Valid: {len(ok)}/{len(test_smi)}")
if fail:
    print("FAILED SMILES:")
    for n, s in fail:
        print(f"  {n}: {s}")
