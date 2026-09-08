
from rdkit import Chem
from rdkit.Chem import AllChem
import os

# Read the pose SDF preserving all H atoms and 3D coords
mol = Chem.MolFromMolFile("all_poses/EL2003A_pose2.sdf", removeHs=False, sanitize=True)
print(f"Atoms: {mol.GetNumAtoms()}, H atoms: {sum(1 for a in mol.GetAtoms() if a.GetAtomicNum()==1)}")
conf = mol.GetConformer()

# Verify Z coords are non-zero (so it's genuinely 3D)
import numpy as np
pos = np.array(conf.GetPositions())
print(f"Z coord range: {pos[:,2].min():.2f} to {pos[:,2].max():.2f} Å  (non-zero = 3D ✓)")

# Write with SDWriter — RDKit SDWriter explicitly sets the 3D flag when
# a conformer with non-zero Z coords is present, preventing OpenFF from
# triggering ELF10 multi-conformer sampling.
out_path = "EL2003A_pose2_3D.sdf"
writer = Chem.SDWriter(out_path)
writer.write(mol)
writer.close()

# Verify the written file has the correct header
with open(out_path) as f:
    header_lines = [next(f) for _ in range(5)]
print("\nWritten SDF header:")
for i, l in enumerate(header_lines):
    print(f"  line {i+1}: {repr(l.rstrip())}")

# Check if the counts line has a dimensionality marker
counts_line = header_lines[3]
print(f"\nCounts line: '{counts_line.rstrip()}'")
# In V2000: position 20-22 is often used for 3D marker
print(f"  chars 20-23: '{counts_line[20:24]}'")

# Also check file size
sz = os.path.getsize(out_path)
print(f"\nFile size: {sz} bytes (original: 3500 bytes)")
print(f"Saved to: {out_path}")
