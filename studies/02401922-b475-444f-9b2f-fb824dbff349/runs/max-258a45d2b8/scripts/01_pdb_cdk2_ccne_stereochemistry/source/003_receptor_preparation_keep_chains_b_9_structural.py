
# === RECEPTOR PREPARATION ===
# Keep chains A, B + 9 structural waters contacting CTX
# Protonate at pH 7.4 with pdbfixer
# Remove CTX from receptor (used separately as reference)

from pdbfixer import PDBFixer
from openmm.app import PDBFile
import io

PDB_IN = '/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/CDK2-CCNE.pdb'

# Waters within 4A of CTX to retain
KEEP_WATERS = {'58','187','115','5','227','207','122','11','229'}

# Step 1: manual parse — extract chains A+B (ATOM) + selected HOH, strip CTX
kept_lines = []
with open(PDB_IN) as f:
    for line in f:
        rec = line[:6].strip()
        if rec == 'ATOM':
            chain = line[21]
            if chain in ('A','B'):
                kept_lines.append(line)
        elif rec == 'HETATM':
            resname = line[17:20].strip()
            resnum  = line[22:26].strip()
            chain   = line[21]
            if resname == 'HOH' and resnum in KEEP_WATERS:
                # Re-label water to chain A so pdbfixer doesn't drop it
                kept_lines.append(line[:21] + 'A' + line[22:])
            # CTX excluded from receptor (kept separately)
        elif rec in ('TER','END','CRYST1','SCALE1','SCALE2','SCALE3'):
            kept_lines.append(line)

receptor_raw = ''.join(kept_lines)
with open('receptor_raw.pdb','w') as f:
    f.write(receptor_raw)

print(f"Raw receptor lines: {len(kept_lines)}")
print(f"Waters retained: {KEEP_WATERS}")
