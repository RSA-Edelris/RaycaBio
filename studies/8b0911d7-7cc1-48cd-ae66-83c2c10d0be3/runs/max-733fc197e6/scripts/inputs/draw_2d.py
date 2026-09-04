import os, json
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'

ligands_2d = [
    {"id": "EDS00760714-1", "name": "Compound 32 (R)", "smiles": "Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NCCF)n2)nc2ccccc21", "kd": "1-5 uM"},
    {"id": "EDS00760778-1", "name": "Compound 16 (R)", "smiles": "Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NC3CCC3)n2)nc2ccccc21", "kd": "<1 uM"},
    {"id": "EDS00760778-2", "name": "Compound 16 (S)", "smiles": "Cn1c(CN2CC3(CC3)C[C@H]2c2cccc(C(=O)NC3CCC3)n2)nc2ccccc21", "kd": "n.d."},
    {"id": "EDS00760714-2", "name": "Compound 32 (S)", "smiles": "Cn1c(CN2CC3(CC3)C[C@H]2c2cccc(C(=O)NCCF)n2)nc2ccccc21", "kd": "n.d."},
]

out_dir = os.path.join(WORKDIR, 'figures')
os.makedirs(out_dir, exist_ok=True)

mols, legends = [], []
for lig in ligands_2d:
    mol = Chem.MolFromSmiles(lig["smiles"])
    AllChem.Compute2DCoords(mol)
    mols.append(mol)
    legends.append(f"{lig['name']}\nKd: {lig['kd']}")
    d = rdMolDraw2D.MolDraw2DCairo(400, 300)
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    p = os.path.join(out_dir, f"{lig['id']}_2d.png")
    with open(p, 'wb') as f:
        f.write(d.GetDrawingText())
    print(f"Wrote {p}")

img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(500,400), legends=legends, useSVG=False)
grid_path = os.path.join(out_dir, 'ligands_grid_2d.png')
img.save(grid_path)
print(f"Grid: {grid_path}")
print("DONE")
