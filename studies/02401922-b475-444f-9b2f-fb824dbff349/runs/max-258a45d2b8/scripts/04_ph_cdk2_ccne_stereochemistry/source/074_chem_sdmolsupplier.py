
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem.rdchem import StereoInfo
import subprocess, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
sdf_path = "/home/ubuntu/rayca-artifacts/fec3a540149a0d0fc51a148c/files/Sorted_Cedilla.sdf"

# Reload
suppl = Chem.SDMolSupplier(sdf_path, removeHs=True, sanitize=True)
raw_mols = [m for m in suppl if m is not None]

# Standardization pipeline
lfc = rdMolStandardize.LargestFragmentChooser()
te = rdMolStandardize.TautomerEnumerator()
un = rdMolStandardize.Uncharger()

std_mols = []
std_info = []
for mol in raw_mols:
    name = mol.GetProp('_Name') if mol.HasProp('_Name') else 'unk'
    # 1. largest fragment
    m = lfc.choose(mol)
    # 2. canonical tautomer
    m = te.Canonicalize(m)
    # 3. keep neutral (don't uncharge - we want to apply pH later with obabel)
    Chem.SanitizeMol(m)
    m.SetProp('_Name', name)
    # Check stereocenters
    si = Chem.FindMolChiralCenters(m, includeUnassigned=True)
    undef = [s for s in si if s[1] == '?']
    std_mols.append(m)
    std_info.append({'name': name, 'stereo': si, 'undef': undef,
                     'mw': Descriptors.MolWt(m), 'q': Chem.GetFormalCharge(m)})

# Report stereocenters needing attention
print(f"Standardized: {len(std_mols)} molecules")
print("\nStereocenters:")
for i, info in enumerate(std_info):
    if info['stereo']:
        print(f"  {i+1:3d}. {info['name']:30s}  stereo={info['stereo']}  undef={info['undef']}")

# Write standardized SDF (neutral, no H) for obabel pH protonation
out_sdf = os.path.join(wd, "all_std_neutral.sdf")
writer = Chem.SDWriter(out_sdf)
for m in std_mols:
    writer.write(m)
writer.close()
print(f"\nWritten: {out_sdf} ({os.path.getsize(out_sdf)//1024} KB)")
