
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.Draw import rdMolDraw2D
import base64

def svg_b64(smi, w=200, h=150):
    mol = Chem.MolFromSmiles(smi)
    if not mol: return ''
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

def mw(s):
    mol = Chem.MolFromSmiles(s)
    return round(Descriptors.MolWt(mol)) if mol else 0

SMILES = {
    'indole_acid': 'OC(=O)c1cc2cc(F)cc(F)c2[nH]1',
    'pipe_amine':  'N[C@@H]1CCCNC1',
    'amide_int':   'O=C(N[C@@H]1CCCNC1)c1cc2cc(F)cc(F)c2[nH]1',
    'dmae_br':     'CN(C)CCBr',
    'mcuf651':     'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1',
}

for k, s in SMILES.items():
    mol = Chem.MolFromSmiles(s)
    print(f"  {k}: {'OK' if mol else 'FAIL'}  MW={mw(s)}")

# Pre-generate all SVGs
svgs = {k: svg_b64(s) for k, s in SMILES.items()}
print('\nSVGs generated:', {k: bool(v) for k, v in svgs.items()})
