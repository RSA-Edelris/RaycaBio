
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import base64, html as H

def mol_b64(smi, w=175, h=125):
    mol = Chem.MolFromSmiles(smi)
    if mol is None: return None
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

# Extra intermediates needed
CDI_PAB    = 'Nc1ccc([C@@H](OC(=O)n2ccnc2)CN)cc1'
STAGE3_INT = ('CC[C@@]1(O)C(=O)OCc2c1cc1n(c2=O)Cc2c-1nc1cc(F)c(C)c3c1c2'
              '[C@@H](NC(=O)O[C@H](CN)'
              'c1ccc(NC(=O)[C@H](C)NC(=O)[C@@H](NC(C)=O)C(C)C)cc1)CC3')
POLYSAR_ARM = ('O=C1C=CC(=O)N1CCOCCOCCNC(=O)CCN(CC(=O)N)'
               'C(=O)CN(C)C(=O)CN(C)C(=O)O')  # simplified arm with mal

extra = {'CDI_PAB': CDI_PAB, 'STAGE3_INT': STAGE3_INT, 'POLYSAR_ARM': POLYSAR_ARM}
for k, s in extra.items():
    mol = Chem.MolFromSmiles(s)
    print(f"  {'OK' if mol else 'FAIL'}  {k}")

# Pre-generate all SVGs
cache = {}
all_smi = {
    'Sarcosine NCA': SAR_NCA,
    'Polysar4 stub': POLYSAR4_STUB,
    'Polysar arm': POLYSAR_ARM,
    'Mal-PEG2-NHS': MAL_PEG2_NHS,
    'PAB scaffold': PAB_SCAFFOLD,
    'CDI-PAB carbonate': CDI_PAB,
    'Carbamate int': CARBAMATE_INT,
    'Stage3 int': STAGE3_INT,
    'Mablink': MABLINK_SMILES,
    'Exatecan': EXATECAN,
    'Ac-Val-Ala': AC_VAL_ALA,
}
for name, smi in all_smi.items():
    b = mol_b64(smi, w=175, h=130)
    cache[smi] = b
    print(f"  SVG {'ok' if b else 'FAIL'}  {name}")
