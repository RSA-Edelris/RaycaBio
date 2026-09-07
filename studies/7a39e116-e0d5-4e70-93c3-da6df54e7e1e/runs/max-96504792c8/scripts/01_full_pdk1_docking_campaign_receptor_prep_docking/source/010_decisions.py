
import pdbfixer, openmm, shutil
from pdbfixer import PDBFixer
from openmm.app import PDBFile

WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
WORK = "/work"

# ── Receptor preparation decisions (all documented) ─────────────────────────
# 1. pH 7.4: addHydrogens uses OpenMM propka-equivalent pKa estimates
# 2. Missing residues SER231-ASN240 (activation loop, SEQRES-derived): rebuilt
# 3. replaceNonstandardResidues: SEP241→SER (phosphoserine→serine, phosphate group
#    removed — not in binding site, acceptable for docking study)
# 4. removeHeterogens=True, keepWater=False: LI8, GOL, SO4, CL stripped.
#    No waters within 5 Å of LI8 center → no conserved waters retained.
# 5. Box: center (−4.28, 43.73, 44.51), 22×22×22 Å, derived from LI8 centroid.

fixer = PDBFixer(filename=f"{WS}/1Z5M.pdb")

# Step 1 – missing residues (activation loop SER231-ASN240)
fixer.findMissingResidues()
print("Missing residue chains/keys:", list(fixer.missingResidues.keys())[:10])
fixer.findNonstandardResidues()
print("Nonstandard residues:", fixer.nonstandardResidues)
fixer.replaceNonstandardResidues()

# Step 2 – remove heterogens (strip LI8, GOL, SO4, CL, waters)
fixer.removeHeterogens(keepWater=False)

# Step 3 – missing heavy atoms
fixer.findMissingAtoms()
print("Missing atoms (sample):", {str(k): len(v) for k,v in list(fixer.missingAtoms.items())[:5]})
fixer.addMissingAtoms()

# Step 4 – hydrogens at pH 7.4
fixer.addMissingHydrogens(7.4)

# Step 5 – save prepared receptor
rec_path = f"{WS}/1Z5M_receptor_pH7.4.pdb"
with open(rec_path, "w") as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

import os
size = os.path.getsize(rec_path)
print(f"\nReceptor written: {rec_path} ({size} bytes)")

# Copy to /work for gnina dispatch
shutil.copy(rec_path, f"{WORK}/1Z5M_receptor_pH7.4.pdb")
print(f"Copied to /work/1Z5M_receptor_pH7.4.pdb")

# Count atoms
lines_rec = open(rec_path).readlines()
atom_count = sum(1 for l in lines_rec if l.startswith(("ATOM","HETATM")))
print(f"Atom count in prepared receptor: {atom_count}")
