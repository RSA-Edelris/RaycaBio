
# Check protonation tools and RDKit capabilities
import subprocess

# Check dimorphite-dl
r = subprocess.run(['python3', '-c', 'import dimorphite_dl'], capture_output=True, text=True)
print(f"dimorphite_dl: {'available' if r.returncode==0 else 'not available'}")

# Check obabel protonation
r = subprocess.run(['obabel', '--help'], capture_output=True, text=True)
print(f"obabel -p flag: {'-p' in r.stdout or '-p' in r.stderr}")

# RDKit EnumerateStereoisomers
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
from rdkit.Chem import AllChem, SDMolSupplier, SDWriter, Descriptors
from rdkit import Chem
print("rdkit stereo enumeration: available")

# Test reading V3000
INPUT_SDF = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_lig_results_2.sdf"
sup = SDMolSupplier(INPUT_SDF, removeHs=False)
mols = [m for m in sup if m is not None]
print(f"\nMolecules read by RDKit: {len(mols)}")
for m in mols:
    name = m.GetProp('_Name') if m.HasProp('_Name') else 'unnamed'
    mol_name = m.GetProp('Molecule Name') if m.HasProp('Molecule Name') else name
    si = m.GetStereoInfo()
    n_stereo = len(Chem.FindMolChiralCenters(m, includeUnassigned=True))
    n_unassigned = len(Chem.FindMolChiralCenters(m, includeUnassigned=True, useLegacyImplementation=False))
    print(f"  {mol_name}: {m.GetNumAtoms()} atoms, chiral centers={n_stereo}")
