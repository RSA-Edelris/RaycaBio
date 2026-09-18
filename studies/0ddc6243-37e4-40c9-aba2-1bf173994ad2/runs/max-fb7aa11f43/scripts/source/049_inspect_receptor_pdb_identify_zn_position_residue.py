
# Inspect receptor PDB: identify ZN position, residue ranges, and key residue numbers
# needed for the analysis script
import re

receptor_amb = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_amber.pdb"
zn_lines, chain_ranges, key_residues = [], {}, {}

res_seen = {}  # (chain, resname, resnum) → True

with open(receptor_amb) as f:
    for line in f:
        if not line.startswith(('ATOM','HETATM')): continue
        resname = line[17:20].strip()
        chain   = line[21]
        resnum  = line[22:26].strip()
        key = (chain, resnum)
        if key not in res_seen:
            res_seen[key] = resname
            if chain not in chain_ranges:
                chain_ranges[chain] = [int(resnum), int(resnum)]
            else:
                rn = int(resnum)
                chain_ranges[chain][0] = min(chain_ranges[chain][0], rn)
                chain_ranges[chain][1] = max(chain_ranges[chain][1], rn)
        if resname == 'ZN':
            zn_lines.append(line.rstrip())
        # Key binding site residues
        if chain == 'Z' and resnum in ('353','357','378','380','400','402','351','391'):
            key_residues[f"Z:{resname}{resnum}"] = resnum
        if chain == 'X' and resnum in ('572','573','574','575','628'):
            key_residues[f"X:{resname}{resnum}"] = resnum

print("Chain residue ranges:")
for ch, (lo, hi) in sorted(chain_ranges.items()):
    print(f"  Chain {ch}: {lo}–{hi}")

print(f"\nZN lines ({len(zn_lines)}):")
for l in zn_lines: print(f"  {l}")

print(f"\nKey binding site residues in PDB:")
for k,v in sorted(key_residues.items()):
    print(f"  {k} → seqid {v}")

# How many residues in CRBN (Z) and GSPT1 (X)?
crbn_res  = sum(1 for (ch,rn),rname in res_seen.items() if ch=='Z')
gspt1_res = sum(1 for (ch,rn),rname in res_seen.items() if ch=='X')
print(f"\nCRBN (Z): {crbn_res} residues")
print(f"GSPT1 (X): {gspt1_res} residues")
