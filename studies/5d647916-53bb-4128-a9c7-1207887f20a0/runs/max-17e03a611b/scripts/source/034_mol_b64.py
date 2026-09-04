
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import base64

def mol_b64(smiles, w=175, h=125):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None: return None
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

# fix: 2-amino-4-formylthiazole correct SMILES
fixed = 'Nc1nc(C=O)cs1'
mol = Chem.MolFromSmiles(fixed)
print(f"Fixed SMILES valid: {mol is not None}")
SVG_CACHE[fixed] = mol_b64(fixed)

# patch COMPOUNDS list: replace the bad SMILES in B54 Route 3 step 1
for cpd in COMPOUNDS:
    if cpd['id'] == 'B54':
        for rt in cpd['routes']:
            if 'HWE' in rt['tag']:
                steps = list(rt['steps'])
                steps[0] = ('mol', fixed, '2-Amino-4-formylthiazole', 'sm')
                rt['steps'] = tuple(steps)
                print("Patched B54 Route 3 step 0")

print(f"Cache size now: {len(SVG_CACHE)}")
