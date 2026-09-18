#!/usr/bin/env python3
"""Create GROMACS index file for analysis groups from a solvated .gro file."""
import sys, os

gro = sys.argv[1]
ndx = sys.argv[2]
cid = sys.argv[3]          # compound ID = ligand mol name in topology

CHAIN_A_ATOMS = 4859       # from pdb2gmx output
CHAIN_B_ATOMS = 4375

# Parse gro file
with open(gro) as f:
    f.readline()           # title
    n = int(f.readline())
    atoms = []
    for _ in range(n):
        line = f.readline()
        resname = line[5:10].strip()
        atoms.append(resname)

chain_a  = list(range(1, CHAIN_A_ATOMS + 1))
chain_b  = list(range(CHAIN_A_ATOMS + 1, CHAIN_A_ATOMS + CHAIN_B_ATOMS + 1))
lig_idx  = [i + 1 for i, r in enumerate(atoms) if r == "MOL"]
wat_idx  = [i + 1 for i, r in enumerate(atoms) if r == "SOL"]
ion_idx  = [i + 1 for i, r in enumerate(atoms) if r in ("NA", "CL")]
prot_idx = chain_a + chain_b

def write_grp(fh, name, indices):
    fh.write(f"[ {name} ]\n")
    for j, idx in enumerate(indices):
        fh.write(f" {idx}")
        if (j + 1) % 15 == 0:
            fh.write("\n")
    fh.write("\n\n")

with open(ndx, "w") as fh:
    write_grp(fh, "System",        list(range(1, n + 1)))
    write_grp(fh, "Protein",       prot_idx)
    write_grp(fh, "ChainA_CDK2",   chain_a)
    write_grp(fh, "ChainB_CyclinE", chain_b)
    write_grp(fh, "LIG",           lig_idx)
    write_grp(fh, "Protein_LIG",   prot_idx + lig_idx)
    write_grp(fh, "Water",         wat_idx)
    write_grp(fh, "Ion",           ion_idx)
    write_grp(fh, "Water_and_ions", wat_idx + ion_idx)
    write_grp(fh, "non_Protein",   lig_idx + wat_idx + ion_idx)

print(f"Index written: {ndx}  ({len(chain_a)} A, {len(chain_b)} B, {len(lig_idx)} LIG atoms)")
