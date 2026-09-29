
# Extract SEQRES sequences for BD1 (3MXF A) and BD2 (5T35 A)
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
print(f"BD1 seq ({len(bd1_seq)} aa): {bd1_seq}")
print(f"BD2 seq ({len(bd2_seq)} aa): {bd2_seq}")

# Simple global alignment (Needleman-Wunsch with BLOSUM62-like match/mismatch)
# Using a minimal implementation
def nw_align(s1, s2, match=2, mismatch=-1, gap=-2):
    m, n = len(s1), len(s2)
    dp = np.zeros((m+1, n+1))
    for i in range(m+1): dp[i,0] = i * gap
    for j in range(n+1): dp[0,j] = j * gap
    for i in range(1,m+1):
        for j in range(1,n+1):
            sc = match if s1[i-1]==s2[j-1] else mismatch
            dp[i,j] = max(dp[i-1,j-1]+sc, dp[i-1,j]+gap, dp[i,j-1]+gap)
    # traceback
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
print(f"\nAlignment:")
print(f"BD1: {a1}")
print(f"BD2: {a2}")
matches = sum(c1==c2 and c1!='-' for c1,c2 in zip(a1,a2))
print(f"Identity: {matches}/{len([c for c in a1 if c!='-' and a2[a1.index(c)] != '-'])} ... "
      f"{100*matches/max(len(bd1_seq),len(bd2_seq)):.0f}%")
