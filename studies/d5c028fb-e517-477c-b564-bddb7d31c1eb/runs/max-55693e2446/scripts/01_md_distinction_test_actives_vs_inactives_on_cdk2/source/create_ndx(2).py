#!/usr/bin/env python3
"""Append custom analysis groups to a GROMACS index file.

Usage:  create_ndx.py <ions.gro> <base_ndx> <analysis_ndx> <cid>

The caller should first generate base_ndx with:
    echo "q" | gmx make_ndx -f ions.gro -o base_ndx

This script reads base_ndx, appends the custom groups, and writes analysis_ndx.
Custom groups: ChainA_CDK2, ChainB_CyclinE, LIG, Protein_LIG, non-Protein
"""
import sys, os

gro        = sys.argv[1]
base_ndx   = sys.argv[2]
out_ndx    = sys.argv[3]
cid        = sys.argv[4]

CHAIN_A_ATOMS = 4859   # atoms in chain A from pdb2gmx
CHAIN_B_ATOMS = 4375   # atoms in chain B from pdb2gmx

with open(gro) as f:
    f.readline()
    n = int(f.readline())
    atoms = []
    for _ in range(n):
        line = f.readline()
        resname = line[5:10].strip()
        atoms.append(resname)

chain_a  = list(range(1, CHAIN_A_ATOMS + 1))
chain_b  = list(range(CHAIN_A_ATOMS + 1, CHAIN_A_ATOMS + CHAIN_B_ATOMS + 1))
prot_idx = chain_a + chain_b
lig_idx  = [i + 1 for i, r in enumerate(atoms) if r == "MOL"]
wat_idx  = [i + 1 for i, r in enumerate(atoms) if r == "SOL"]
ion_idx  = [i + 1 for i, r in enumerate(atoms) if r in ("NA", "CL")]
non_prot = lig_idx + wat_idx + ion_idx

def fmt_grp(name, indices):
    lines = [f"[ {name} ]\n"]
    for j, idx in enumerate(indices):
        lines.append(f" {idx}")
        if (j + 1) % 15 == 0:
            lines.append("\n")
    lines.append("\n\n")
    return "".join(lines)

# Start from the default index file
with open(base_ndx) as f:
    base = f.read()

with open(out_ndx, "w") as fh:
    fh.write(base.rstrip() + "\n\n")
    fh.write(fmt_grp("ChainA_CDK2",    chain_a))
    fh.write(fmt_grp("ChainB_CyclinE", chain_b))
    fh.write(fmt_grp("LIG",            lig_idx))
    fh.write(fmt_grp("Protein_LIG",    prot_idx + lig_idx))
    fh.write(fmt_grp("Water",          wat_idx))
    fh.write(fmt_grp("Ion",            ion_idx))
    fh.write(fmt_grp("Water_and_ions", wat_idx + ion_idx))

print(f"Index written: {out_ndx}  "
      f"(ChainA={len(chain_a)}, ChainB={len(chain_b)}, LIG={len(lig_idx)}, "
      f"SOL={len(wat_idx)}, Ion={len(ion_idx)})")
