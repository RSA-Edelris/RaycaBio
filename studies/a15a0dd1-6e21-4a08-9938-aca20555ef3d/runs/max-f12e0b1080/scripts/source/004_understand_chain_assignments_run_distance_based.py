
# Understand chain assignments and then run distance-based contact maps

import math
from collections import defaultdict

def parse_atoms(path, chains=None, include_hetatm=True):
    atoms = []
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec not in ("ATOM", "HETATM"):
                continue
            if rec == "HETATM" and not include_hetatm:
                continue
            ch = line[21]
            if chains and ch not in chains:
                continue
            alt = line[16].strip()
            if alt and alt not in ('', 'A', ' '):
                continue  # skip alt B/C
            try:
                atoms.append({
                    "rec": rec, "name": line[12:16].strip(),
                    "resn": line[17:20].strip(), "chain": ch,
                    "resi": int(line[22:26]),
                    "x": float(line[30:38]), "y": float(line[38:46]), "z": float(line[46:54]),
                    "occ": float(line[54:60]), "bfac": float(line[60:66]),
                })
            except:
                pass
    return atoms

def chain_summary(path):
    counts = defaultdict(lambda: defaultdict(set))
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec in ("ATOM","HETATM"):
                ch = line[21]
                resn = line[17:20].strip()
                resi = line[22:26].strip()
                counts[ch][resn].add(resi)
    result = {}
    for ch, resns in sorted(counts.items()):
        protein_res = sum(len(v) for k,v in resns.items() if k not in ("HOH","WAT","SO4","GOL"))
        result[ch] = protein_res
    return result

print("=== 6H0F chain residue counts ===")
s6 = chain_summary(p6h0f)
for ch, n in sorted(s6.items()):
    print(f"  {ch}: {n}")

print("\n=== 2O98 chain residue counts ===")
s2 = chain_summary(p2o98)
for ch, n in sorted(s2.items()):
    print(f"  {ch}: {n}")
