
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.Draw import rdMolDraw2D
import base64, re

def mol_b64(smi, w=175, h=130):
    mol = Chem.MolFromSmiles(smi)
    if not mol: return None
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

def mw(smi):
    mol = Chem.MolFromSmiles(smi)
    return round(Descriptors.MolWt(mol)) if mol else 0

# Correct SMILES
INDOLE_ACID = 'OC(=O)c1cc2cc(F)cc(F)c2[nH]1'
PIPE_AMINE  = 'N[C@@H]1CCCNC1'
AMIDE_INT   = 'O=C(N[C@@H]1CCCNC1)c1cc2cc(F)cc(F)c2[nH]1'
DMAE_BR     = 'CN(C)CCBr'
MCUF651     = 'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1'

for smi, name in [(INDOLE_ACID,'Indole acid'), (PIPE_AMINE,'Pipe amine'),
                  (AMIDE_INT,'Amide int'), (DMAE_BR,'DMAE-Br'), (MCUF651,'MCUF651')]:
    mol = Chem.MolFromSmiles(smi)
    print(f"  {name}: {'OK' if mol else 'FAIL'}  MW={mw(smi)}")
