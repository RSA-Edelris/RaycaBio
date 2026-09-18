
import numpy as np

# ── 1. Parse 5EU1: extract chain A BRD9 protein atoms + 5SW ligand ──────────
brd9_atoms = []   # {name, resname, resseq, x, y, z}
lig_atoms  = []   # BI-7273 (5SW chain A res 201)

for line in pdb_text.splitlines():
    if not (line.startswith("ATOM") or line.startswith("HETATM")):
        continue
    chain   = line[21]
    resname = line[17:20].strip()
    resseq  = int(line[22:26])
    aname   = line[12:16].strip()
    x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    rec = {"name": aname, "resname": resname, "resseq": resseq,
           "x": x, "y": y, "z": z, "chain": chain}
    if line.startswith("ATOM") and chain == "A":
        brd9_atoms.append(rec)
    if line.startswith("HETATM") and resname == "5SW" and chain == "A":
        lig_atoms.append(rec)

print(f"BRD9 chain-A atoms: {len(brd9_atoms)}")
print(f"BI-7273 (5SW) atoms: {len(lig_atoms)}")
for a in lig_atoms:
    print(f"  {a['name']:4s}  ({a['x']:7.3f}, {a['y']:7.3f}, {a['z']:7.3f})")
