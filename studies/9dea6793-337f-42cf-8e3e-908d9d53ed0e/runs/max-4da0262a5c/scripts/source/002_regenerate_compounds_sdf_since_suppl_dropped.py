
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import os

# Regenerate compounds from the sdf since suppl was dropped
sdf_path = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"
suppl2 = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)

mols = []
names = []
for mol in suppl2:
    if mol is not None:
        name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'unnamed'
        # Compute 2D coords if not already set
        AllChem.Compute2DCoords(mol)
        mols.append(mol)
        names.append(name)

# Draw all compounds in a grid
img = Draw.MolsToGridImage(
    mols, 
    molsPerRow=4, 
    subImgSize=(400,300),
    legends=names,
    returnPNG=True
)

outpath = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4/all_targets_grid.png"
with open(outpath, 'wb') as f:
    f.write(img)
print(f"Saved grid image to {outpath}")
print(f"Total molecules: {len(mols)}")
for i, (m, n) in enumerate(zip(mols, names)):
    print(f"  {i+1}. {n}: {Chem.MolToSmiles(m)}")
