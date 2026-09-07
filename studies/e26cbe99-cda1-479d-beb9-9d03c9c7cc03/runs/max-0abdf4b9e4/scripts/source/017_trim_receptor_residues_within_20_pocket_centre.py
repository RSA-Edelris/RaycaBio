
import numpy as np

# ── Trim receptor to residues within 20 Å of pocket centre ───────────────────
TRIM_RADIUS = 20.0

# Parse receptor (with H) — find which residues have ANY atom within radius
with open(receptor_path) as f:
    rec_lines = f.readlines()

# First pass: collect residue IDs (chain+resnum) whose heavy atoms are in radius
keep_residues = set()
for line in rec_lines:
    rec = line[:6].strip()
    if rec not in ('ATOM', 'HETATM'):
        continue
    try:
        x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    except:
        continue
    d = np.sqrt((x-pocket_cx)**2 + (y-pocket_cy)**2 + (z-pocket_cz)**2)
    if d <= TRIM_RADIUS:
        chain  = line[21]
        resnum = line[22:27].strip()
        keep_residues.add((chain, resnum))

# Second pass: write trimmed PDB keeping all atoms of kept residues
trimmed_path = 'PB-20260903-4CI2_receptor_trimmed.pdb'
written = 0
with open(trimmed_path, 'w') as out:
    for line in rec_lines:
        rec = line[:6].strip()
        if rec in ('ATOM', 'HETATM'):
            chain  = line[21]
            resnum = line[22:27].strip()
            if (chain, resnum) not in keep_residues:
                continue
        out.write(line)
        written += 1

import os
print(f"Kept {len(keep_residues)} residues within {TRIM_RADIUS} Å of pocket centre")
print(f"Trimmed receptor: {trimmed_path}  "
      f"({os.path.getsize(trimmed_path):,} bytes, {written} lines)")

# Also make a noH version for gnina (gnina handles H internally)
trimmed_noh_path = 'PB-20260903-4CI2_receptor_trimmed_noH.pdb'
with open(trimmed_path) as fin, open(trimmed_noh_path, 'w') as fout:
    for line in fin:
        rec = line[:6].strip()
        if rec in ('ATOM', 'HETATM'):
            aname = line[12:16].strip()
            if aname.startswith('H'):
                continue
        fout.write(line)

print(f"No-H trimmed receptor: {trimmed_noh_path}  "
      f"({os.path.getsize(trimmed_noh_path):,} bytes)")
