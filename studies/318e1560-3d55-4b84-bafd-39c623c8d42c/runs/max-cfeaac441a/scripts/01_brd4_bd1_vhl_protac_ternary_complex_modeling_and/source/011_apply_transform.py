
def apply_transform(c,R,t): return c@R.T+t

# Read all JQ1 atoms from 3MXF
def read_hetatm_ligand(path, chain_id, resname_filter=None):
    atoms = []
    with open(path) as f:
        for line in f:
            if line[:6].strip()=="HETATM" and line[21]==chain_id:
                rn=line[17:20].strip()
                if resname_filter and rn!=resname_filter: continue
                name=line[12:16].strip(); resnum=int(line[22:26])
                x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                atoms.append((name,resnum,rn,np.array([x,y,z])))
    return atoms

def read_ca_chain(path, chain_id):
    coords=[]
    seen=set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn=int(line[22:26])
                if rn not in seen:
                    seen.add(rn); x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                    coords.append(np.array([x,y,z]))
    return np.array(coords)

jq1_atoms  = read_hetatm_ligand(pdb3,'A','JQ1')
mz1_atoms  = read_hetatm_ligand(pdb5,'D','759')

# Transform JQ1 into ternary (BD2/VHL) frame using the sequence-derived Kabsch transform
jq1_coords = np.array([a[3] for a in jq1_atoms])
jq1_tf     = apply_transform(jq1_coords, Rf, tf)

# Centroid of transformed JQ1 (BD1 warhead position in ternary frame)
jq1_cen = jq1_tf.mean(axis=0)

# MZ1 atoms — split by proximity to BD2 (chain A) vs VHL (chain D)
bd2_ca  = read_ca_chain(pdb5,'A')
vhl_ca  = read_ca_chain(pdb5,'D')
bd2_cen = bd2_ca.mean(axis=0)
vhl_cen = vhl_ca.mean(axis=0)

mz1_coords = np.array([a[3] for a in mz1_atoms])
mz1_names  = [a[0] for a in mz1_atoms]

dist_bd2 = np.linalg.norm(mz1_coords - bd2_cen, axis=1)
dist_vhl = np.linalg.norm(mz1_coords - vhl_cen, axis=1)
is_bd_side  = dist_bd2 < dist_vhl

bd_side_atoms  = mz1_coords[is_bd_side]
vhl_side_atoms = mz1_coords[~is_bd_side]
print(f"MZ1 partition: {is_bd_side.sum()} atoms BD-side, {(~is_bd_side).sum()} atoms VHL-side")

bd_exit   = bd_side_atoms.mean(axis=0)    # BD2 warhead centre in 5T35 frame
vhl_exit  = vhl_side_atoms.mean(axis=0)  # VHL warhead centre in 5T35 frame

# Distance from JQ1(BD1, transformed) centroid to VHL warhead centroid
d_jq1_to_vhl = np.linalg.norm(jq1_cen - vhl_exit)
d_bd2_to_vhl = np.linalg.norm(bd_exit  - vhl_exit)

print(f"\nBD2 warhead (MZ1) centroid:       {bd_exit}")
print(f"VHL warhead (MZ1) centroid:       {vhl_exit}")
print(f"JQ1 (BD1 transformed) centroid:   {jq1_cen}")
print(f"\nBD2→VHL warhead distance (MZ1):   {d_bd2_to_vhl:.1f} Å  (reference from 5T35)")
print(f"BD1→VHL warhead distance (model): {d_jq1_to_vhl:.1f} Å  (BD1 superposed onto BD2)")
