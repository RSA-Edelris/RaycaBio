
import os

# 1. Remove ZN from receptor and write clean version
receptor_in  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_amber.pdb"
receptor_nozn = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/md/receptor_nozn.pdb"
os.makedirs(os.path.dirname(receptor_nozn), exist_ok=True)

with open(receptor_in) as fin, open(receptor_nozn, 'w') as fout:
    for line in fin:
        if line.startswith('HETATM') and 'ZN' in line[17:21]:
            continue  # drop ZN
        fout.write(line)
print(f"Wrote {os.path.getsize(receptor_nozn):,} bytes (ZN removed)")

# 2. Compute AMBER topology residue indices for key residues
# tleap reads chain Z first, then chain X (order in PDB).
# Count unique (chain, seqid) in PDB order → amber residue index
from collections import OrderedDict

amber_idx = {}    # (chain, seqid_int) → 1-based amber residue index
idx = 0
last_key = None

with open(receptor_nozn) as f:
    for line in f:
        if not line.startswith(('ATOM','HETATM')): continue
        ch  = line[21]
        sid = int(line[22:26])
        key = (ch, sid)
        if key != last_key:
            idx += 1
            amber_idx[key] = idx
            last_key = key

crbn_end  = max(v for (ch,_),v in amber_idx.items() if ch=='Z')
gspt1_end = max(v for (ch,_),v in amber_idx.items() if ch=='X')

# Key residues
crbn_start  = min(v for (ch,_),v in amber_idx.items() if ch=='Z')
gspt1_start = min(v for (ch,_),v in amber_idx.items() if ch=='X')

w380  = amber_idx.get(('Z',380), 'MISSING')
w400  = amber_idx.get(('Z',400), 'MISSING')
h353  = amber_idx.get(('Z',353), 'MISSING')
k572  = amber_idx.get(('X',572), 'MISSING')
k628  = amber_idx.get(('X',628), 'MISSING')
lig_idx = gspt1_end + 1  # LIG is appended after protein by tleap

print(f"CRBN  residues: amber {crbn_start}–{crbn_end}  (total {crbn_end - crbn_start + 1})")
print(f"GSPT1 residues: amber {gspt1_start}–{gspt1_end}  (total {gspt1_end - gspt1_start + 1})")
print(f"LIG (approx):   amber {lig_idx}")
print(f"\nKey residue AMBER indices:")
print(f"  W380 (CRBN Trp-cage floor): {w380}")
print(f"  W400 (CRBN Trp-cage lid):   {w400}")
print(f"  H353 (CRBN H-bond):         {h353}")
print(f"  K572 (GSPT1 neo):           {k572}")
print(f"  K628 (GSPT1 neo):           {k628}")
