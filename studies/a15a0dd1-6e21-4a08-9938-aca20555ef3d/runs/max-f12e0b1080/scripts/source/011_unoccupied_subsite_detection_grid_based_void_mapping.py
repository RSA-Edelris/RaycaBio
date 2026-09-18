
# Unoccupied subsite detection: grid-based void mapping around the ligand

import math, json
from collections import defaultdict

def dist(a,b):
    return math.sqrt((a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2)

def element(n):
    for c in n:
        if c.isalpha(): return c.upper()
    return "C"

def parse_chain(path, chain, recs=("ATOM","HETATM")):
    atoms=[]
    with open(path) as f:
        for line in f:
            rec=line[:6].strip()
            if rec not in recs: continue
            if line[21]!=chain: continue
            alt=line[16].strip()
            if alt and alt not in ('','A',' '): continue
            try:
                atoms.append({"rec":rec,"name":line[12:16].strip(),
                    "resn":line[17:20].strip(),"chain":line[21],
                    "resi":int(line[22:26]),
                    "x":float(line[30:38]),"y":float(line[38:46]),"z":float(line[46:54]),
                    "occ":float(line[54:60]),"bfac":float(line[60:66])})
            except: pass
    return atoms

VDW_R={"C":1.7,"N":1.55,"O":1.52,"S":1.8,"ZN":1.39,"H":1.1}

def subsite_voids(lig_atoms, prot_atoms, step=0.8, probe=1.2, shell_lo=2.5, shell_hi=5.5):
    """
    Scan a grid around the ligand centroid.
    A grid point is a 'void' if:
      - no ligand heavy atom within shell_lo (so it's not already occupied)
      - at least one protein atom within shell_hi (so it's in the pocket)
      - no protein heavy atom within probe (not clashing with protein)
    Returns void points with nearest protein residue info.
    """
    heavy_lig = [a for a in lig_atoms  if element(a["name"])!="H"]
    heavy_pro = [a for a in prot_atoms if element(a["name"])!="H" and a["resn"] not in ("HOH","WAT")]
    
    cx = sum(a["x"] for a in heavy_lig)/len(heavy_lig)
    cy = sum(a["y"] for a in heavy_lig)/len(heavy_lig)
    cz = sum(a["z"] for a in heavy_lig)/len(heavy_lig)
    
    R = 6.0  # search radius around centroid
    voids = []
    xs = [cx+dx for dx in [i*step for i in range(-int(R/step),int(R/step)+1)]]
    ys = [cy+dy for dy in [i*step for i in range(-int(R/step),int(R/step)+1)]]
    zs = [cz+dz for dz in [i*step for i in range(-int(R/step),int(R/step)+1)]]
    
    for x in xs:
        for y in ys:
            for z in zs:
                pt = {"x":x,"y":y,"z":z}
                # distance from centroid
                dc = math.sqrt((x-cx)**2+(y-cy)**2+(z-cz)**2)
                if dc > R: continue
                # check not occupied by ligand
                min_lig = min((dist(pt,a) for a in heavy_lig), default=999)
                if min_lig < shell_lo: continue
                # check near protein
                near_prot = [(dist(pt,a),a) for a in heavy_pro if dist(pt,a)<shell_hi]
                if not near_prot: continue
                # check no clash with protein
                if any(d<probe for d,_ in near_prot): continue
                # cluster to nearest protein residue
                near_prot.sort(key=lambda x:x[0])
                nearest = near_prot[0][1]
                voids.append({
                    "x":x,"y":y,"z":z,"dc":dc,
                    "min_lig":min_lig,"min_prot":near_prot[0][0],
                    "nearest_res":f"{nearest['resn']}{nearest['resi']}",
                    "nearest_chain":nearest["chain"],
                    # vector from lig centroid to void
                    "vx":(x-cx)/dc if dc>0 else 0,
                    "vy":(y-cy)/dc if dc>0 else 0,
                    "vz":(z-cz)/dc if dc>0 else 0,
                })
    return voids, (cx,cy,cz)

def cluster_voids(voids, r=1.5):
    """Simple greedy clustering of void points."""
    clusters=[]
    used=set()
    for i,v in enumerate(voids):
        if i in used: continue
        members=[v]
        used.add(i)
        for j,w in enumerate(voids):
            if j in used: continue
            if math.sqrt((v["x"]-w["x"])**2+(v["y"]-w["y"])**2+(v["z"]-w["z"])**2)<r:
                members.append(w); used.add(j)
        # centroid
        mx=sum(m["x"] for m in members)/len(members)
        my=sum(m["y"] for m in members)/len(members)
        mz=sum(m["z"] for m in members)/len(members)
        # dominant residues
        res_count=defaultdict(int)
        for m in members: res_count[f"{m['nearest_chain']}:{m['nearest_res']}"]+=1
        top_res=sorted(res_count.items(),key=lambda x:-x[1])[:3]
        # mean vector
        vx=sum(m["vx"] for m in members)/len(members)
        vy=sum(m["vy"] for m in members)/len(members)
        vz=sum(m["vz"] for m in members)/len(members)
        vmag=math.sqrt(vx**2+vy**2+vz**2)
        clusters.append({"n_pts":len(members),"cx":mx,"cy":my,"cz":mz,
                         "top_residues":top_res,"vx":vx/vmag,"vy":vy/vmag,"vz":vz/vmag,
                         "vol_est":len(members)*0.8**3})
    clusters.sort(key=lambda x:-x["n_pts"])
    return clusters

# ── 6H0F ──
lig_6   = [a for a in parse_chain(p6h0f,"B",("HETATM",)) if a["resn"]=="Y70"]
crbn_B  = parse_chain(p6h0f,"B",("ATOM",))
ikzf_C  = parse_chain(p6h0f,"C",("ATOM",))

print("Computing voids for 6H0F...")
v6,cent6 = subsite_voids(lig_6, crbn_B+ikzf_C)
c6 = cluster_voids(v6)
print(f"  Ligand centroid: ({cent6[0]:.1f}, {cent6[1]:.1f}, {cent6[2]:.1f})")
print(f"  Total void points: {len(v6)}  →  {len(c6)} clusters")
for i,cl in enumerate(c6[:6]):
    print(f"  Subsite {i+1}: vol≈{cl['vol_est']:.0f}Å³  "
          f"near [{', '.join(r for r,n in cl['top_residues'][:2])}]  "
          f"vector=({cl['vx']:+.2f},{cl['vy']:+.2f},{cl['vz']:+.2f})")

# ── 2O98 ──
fsc_A2  = [a for a in parse_chain(p2o98,"A",("HETATM",)) if a["resn"]=="FSC"]
p14_A2  = parse_chain(p2o98,"A",("ATOM",))
atp_P2  = parse_chain(p2o98,"P",("ATOM",))

print("\nComputing voids for 2O98...")
v2,cent2 = subsite_voids(fsc_A2, p14_A2+atp_P2)
c2 = cluster_voids(v2)
print(f"  Ligand centroid: ({cent2[0]:.1f}, {cent2[1]:.1f}, {cent2[2]:.1f})")
print(f"  Total void points: {len(v2)}  →  {len(c2)} clusters")
for i,cl in enumerate(c2[:6]):
    print(f"  Subsite {i+1}: vol≈{cl['vol_est']:.0f}Å³  "
          f"near [{', '.join(r for r,n in cl['top_residues'][:2])}]  "
          f"vector=({cl['vx']:+.2f},{cl['vy']:+.2f},{cl['vz']:+.2f})")
