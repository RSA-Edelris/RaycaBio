
import numpy as np
import pathlib

session_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb")
work_dir = session_dir / "brd4_vhl_protac"
pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

def read_ca_coords(path, chain_id):
    coords = {}
    with open(path) as f:
        for line in f:
            if line[:4] == "ATOM" and line[21] == chain_id and line[12:16].strip() == "CA":
                resnum = int(line[22:26])
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords[resnum] = np.array([x, y, z])
    return coords

def kabsch(mobile, target):
    mob_c = mobile.mean(axis=0); tgt_c = target.mean(axis=0)
    mob_ = mobile - mob_c; tgt_ = target - tgt_c
    H = mob_.T @ tgt_
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = tgt_c - mob_c @ R.T
    return R, t

def apply_transform(coords_arr, R, t):
    return coords_arr @ R.T + t

def rmsd_fn(a, b):
    return float(np.sqrt(np.mean(np.sum((a - b)**2, axis=1))))

# Script 009: extract SEQRES and align
three_to_one = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
    'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
    'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V','MSE':'M'
}

def get_seqres(path, chain_id):
    seq = []
    with open(path) as f:
        for line in f:
            if line[:6] == "SEQRES" and line[11] == chain_id:
                seq.extend(line[19:].split())
    return ''.join(three_to_one.get(r, 'X') for r in seq)

bd1_seq = get_seqres(pdb3, 'A')
bd2_seq = get_seqres(pdb5, 'A')
print(f"BD1 SEQRES: {len(bd1_seq)} aa")
print(f"BD2 SEQRES: {len(bd2_seq)} aa")

def nw_align(s1, s2, match=2, mismatch=-1, gap=-2):
    m, n = len(s1), len(s2)
    dp = np.zeros((m+1, n+1))
    for i in range(m+1): dp[i,0] = i * gap
    for j in range(n+1): dp[0,j] = j * gap
    for i in range(1,m+1):
        for j in range(1,n+1):
            sc = match if s1[i-1]==s2[j-1] else mismatch
            dp[i,j] = max(dp[i-1,j-1]+sc, dp[i-1,j]+gap, dp[i,j-1]+gap)
    a1, a2 = [], []
    i, j = m, n
    while i>0 or j>0:
        if i>0 and j>0:
            sc = match if s1[i-1]==s2[j-1] else mismatch
            if dp[i,j] == dp[i-1,j-1]+sc:
                a1.append(s1[i-1]); a2.append(s2[j-1]); i-=1; j-=1; continue
        if i>0 and dp[i,j] == dp[i-1,j]+gap:
            a1.append(s1[i-1]); a2.append('-'); i-=1
        else:
            a1.append('-'); a2.append(s2[j-1]); j-=1
    return ''.join(reversed(a1)), ''.join(reversed(a2))

a1, a2 = nw_align(bd1_seq, bd2_seq)
matches = sum(c1==c2 and c1!='-' for c1,c2 in zip(a1,a2))
print(f"Alignment: BD1={len(bd1_seq)}, BD2={len(bd2_seq)}, matches={matches}")

# Script 010: seqres->pdb mapping + kabsch
bd1_ca = read_ca_coords(pdb3, 'A')
bd2_ca = read_ca_coords(pdb5, 'A')

def seqres_to_pdb_map(pdb_path, chain_id, seqres_seq):
    ca_seq = []
    seen = set()
    with open(pdb_path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn = int(line[22:26])
                resname = line[17:20].strip()
                if rn not in seen:
                    seen.add(rn)
                    ca_seq.append((rn, three_to_one.get(resname,'X')))
    ca_str = ''.join(r[1] for r in ca_seq)
    best_start, best_score = 0, 0
    for start in range(len(seqres_seq) - len(ca_str) + 1):
        score = sum(a==b for a,b in zip(ca_str, seqres_seq[start:]))
        if score > best_score:
            best_score = score; best_start = start
    mapping = {}
    for i, (rn, aa) in enumerate(ca_seq):
        seqres_pos = best_start + i
        mapping[seqres_pos] = rn
    return mapping

bd1_map = seqres_to_pdb_map(pdb3, 'A', bd1_seq)
bd2_map = seqres_to_pdb_map(pdb5, 'A', bd2_seq)
print(f"BD1 map range: {min(bd1_map.values())}-{max(bd1_map.values())} ({len(bd1_map)} residues)")
print(f"BD2 map range: {min(bd2_map.values())}-{max(bd2_map.values())} ({len(bd2_map)} residues)")

# parse aligned positions
pos1 = pos2 = 0
paired_seqres = []
for c1, c2 in zip(a1, a2):
    if c1 != '-' and c2 != '-':
        paired_seqres.append((pos1, pos2))
    if c1 != '-': pos1 += 1
    if c2 != '-': pos2 += 1

valid_pairs = [(p1,p2) for p1,p2 in paired_seqres if p1 in bd1_map and p2 in bd2_map]
mobile_aln = np.array([bd1_ca[bd1_map[p1]] for p1,p2 in valid_pairs])
target_aln = np.array([bd2_ca[bd2_map[p2]] for p1,p2 in valid_pairs])
print(f"\nSequence-aligned valid pairs: {len(valid_pairs)}")

R_aln, t_aln = kabsch(mobile_aln, target_aln)
fit_aln = apply_transform(mobile_aln, R_aln, t_aln)
print(f"Initial RMSD over all aligned pairs: {rmsd_fn(fit_aln, target_aln):.2f} Å")

pm, pt = mobile_aln.copy(), target_aln.copy()
for i in range(10):
    Ri, ti = kabsch(pm, pt)
    fi = apply_transform(pm, Ri, ti)
    dists = np.sqrt(np.sum((fi-pt)**2, axis=1))
    keep = dists <= dists.mean() + 2*dists.std()
    if keep.all(): break
    pm, pt = pm[keep], pt[keep]
Rf, tf = kabsch(pm, pt)
ff = apply_transform(pm, Rf, tf)
core_rmsd = rmsd_fn(ff, pt)
print(f"Core RMSD after iterative trim: {core_rmsd:.2f} Å over {len(pm)} residues")
