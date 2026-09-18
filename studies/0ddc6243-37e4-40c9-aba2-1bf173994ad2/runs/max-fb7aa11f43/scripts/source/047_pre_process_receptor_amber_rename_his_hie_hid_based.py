
# Pre-process receptor for AMBER: rename HIS→HIE/HID based on documented protonation states
receptor_in  = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_CRBN_GSPT1.pdb"
receptor_amb = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/receptor_amber.pdb"

# HIS renaming map (seqid → AMBER residue name)
# HIS353 → HIE (ε-protonated, contacts ligand O4 via NE2)
# HIS357 → HID
# HIS378 → HID
# All other HIS → HID
his_map = {'353': 'HIE', '357': 'HID', '378': 'HID'}

lines_out = []
with open(receptor_in) as f:
    for line in f:
        if line.startswith(('ATOM', 'HETATM')):
            resname = line[17:20].strip()
            resseq  = line[22:26].strip()
            if resname == 'HIS':
                new_name = his_map.get(resseq, 'HID')
                line = line[:17] + f'{new_name:<3}' + line[20:]
        lines_out.append(line)

with open(receptor_amb, 'w') as f:
    f.writelines(lines_out)

# Count HIS variants
from collections import Counter
variants = Counter()
with open(receptor_amb) as f:
    for line in f:
        if line.startswith('ATOM') and line[17:20] in ('HIE','HID','HIP'):
            variants[line[17:20]] += 1
print("HIS variant counts in AMBER-ready receptor:")
for k,v in variants.items():
    print(f"  {k}: {v} residues")

import os
print(f"\nWrote {os.path.getsize(receptor_amb):,} bytes → {receptor_amb}")
print("ZN present:", any('ZN' in line for line in open(receptor_amb)))
