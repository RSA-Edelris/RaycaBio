
import numpy as np, pathlib

work_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb/brd4_vhl_protac")
pdb3 = work_dir / "3MXF.pdb"
pdb5 = work_dir / "5T35.pdb"

# ── Rebuild the Kabsch transform (Rf, tf) from scratch ──
three_to_one = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
    'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
    'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V','MSE':'M'
}

def read_ca(path, chain):
    coords={}; seen=set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain and line[12:16].strip()=="CA":
                rn=int(line[22:26])
                if rn not in seen:
                    seen.add(rn)
                    coords[rn]=np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])])
    return coords

def get_seqres(path, chain):
    seq=[]
    with open(path) as f:
        for line in f:
            if line[:6]=="SEQRES" and line[11]==chain:
                seq.extend(line[19:].split())
    return ''.join(three_to_one.get(r,'X') for r in seq)

def nw_align(s1, s2, match=2, mismatch=-1, gap=-2):
    m,n=len(s1),len(s2)
    dp=np.zeros((m+1,n+1))
    for i in range(m+1): dp[i,0]=i*gap
    for j in range(n+1): dp[0,j]=j*gap
    for i in range(1,m+1):
        for j in range(1,n+1):
            sc=match if s1[i-1]==s2[j-1] else mismatch
            dp[i,j]=max(dp[i-1,j-1]+sc,dp[i-1,j]+gap,dp[i,j-1]+gap)
    a1,a2=[],[]
    i,j=m,n
    while i>0 or j>0:
        if i>0 and j>0:
            sc=match if s1[i-1]==s2[j-1] else mismatch
            if dp[i,j]==dp[i-1,j-1]+sc:
                a1.append(s1[i-1]); a2.append(s2[j-1]); i-=1; j-=1; continue
        if i>0 and dp[i,j]==dp[i-1,j]+gap:
            a1.append(s1[i-1]); a2.append('-'); i-=1
        else:
            a1.append('-'); a2.append(s2[j-1]); j-=1
    return ''.join(reversed(a1)),''.join(reversed(a2))

def seqres_to_pdb_map(pdb_path, chain_id, seqres_seq):
    ca_seq=[]; seen=set()
    with open(pdb_path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn=int(line[22:26]); resname=line[17:20].strip()
                if rn not in seen:
                    seen.add(rn); ca_seq.append((rn,three_to_one.get(resname,'X')))
    ca_str=''.join(r[1] for r in ca_seq)
    best_start=best_score=0
    for start in range(len(seqres_seq)-len(ca_str)+1):
        score=sum(a==b for a,b in zip(ca_str,seqres_seq[start:]))
        if score>best_score: best_score=score; best_start=start
    return {best_start+i:rn for i,(rn,_) in enumerate(ca_seq)}

def kabsch(mobile, target):
    mc,tc=mobile.mean(0),target.mean(0)
    H=(mobile-mc).T@(target-tc)
    U,S,Vt=np.linalg.svd(H)
    d=np.linalg.det(Vt.T@U.T)
    R=Vt.T@np.diag([1,1,d])@U.T
    return R, tc-mc@R.T

bd1_ca=read_ca(pdb3,'A'); bd2_ca=read_ca(pdb5,'A')
bd1_seq=get_seqres(pdb3,'A'); bd2_seq=get_seqres(pdb5,'A')
a1,a2=nw_align(bd1_seq,bd2_seq)
bd1_map=seqres_to_pdb_map(pdb3,'A',bd1_seq)
bd2_map=seqres_to_pdb_map(pdb5,'A',bd2_seq)

pos1=pos2=0; paired=[]
for c1,c2 in zip(a1,a2):
    if c1!='-' and c2!='-': paired.append((pos1,pos2))
    if c1!='-': pos1+=1
    if c2!='-': pos2+=1
valid=[(p1,p2) for p1,p2 in paired if p1 in bd1_map and p2 in bd2_map]
mob=np.array([bd1_ca[bd1_map[p1]] for p1,p2 in valid])
tgt=np.array([bd2_ca[bd2_map[p2]] for p1,p2 in valid])
pm,pt=mob.copy(),tgt.copy()
for _ in range(10):
    Ri,ti=kabsch(pm,pt); fi=pm@Ri.T+ti
    dists=np.sqrt(np.sum((fi-pt)**2,axis=1)); keep=dists<=dists.mean()+2*dists.std()
    if keep.all(): break
    pm,pt=pm[keep],pt[keep]
Rf,tf=kabsch(pm,pt)
print(f"Transform rebuilt: core RMSD = {np.sqrt(np.mean(np.sum(((pm@Rf.T+tf)-pt)**2,axis=1))):.2f} Å")
