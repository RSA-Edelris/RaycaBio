
# ── Phase 1: PDBFixer in-process ──────────────────────────────────────────────
from pdbfixer import PDBFixer
from openmm.app import PDBFile
import io

print("Loading 4CI2 into PDBFixer ...")
fixer = PDBFixer(filename=pdb_path)

print(f"Chains: {[c.id for c in fixer.topology.chains()]}")
print(f"Residues before: {fixer.topology.getNumResidues()}")

# Find and add missing residues (excludes tag-only termini automatically)
fixer.findMissingResidues()
n_missing = sum(len(v) for v in fixer.missingResidues.values())
print(f"Missing residues to build: {n_missing}")

# Remove terminal missing-residue segments that are pure tag (negative seqnos)
# PDBFixer returns these as keys (chain_idx, residue_idx) → residue list
keys_to_remove = []
for key in list(fixer.missingResidues.keys()):
    chain_idx, res_idx = key
    chain = list(fixer.topology.chains())[chain_idx]
    res_list = list(chain.residues())
    # If the segment falls before the first or after the last resolved residue, prune it
    if res_idx == 0 or res_idx >= len(res_list):
        keys_to_remove.append(key)

for k in keys_to_remove:
    del fixer.missingResidues[k]

n_remaining = sum(len(v) for v in fixer.missingResidues.values())
print(f"Missing residues after removing terminal tag segments: {n_remaining}")

fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()

fixer.removeHeterogens(keepWater=False)   # clean receptor: remove LVY, ZN, water

fixer.findMissingAtoms()
fixer.addMissingAtoms()

print("Adding hydrogens at pH 7.4 ...")
fixer.addMissingHydrogens(7.4)

# Write prepared receptor
receptor_path = 'PB-20260903-4CI2_receptor.pdb'
with open(receptor_path, 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

import os
print(f"Receptor written: {receptor_path}  ({os.path.getsize(receptor_path):,} bytes)")
print(f"Residues in final structure: {fixer.topology.getNumResidues()}")
print(f"Atoms in final structure:    {fixer.topology.getNumAtoms()}")
