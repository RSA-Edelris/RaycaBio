
# Build interaction statistics table
from collections import defaultdict

hbond_counts  = defaultdict(int)   # resid -> number of ligands making H-bond
hydro_counts  = defaultdict(int)   # resid -> number of ligands making hydrophobic contact

for lig, idata in interactions.items():
    for resid in idata['hbonds']:
        hbond_counts[resid] += 1
    for resid in idata['hydrophobic']:
        hydro_counts[resid] += 1

N = 6  # total ligands

print("=== H-BOND STATISTICS (sorted by frequency) ===")
print(f"{'Residue':14s} {'Atom(s)':20s} {'Count':>6} {'Freq':>6}")
print('-'*55)
# Collect atom names per residue
hbond_atoms = defaultdict(set)
for lig, idata in interactions.items():
    for resid, pairs in idata['hbonds'].items():
        for d, an in pairs:
            hbond_atoms[resid].add(an)

for resid, cnt in sorted(hbond_counts.items(), key=lambda x: -x[1]):
    atoms = ', '.join(sorted(hbond_atoms[resid]))
    print(f"{resid:14s} {atoms:20s} {cnt:>6}  {cnt/N*100:>5.0f}%")

print("\n=== HYDROPHOBIC CONTACT STATISTICS ===")
print(f"{'Residue':14s} {'Count':>6} {'Freq':>6}")
print('-'*35)
for resid, cnt in sorted(hydro_counts.items(), key=lambda x: -x[1]):
    print(f"{resid:14s} {cnt:>6}  {cnt/N*100:>5.0f}%")
