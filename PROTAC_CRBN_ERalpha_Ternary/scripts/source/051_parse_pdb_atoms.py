
import numpy as np

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

pdb_path = (f"{SESSION}/ARV_001/boltz_results_ARV_001_constrained/"
            f"predictions/ARV_001_constrained/ARV_001_constrained_model_0.pdb")
atoms = parse_pdb_atoms(pdb_path)

# K233 NZ in chain A
k233_nz = [a[4] for a in atoms if a[0]=='A' and a[2]==233 and a[3]=='NZ'][0]
print(f"K233 NZ xyz: {k233_nz}")

# Closest 5 chain-B heavy atoms
crbn_atoms = [(a[1], a[2], a[3], a[4]) for a in atoms if a[0]=='B']
dists = [(rn, rs, nm, np.linalg.norm(xyz - k233_nz)) for rn,rs,nm,xyz in crbn_atoms]
dists.sort(key=lambda x: x[3])
print("\n5 closest CRBN heavy atoms to K233 NZ:")
for rn,rs,nm,d in dists[:5]:
    print(f"  CRBN {rn}{rs} {nm:4s}  {d:.3f} Å")

# Check: are there ANY sub-2 Å contacts at the A-B interface?
crbn_xyz = np.array([a[4] for a in atoms if a[0]=='B'])
era_xyz  = np.array([a[4] for a in atoms if a[0]=='A'])
from scipy.spatial.distance import cdist
dm = cdist(era_xyz, crbn_xyz)
clash_mask = dm < 2.0
n_clashes = clash_mask.sum()
print(f"\nTotal chain-A/chain-B atom pairs < 2.0 Å: {n_clashes}")
print(f"Min A-B distance overall: {dm.min():.3f} Å")

# Distribution of A-B interface contacts
print("A-B distance histogram:")
for threshold in [2.0, 3.0, 3.5, 4.0, 5.0]:
    print(f"  < {threshold} Å : {(dm < threshold).sum()} pairs")
