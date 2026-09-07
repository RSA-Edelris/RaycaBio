
# Extract LVY (lenalidomide) coordinates → pocket centre; also show missing residue summary
import numpy as np

lvy_atoms = []
missing_res_lines = []
remark_zone = False

for line in lines:
    rec = line[:6].strip()
    if rec in ('HETATM', 'ATOM'):
        res_name = line[17:20].strip()
        if res_name == 'LVY':
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            lvy_atoms.append((x, y, z))
    if 'REMARK 465' in line[:12]:
        if 'SSSEQ' in line:
            remark_zone = True
        if remark_zone and len(line) > 20 and line[15:18].strip().isalpha() and len(line[15:18].strip()) == 3:
            missing_res_lines.append(line.rstrip())

if lvy_atoms:
    cx = np.mean([a[0] for a in lvy_atoms])
    cy = np.mean([a[1] for a in lvy_atoms])
    cz = np.mean([a[2] for a in lvy_atoms])
    print(f"LVY atoms: {len(lvy_atoms)}")
    print(f"Pocket centre (Å): x={cx:.2f}  y={cy:.2f}  z={cz:.2f}")
else:
    print("LVY not found — checking all HETATMs:")
    het = set()
    for line in lines:
        if line[:6].strip() == 'HETATM':
            het.add(line[17:20].strip())
    print(het)

print(f"\nMissing residues (first 20): {len(missing_res_lines)} total")
for r in missing_res_lines[:20]:
    print(' ', r)
