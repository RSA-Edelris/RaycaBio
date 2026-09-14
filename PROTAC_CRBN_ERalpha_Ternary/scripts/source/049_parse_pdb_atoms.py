
import numpy as np
from collections import defaultdict

def parse_pdb_atoms(path):
    """Return dict keyed by (chain, resname, resseq, name) -> np.array(xyz)"""
    atoms = []
    with open(path) as f:
        for line in f:
            if line[:6] not in ("ATOM  ", "HETATM"):
                continue
            chain  = line[21]
            resseq = int(line[22:26].strip())
            resname = line[17:20].strip()
            name   = line[12:16].strip()
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            atoms.append((chain, resname, resseq, name, np.array([x, y, z])))
    return atoms

def surface_lys(pdb_path, cutoff=20.0):
    """
    For each LYS in chain A (ERα), find minimum distance from NZ to any
    chain B (CRBN) heavy atom. Return list of (resseq, min_dist) sorted by dist.
    """
    atoms = parse_pdb_atoms(pdb_path)
    # chain B heavy atoms (CRBN)
    crbn_xyz = np.array([a[4] for a in atoms if a[0]=="B" and a[3][0] != "H"])
    
    results = []
    # group LYS NZ atoms in chain A
    lys_nz = [(a[2], a[4]) for a in atoms if a[0]=="A" and a[1]=="LYS" and a[3]=="NZ"]
    for resseq, xyz in lys_nz:
        dists = np.linalg.norm(crbn_xyz - xyz, axis=1)
        results.append((resseq, float(dists.min())))
    results.sort(key=lambda x: x[1])
    return [(r, d) for r, d in results if d <= cutoff]

# Run on all 10 compounds
print("=== SURFACE LYSINES PRESENTED TO CRBN (chain A LYS NZ ≤ 20 Å from any CRBN heavy atom) ===")
print()
lys_summary = {}
for cmpd in [f"ARV_{i:03d}" for i in range(1, 11)]:
    pred = f"{SESSION}/{cmpd}/boltz_results_{cmpd}_constrained/predictions/{cmpd}_constrained"
    pdb = f"{pred}/{cmpd}_constrained_model_0.pdb"
    hits = surface_lys(pdb, cutoff=20.0)
    lys_summary[cmpd] = hits
    lig_crbn = scores[cmpd][0]["lig_crbn"]
    hit_str = ", ".join(f"K{r}({d:.1f}Å)" for r, d in hits[:6]) if hits else "none"
    print(f"  {cmpd}  lig→CRBN={lig_crbn:.4f}  surface LYS: {hit_str}")
    if len(hits) > 6:
        print(f"         ... +{len(hits)-6} more")

print()
print("=== CLOSEST LYS ACROSS ALL COMPOUNDS ===")
all_hits = []
for cmpd, hits in lys_summary.items():
    for r, d in hits:
        all_hits.append((cmpd, r, d))
all_hits.sort(key=lambda x: x[2])
for cmpd, r, d in all_hits[:15]:
    print(f"  {cmpd}  K{r}  {d:.2f} Å")
