
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D
import base64

# Full Mablink SMILES from SDF
MABLINK_SMILES = ('CC[C@@]1(O)C(=O)OCc2c1cc1n(c2=O)Cc2c-1nc1cc(F)c(C)c3c1c2'
                  '[C@@H](NC(=O)O[C@H](CNC(=O)CC[C@@H](NC(=O)COCCOCCNC(=O)CCN1'
                  'C(=O)C=CC1=O)C(=O)N(C)CC(=O)N(C)CC(=O)N(C)CC(=O)N(C)CC(=O)'
                  'N(C)CC(=O)N(C)CC(=O)N(C)CC(=O)N(C)CC(=O)N(C)CC(=O)N(C)CC(=O)O)'
                  'c1ccc(NC(=O)[C@H](C)NC(=O)[C@@H](NC(C)=O)C(C)C)cc1)CC3')

# Key building-block SMILES derived by retrosynthetic disconnection
# Exatecan (payload, cut carbamate N-H → free amine)
EXATECAN = 'CC[C@@]1(O)C(=O)OCc2c1cc1n(c2=O)Cc2c-1nc1cc(F)c(C)c3c1c2[C@@H](N)CC3'

# Ac-Val-Ala-COOH  (protease-cleavable recognition dipeptide)
AC_VAL_ALA = 'CC(=O)N[C@@H](C(C)C)C(=O)N[C@H](C)C(=O)O'

# Branched PAB amino-alcohol scaffold (self-immolative; benzylic OH → carbamate,
# CH2-NH2 → amide to polysar arm, Ar-NH2 → amide to Ac-Val-Ala)
PAB_SCAFFOLD = 'Nc1ccc([C@@H](O)CN)cc1'

# Maleimide-PEG2-βAla activated NHS ester (for Glu conjugation to polysar arm)
MAL_PEG2_NHS = 'O=C1C=CC(=O)N1CCOCCOCCNC(=O)CCN1C(=O)CCC1=O'

# Sarcosine NCA monomer (for polysar10 ROP)
SAR_NCA = 'O=C1OC(=O)CN1C'

# Simplified polysar-4 stub (4 sarcosine units) — RDKit-renderable stand-in for polysar10
POLYSAR4_STUB = 'OC(=O)CN(C)C(=O)CN(C)C(=O)CN(C)C(=O)CN(C)C(=O)N'

# Linker-exatecan carbamate intermediate (PAB-CH(OC(=O)NHExatecan)(CH2NH2), Ar-NH2 free)
# = after step B (carbamate formed, before dipeptide amide and polysar amide)
CARBAMATE_INT = ('CC[C@@]1(O)C(=O)OCc2c1cc1n(c2=O)Cc2c-1nc1cc(F)c(C)c3c1c2'
                 '[C@@H](NC(=O)O[C@H](CN)c1ccc(N)cc1)CC3')

# validate
smiles_map = {
    'Mablink (full)': MABLINK_SMILES,
    'Exatecan': EXATECAN,
    'Ac-Val-Ala-COOH': AC_VAL_ALA,
    'PAB scaffold': PAB_SCAFFOLD,
    'Mal-PEG2-NHS': MAL_PEG2_NHS,
    'Sarcosine NCA': SAR_NCA,
    'Polysar stub (×4)': POLYSAR4_STUB,
    'Carbamate intermediate': CARBAMATE_INT,
}
for name, smi in smiles_map.items():
    mol = Chem.MolFromSmiles(smi)
    mw = Descriptors.MolWt(mol) if mol else None
    print(f"  {'OK' if mol else 'FAIL'}  MW={mw:.0f if mw else 'N/A'}  {name}")
