
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

# Load the molecule
suppl = Chem.SDMolSupplier(
    '/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files/P922_Results.sdf',
    removeHs=False, sanitize=True
)
mols = [m for m in suppl if m is not None]
print(f"Loaded {len(mols)} molecule(s)")

for mol in mols:
    name = mol.GetPropsAsDict().get('_Name', 'unnamed')
    print(f"\nMolecule: {name}")
    
    # Find stereocenters
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    stereo_info = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    print(f"  Chiral centers: {stereo_info}")
    
    unspec = [(idx, s) for idx, s in stereo_info if s == '?']
    spec   = [(idx, s) for idx, s in stereo_info if s != '?']
    print(f"  Specified: {spec}")
    print(f"  Unspecified (racemic): {unspec}")
    print(f"  SMILES: {Chem.MolToSmiles(mol)}")
