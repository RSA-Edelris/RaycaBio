
from rdkit import Chem

test = {
    'mcuf_acid':     'O=C(O)[C@H]1CCCNC1',
    'mcuf_amine':    'Nc1cc2cc(F)cc(F)c2[nH]1',
    'mcuf_int':      'O=C([C@H]1CCCNC1)Nc1cc2cc(F)cc(F)c2[nH]1',
    'mcuf_target':   'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1',
    'a317_acetylpyr':'CC(=O)[C@@H]1CCCN1',
    'a317_ketoN':    'CC(=O)[C@@H]1CCCN1c1ccccn1',
    'a317_brketo':   'O=C(CBr)[C@@H]1CCCN1c1ccccn1',
    'a317_thiaz':    'Nc1nc([C@@H]2CCCN2c2ccccn2)cs1',
    'a317_pyrracid': 'O=C(O)c1cccn1Cc1ccncc1',
    'a317_target':   'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1',
    '7977_nitropyr': 'O=[N+]([O-])c1cnccc1Br',
    '7977_aminopyr': 'Cc1cnc(Br)cc1N',
    '7977_diamine':  'Cc1cnc(Br)cc1Nc1cnccc1',
    '7977_imidazo':  'O=c1[nH]c2cnccc2n1CC(N)=O',
    '7977_target':   'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21',
    '7977_boron':    'OB(O)c1cc(Cl)ccc1F',
    '7877_brohypy':  'Oc1ncccc1Br',
    '7877_alkyne':   'BrCC#Cc1ccc(C(=O)OC)c(C2CCCC2)c1',
    '7877_oproparg': 'OCC#Cc1ccc(C(=O)OC)c(C2CCCC2)c1',
    '7877_furopyr':  'COC(=O)c1ccc(-c2coc3ncccc23)cc1C1CCCC1',
    '7877_target':   'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1',
    'b54_methanol':  'OCc1cn(C2CCCCC2)cn1',
    'b54_aldehyde':  'O=Cc1cn(C2CCCCC2)cn1',
    'b54_enone':     'CC(=O)C=Cc1cn(C2CCCCC2)cn1',
    'b54_brenone':   'O=C(CBr)C=Cc1cn(C2CCCCC2)cn1',
    'b54_thiazole':  'Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1',
    'b54_pyrracid':  'O=C(O)c1cccn1Cc1ccncc1',
    'b54_target':    'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1',
    '8008_so2cl':    'O=S(=O)(Cl)c1cnc2cccnc2c1O',
    '8008_sulfonam': 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2cccnc2c1O',
    '8008_oethy':    'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC)nc2c1O',
    '8008_target':   'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#Cc3cncc(C(=O)OC)c3)nc2c1O',
}
ok_keys, fail = [], []
for k,s in test.items():
    m = Chem.MolFromSmiles(s)
    (ok_keys if m else fail).append((k,s))
print(f"Valid {len(ok_keys)}, Fail {len(fail)}")
for k,s in fail: print(f"  FAIL {k}: {s}")
