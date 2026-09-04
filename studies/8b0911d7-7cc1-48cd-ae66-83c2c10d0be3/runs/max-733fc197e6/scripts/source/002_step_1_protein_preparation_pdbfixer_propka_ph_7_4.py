
# Step 1: Protein preparation with PDBFixer + PROPKA pH 7.4
import os, subprocess
from pdbfixer import PDBFixer
from openmm.app import PDBFile

PDB_IN = '/home/ubuntu/rayca-artifacts/db61873ef1ff7fa5e8bf27d4/files/9C56.pdb'
WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
PDB_FIXED = os.path.join(WORKDIR, '9C56_prepared.pdb')

fixer = PDBFixer(filename=PDB_IN)

# Find and fix missing residues
fixer.findMissingResidues()
print("Missing residue segments:", {k: [r.name for r in v] for k,v in fixer.missingResidues.items()})

# Remove C-terminal disordered tail (281-314) - too long/disordered for loop modelling
# Only add short loops: residues 182-184 (3 residues) and N-term GLY0/MET1
# The C-terminal tail 281-314 is 34 residues - keep truncated
chains = list(fixer.topology.chains())
print(f"Chains: {[c.id for c in chains]}")
print(f"Residue range: {list(fixer.topology.residues())[0].id} - {list(fixer.topology.residues())[-1].id}")
