
def apply_transform(c,R,t): return c@R.T+t

# ── Identify MZ1 exit atoms (the atoms at the warhead–linker junctions) ──
# Strategy: for each MZ1 atom, compute min dist to BD2 Cα and to VHL Cα.
# "Linker" atoms are far from both chains. 
# BD-side exit = BD-side atom farthest from BD2 chain centroid (most solvent-exposed)
# VHL-side exit = VHL-side atom farthest from VHL chain centroid

# Read CA chains
def read_ca_chain(path, chain_id):
    c=[]; seen=set()
    with open(path) as f:
        for line in f:
            if line[:4]=="ATOM" and line[21]==chain_id and line[12:16].strip()=="CA":
                rn=int(line[22:26])
                if rn not in seen:
                    seen.add(rn); x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                    c.append(np.array([x,y,z]))
    return np.array(c)

bd2_ca_arr = read_ca_chain(pdb5,'A')
vhl_ca_arr = read_ca_chain(pdb5,'D')

# For each MZ1 atom: min distance to BD2 and to VHL CA sets
def min_dist_to_chain(atom_coords, chain_ca):
    diffs = chain_ca - atom_coords  # (N,3)
    return float(np.min(np.linalg.norm(diffs,axis=1)))

mz1_bd_dists  = np.array([min_dist_to_chain(a[3], bd2_ca_arr) for a in mz1_atoms])
mz1_vhl_dists = np.array([min_dist_to_chain(a[3], vhl_ca_arr) for a in mz1_atoms])

# Linker atoms: far from both (both distances > threshold)
thr = 8.0
linker_mask = (mz1_bd_dists > thr) & (mz1_vhl_dists > thr)
print(f"MZ1 atoms far from both chains (>8Å): {linker_mask.sum()}")

# BD-side exit: BD-side atoms (dist_bd2 < dist_vhl) with max dist to BD2
bd_side_mask = mz1_bd_dists < mz1_vhl_dists
bd_exit_idx  = np.argmax(np.where(bd_side_mask, mz1_bd_dists, -99))
vhl_exit_idx = np.argmax(np.where(~bd_side_mask, mz1_vhl_dists, -99))

bd_exit_atom  = mz1_atoms[bd_exit_idx]
vhl_exit_atom = mz1_atoms[vhl_exit_idx]
print(f"\nBD-side exit atom:  {bd_exit_atom[0]:4s}  dist_to_BD2={mz1_bd_dists[bd_exit_idx]:.1f} Å  "
      f"coords={bd_exit_atom[3]}")
print(f"VHL-side exit atom: {vhl_exit_atom[0]:4s} dist_to_VHL={mz1_vhl_dists[vhl_exit_idx]:.1f} Å  "
      f"coords={vhl_exit_atom[3]}")

bd_exit_xyz  = bd_exit_atom[3]
vhl_exit_xyz = vhl_exit_atom[3]
mz1_bridge   = np.linalg.norm(bd_exit_xyz - vhl_exit_xyz)
print(f"\nMZ1 exit-to-exit bridging distance: {mz1_bridge:.1f} Å  (reference)")

# JQ1 exit atom: in BD1 frame = atom most solvent-exposed (farthest from BD1 CA centroid)
def read_hetatm_ligand(path, chain_id, resname_filter=None):
    atoms=[]
    with open(path) as f:
        for line in f:
            if line[:6].strip()=="HETATM" and line[21]==chain_id:
                rn=line[17:20].strip()
                if resname_filter and rn!=resname_filter: continue
                name=line[12:16].strip(); resnum=int(line[22:26])
                x,y,z=float(line[30:38]),float(line[38:46]),float(line[46:54])
                atoms.append((name,resnum,rn,np.array([x,y,z])))
    return atoms

bd1_ca_arr = read_ca_chain(pdb3,'A')
bd1_ca_cen = bd1_ca_arr.mean(axis=0)
jq1_atoms  = read_hetatm_ligand(pdb3,'A','JQ1')
jq1_to_bd1 = np.array([np.linalg.norm(a[3]-bd1_ca_cen) for a in jq1_atoms])
jq1_exit_idx = np.argmax(jq1_to_bd1)
jq1_exit_atom = jq1_atoms[jq1_exit_idx]
print(f"\nJQ1 exit atom (BD1 frame): {jq1_exit_atom[0]:4s}  dist_to_BD1_cen="
      f"{jq1_to_bd1[jq1_exit_idx]:.1f} Å  coords={jq1_exit_atom[3]}")

# Transform JQ1 exit atom to ternary frame
jq1_exit_tf = apply_transform(jq1_exit_atom[3].reshape(1,3), Rf, tf)[0]
bd1_exit_to_vhl_exit = np.linalg.norm(jq1_exit_tf - vhl_exit_xyz)
print(f"\nBD1 JQ1-exit → VHL-exit distance (model): {bd1_exit_to_vhl_exit:.1f} Å")
print(f"BD2 MZ1-exit → VHL-exit distance (crystal): {mz1_bridge:.1f} Å")
