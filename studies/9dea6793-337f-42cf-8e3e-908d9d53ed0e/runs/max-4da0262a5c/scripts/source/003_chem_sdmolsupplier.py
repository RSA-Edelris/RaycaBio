
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import os

sdf_path = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"
suppl3 = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)

mols2, names2 = [], []
for mol in suppl3:
    if mol is not None:
        AllChem.Compute2DCoords(mol)
        mols2.append(mol)
        names2.append(mol.GetProp('_Name') if mol.HasProp('_Name') else 'unnamed')

outdir = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4"
saved = []
for mol, name in zip(mols2, names2):
    drawer = rdMolDraw2D.MolDraw2DCairo(500, 400)
    drawer.drawOptions().addStereoAnnotation = True
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    path = os.path.join(outdir, f"struct_{name}.png")
    with open(path, 'wb') as f:
        f.write(drawer.GetDrawingText())
    saved.append(path)

print("Saved individual structures:")
for p in saved:
    print(" ", p)
