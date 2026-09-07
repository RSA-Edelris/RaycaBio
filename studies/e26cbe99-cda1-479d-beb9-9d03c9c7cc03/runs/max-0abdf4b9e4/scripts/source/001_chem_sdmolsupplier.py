
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

input_file = '/home/ubuntu/rayca-artifacts/d43a861c8a85cf7cfd38dce9/files/enantio.sdf'

supplier = Chem.SDMolSupplier(input_file, removeHs=True, sanitize=True)
mols = [m for m in supplier if m is not None]
print(f"Loaded {len(mols)} molecules")
for mol in mols:
    name = mol.GetProp('_Name')
    stereo_info = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    unassigned = [c for c in stereo_info if c[1] == '?']
    print(f"\n{name}")
    print(f"  All stereocenters: {stereo_info}")
    print(f"  Unassigned/racemic centers: {unassigned}")
