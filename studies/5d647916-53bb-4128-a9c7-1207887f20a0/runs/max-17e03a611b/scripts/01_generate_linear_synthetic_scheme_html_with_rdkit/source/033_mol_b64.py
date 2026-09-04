
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

missing = [s for s in SVG_CACHE if SVG_CACHE[s] is None]
# actually find which SMILES is NOT in cache
unique_smi = set()
for cpd in COMPOUNDS:
    unique_smi.add(cpd['target_smiles'])
    for rt in cpd['routes']:
        for s in rt['steps']:
            if s[0] == 'mol':
                unique_smi.add(s[1])

failed_smi = [s for s in unique_smi if s not in SVG_CACHE]
print("Not in cache:", failed_smi)

# Try each one explicitly
for smi in failed_smi:
    mol = Chem.MolFromSmiles(smi)
    print(f"  {smi[:60]}  mol={'OK' if mol else 'FAIL'}")
    if mol:
        b = mol_b64(smi)
        SVG_CACHE[smi] = b
        print(f"  → generated")
