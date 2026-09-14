
import numpy as np
from scipy.spatial.distance import cdist

def parse_pdb_atoms(path):
    atoms = []
    with open(path) as f:
        for line in f:
            if line[:6] not in ("ATOM  ", "HETATM"):
                continue
            chain   = line[21]
            resseq  = int(line[22:26].strip())
            resname = line[17:20].strip()
            name    = line[12:16].strip()
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            atoms.append((chain, resname, resseq, name, np.array([x, y, z])))
    return atoms

def surface_lys_shell(pdb_path, lo=3.5, hi=12.0):
    """
    Return ERα LYS where NZ is within (lo, hi] Å of any CRBN heavy atom.
    lo filters out artefactual direct-clash geometry; hi = 'presented to ligase'.
    """
    atoms = parse_pdb_atoms(pdb_path)
    crbn_xyz = np.array([a[4] for a in atoms if a[0]=='B'])
    lys_nz = [(a[2], a[4]) for a in atoms if a[0]=='A' and a[1]=='LYS' and a[3]=='NZ']
    result = []
    for resseq, xyz in lys_nz:
        d = float(np.linalg.norm(crbn_xyz - xyz, axis=1).min())
        if lo < d <= hi:
            result.append((resseq, round(d, 1)))
    result.sort(key=lambda x: x[1])
    return result

# Also get closest distance (regardless of threshold) per LYS per compound
def lys_closest(pdb_path):
    atoms = parse_pdb_atoms(pdb_path)
    crbn_xyz = np.array([a[4] for a in atoms if a[0]=='B'])
    lys_nz = [(a[2], a[4]) for a in atoms if a[0]=='A' and a[1]=='LYS' and a[3]=='NZ']
    return {resseq: round(float(np.linalg.norm(crbn_xyz - xyz, axis=1).min()), 1)
            for resseq, xyz in lys_nz}

print("=== ERα LYSINES PRESENTED TO CRBN (NZ 3.5–12 Å from any CRBN heavy atom) ===")
print()
compound_lys = {}
for cmpd in [f"ARV_{i:03d}" for i in range(1, 11)]:
    pred = (f"{SESSION}/{cmpd}/boltz_results_{cmpd}_constrained/"
            f"predictions/{cmpd}_constrained/{cmpd}_constrained_model_0.pdb")
    hits = surface_lys_shell(pred, lo=3.5, hi=12.0)
    compound_lys[cmpd] = hits
    lig_crbn = scores[cmpd][0]["lig_crbn"]
    hit_str = ", ".join(f"K{r}({d}Å)" for r, d in hits)
    print(f"  {cmpd}  lig→CRBN={lig_crbn:.4f}  [{len(hits)}] {hit_str}")

# Count how many compounds each ERα lysine is presented in
from collections import Counter
lys_counts = Counter()
for cmpd, hits in compound_lys.items():
    for r, d in hits:
        lys_counts[r] += 1

print("\n=== ERα LYSINES PRESENTED IN ≥5 COMPOUNDS ===")
common = [(r, n) for r, n in sorted(lys_counts.items(), key=lambda x: -x[1]) if n >= 5]
for r, n in common:
    print(f"  K{r:3d}  presented in {n}/10 compounds")

print("\n=== ALL LYSINES PRESENTED IN ≥3 COMPOUNDS ===")
for r, n in [(r, n) for r, n in sorted(lys_counts.items(), key=lambda x: -x[1]) if n >= 3]:
    print(f"  K{r:3d}  {n}/10")
