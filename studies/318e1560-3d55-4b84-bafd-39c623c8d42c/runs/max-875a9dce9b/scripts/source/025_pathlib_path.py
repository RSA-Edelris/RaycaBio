
import numpy as np, pathlib
from collections import defaultdict, Counter

session_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb")
work_dir = session_dir / "brd4_vhl_protac"
pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

# ── 1. Identify 5T35 chains from SEQRES ──
print("=== 5T35 SEQRES-based chain identities ===")
seqres = defaultdict(list)
with open(pdb5) as f:
    for line in f:
        if line[:6] == "SEQRES":
            ch = line[11]
            seqres[ch].extend(line[19:].split())

for ch in sorted(seqres):
    n = len(seqres[ch])
    first3 = seqres[ch][:3]
    last3  = seqres[ch][-3:]
    print(f"  chain {ch}: {n} residues  first3={first3} last3={last3}")

# ── 2. Confirm 3MXF chain A residue range ──
print()
def chain_resrange(path, chain_id):
    rns = set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rns.add(int(line[22:26]))
    return min(rns), max(rns), len(rns)

r0, r1, n = chain_resrange(pdb3, 'A')
print(f"3MXF chain A: {n} CA residues, {r0}–{r1}  (expected BD1: 42–168, 127 res)")

for ch in ['A','B','C','D']:
    try:
        r0,r1,n = chain_resrange(pdb5, ch)
        print(f"5T35 chain {ch}: {n} residues, {r0}–{r1}")
    except ValueError:
        print(f"5T35 chain {ch}: no CA atoms")

# ── 3. Verify transform direction: Rf,tf maps BD1→BD2 ──
print()
def apply_transform(c, R, t): return c @ R.T + t

def read_ca_chain(path, chain_id):
    c=[]; seen=set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn=int(line[22:26])
                if rn not in seen:
                    seen.add(rn)
                    c.append([float(line[30:38]),float(line[38:46]),float(line[46:54])])
    return np.array(c)

bd1_ca = read_ca_chain(pdb3, 'A')
bd2_ca = read_ca_chain(pdb5, 'A')
bd1_tf = apply_transform(bd1_ca, Rf, tf)

# After transform, BD1 centroid should be close to BD2 centroid
diff_centroid = np.linalg.norm(bd1_tf.mean(0) - bd2_ca.mean(0))
diff_original = np.linalg.norm(bd1_ca.mean(0)  - bd2_ca.mean(0))
print(f"BD1 centroid distance to BD2 BEFORE transform: {diff_original:.2f} Å")
print(f"BD1 centroid distance to BD2 AFTER  transform: {diff_centroid:.4f} Å  (should be ~0)")

# Applying Rf,tf to BD2 should NOT give a good alignment (wrong direction)
bd2_tf_wrong = apply_transform(bd2_ca, Rf, tf)
diff_wrong = np.linalg.norm(bd2_tf_wrong.mean(0) - bd2_ca.mean(0))
print(f"BD2 centroid distance if Rf applied to BD2 (wrong): {diff_wrong:.2f} Å  (should be large)")
