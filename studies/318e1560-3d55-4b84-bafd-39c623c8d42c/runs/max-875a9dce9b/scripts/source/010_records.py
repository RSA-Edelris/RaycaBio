
three_to_one = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
    'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
    'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V','MSE':'M'
}

# Build SEQRES→PDB resnum mapping using ATOM CA records (ordered)
def seqres_to_pdb_map(pdb_path, chain_id, seqres_seq):
    """Map SEQRES positions (0-based) to PDB resnums."""
    ca_seq = []   # (resnum, one-letter)
    seen = set()
    with open(pdb_path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn = int(line[22:26])
                resname = line[17:20].strip()
                if rn not in seen:
                    seen.add(rn)
                    ca_seq.append((rn, three_to_one.get(resname,'X')))
    # Find subsequence match of ca_seq residues in seqres_seq
    ca_str = ''.join(r[1] for r in ca_seq)
    # Find start offset of ca_str in seqres_seq (allowing mismatches for MSE etc.)
    best_start, best_score = 0, 0
    for start in range(len(seqres_seq) - len(ca_str) + 1):
        score = sum(a==b for a,b in zip(ca_str, seqres_seq[start:]))
        if score > best_score:
            best_score = score; best_start = start
    mapping = {}  # seqres_pos → pdb_resnum
    for i, (rn, aa) in enumerate(ca_seq):
        seqres_pos = best_start + i
        mapping[seqres_pos] = rn
    return mapping

bd1_map = seqres_to_pdb_map(pdb3, 'A', bd1_seq)
bd2_map = seqres_to_pdb_map(pdb5, 'A', bd2_seq)
print(f"BD1 map: {len(bd1_map)} SEQRES positions → PDB resnums, "
      f"range {min(bd1_map.values())}-{max(bd1_map.values())}")
print(f"BD2 map: {len(bd2_map)} SEQRES positions → PDB resnums, "
      f"range {min(bd2_map.values())}-{max(bd2_map.values())}")

# Parse alignment to get paired SEQRES positions
pos1 = pos2 = 0
paired_seqres = []   # (seqres_pos_bd1, seqres_pos_bd2)
for c1, c2 in zip(a1, a2):
    if c1 != '-' and c2 != '-':
        paired_seqres.append((pos1, pos2))
    if c1 != '-': pos1 += 1
    if c2 != '-': pos2 += 1

# Keep only pairs where both have CA coordinates
def kabsch(mobile, target):
    mob_c=mobile.mean(0); tgt_c=target.mean(0)
    H=(mobile-mob_c).T@(target-tgt_c)
    U,S,Vt=np.linalg.svd(H)
    d=np.linalg.det(Vt.T@U.T)
    R=Vt.T@np.diag([1,1,d])@U.T
    return R, tgt_c-mob_c@R.T

def apply_transform(c,R,t): return c@R.T+t
def rmsd_fn(a,b): return float(np.sqrt(np.mean(np.sum((a-b)**2,axis=1))))

valid_pairs = [(p1,p2) for p1,p2 in paired_seqres
               if p1 in bd1_map and p2 in bd2_map]
mobile_aln = np.array([bd1_ca[bd1_map[p1]] for p1,p2 in valid_pairs])
target_aln = np.array([bd2_ca[bd2_map[p2]] for p1,p2 in valid_pairs])

R_aln, t_aln = kabsch(mobile_aln, target_aln)
fit_aln = apply_transform(mobile_aln, R_aln, t_aln)
print(f"\nSequence-aligned pairs: {len(valid_pairs)}")
print(f"Initial RMSD: {rmsd_fn(fit_aln, target_aln):.2f} Å")

# Iterative core trimming
pm, pt = mobile_aln.copy(), target_aln.copy()
for i in range(10):
    Ri,ti = kabsch(pm,pt); fi=apply_transform(pm,Ri,ti)
    dists=np.sqrt(np.sum((fi-pt)**2,axis=1))
    keep=dists<=dists.mean()+2*dists.std()
    if keep.all(): break
    pm,pt = pm[keep],pt[keep]
Rf,tf = kabsch(pm,pt); ff=apply_transform(pm,Rf,tf)
print(f"Core RMSD: {rmsd_fn(ff,pt):.2f} Å over {len(pm)} residues")
