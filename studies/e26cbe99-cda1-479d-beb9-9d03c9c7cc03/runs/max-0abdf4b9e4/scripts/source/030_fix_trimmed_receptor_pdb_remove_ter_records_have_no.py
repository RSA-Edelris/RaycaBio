
# Fix the trimmed receptor PDB: remove TER records that have no preceding ATOM records
# on the same chain within this file.

with open('PB-20260903-4CI2_receptor_trimmed.pdb') as f:
    raw_lines = f.readlines()

# Find which chains actually have ATOM/HETATM records
chains_with_atoms = set()
for line in raw_lines:
    rec = line[:6].strip()
    if rec in ('ATOM', 'HETATM') and len(line) >= 22:
        chains_with_atoms.add(line[21])   # chain ID

print(f"Chains with ATOM records: {sorted(chains_with_atoms)}")

# Rebuild file, dropping TER records whose chain has no atoms
fixed_lines = []
for line in raw_lines:
    rec = line[:6].strip()
    if rec == 'TER' and len(line) >= 22:
        chain = line[21]
        if chain not in chains_with_atoms:
            print(f"  Dropping orphan TER for chain '{chain}': {line.rstrip()}")
            continue
    fixed_lines.append(line)

fixed_path = 'PB-20260903-4CI2_receptor_trimmed_fixed.pdb'
with open(fixed_path, 'w') as f:
    f.writelines(fixed_lines)
print(f"\nFixed PDB written: {len(fixed_lines)} lines  "
      f"(removed {len(raw_lines)-len(fixed_lines)} orphan TER lines)")

# Quick verify: try loading with OpenMM
import openmm as mm
from openmm.app import PDBFile, ForceField, NoCutoff
from openmm import unit

rec_pdb = PDBFile(fixed_path)
print(f"OpenMM topology: {rec_pdb.topology.getNumChains()} chains, "
      f"{rec_pdb.topology.getNumResidues()} residues, "
      f"{rec_pdb.topology.getNumAtoms()} atoms")
