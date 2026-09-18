
# Water analysis: bridging, conserved-candidate vs displaceable

import math
from collections import defaultdict

PROBE_R = 1.4
VDW_R = {"C":1.7,"N":1.55,"O":1.52,"S":1.8,"ZN":1.39,"H":1.1}
SPHERE_N = 92

def dist(a,b):
    return math.sqrt((a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2)

def element(n):
    for c in n:
        if c.isalpha(): return c.upper()
    return "C"

def parse_all(path, chains=None, include_water=True):
    atoms=[]
    with open(path) as f:
        for line in f:
            rec=line[:6].strip()
            if rec not in ("ATOM","HETATM"): continue
            ch=line[21]
            if chains and ch not in chains: continue
            alt=line[16].strip()
            if alt and alt not in ('','A',' '): continue
            resn=line[17:20].strip()
            if not include_water and resn in ("HOH","WAT"): continue
            try:
                atoms.append({"rec":rec,"name":line[12:16].strip(),
                    "resn":resn,"chain":ch,"resi":int(line[22:26]),
                    "x":float(line[30:38]),"y":float(line[38:46]),"z":float(line[46:54]),
                    "occ":float(line[54:60]),"bfac":float(line[60:66])})
            except: pass
    return atoms

def sphere_points(n=SPHERE_N):
    pts=[]; inc=math.pi*(3-math.sqrt(5)); off=2.0/n
    for k in range(n):
        y=k*off-1+(off/2); r=math.sqrt(max(0,1-y*y)); phi=k*inc
        pts.append((math.cos(phi)*r, y, math.sin(phi)*r))
    return pts
SPHERE=sphere_points()

def burial_fraction(wat, context, probe=1.4, r_wat=1.52):
    """Fraction of probe sphere around water O buried by context atoms."""
    ri=r_wat+probe; buried_count=0
    for sp in SPHERE:
        px=wat["x"]+ri*sp[0]; py=wat["y"]+ri*sp[1]; pz=wat["z"]+ri*sp[2]
        for ca in context:
            if ca is wat: continue
            rj=VDW_R.get(element(ca["name"]),1.7)+probe
            dx=px-ca["x"]; dy=py-ca["y"]; dz=pz-ca["z"]
            if dx*dx+dy*dy+dz*dz<rj*rj:
                buried_count+=1; break
    return buried_count/len(SPHERE)

def analyse_waters(path, lig_chains, prot1_chains, prot2_chains, cutoff=3.5):
    lig   = [a for a in parse_all(path, lig_chains)   if a["resn"] not in ("HOH","WAT")]
    prot1 = [a for a in parse_all(path, prot1_chains) if a["resn"] not in ("HOH","WAT")]
    prot2 = [a for a in parse_all(path, prot2_chains) if a["resn"] not in ("HOH","WAT")]
    all_nw= lig+prot1+prot2
    waters= [a for a in parse_all(path, prot1_chains+prot2_chains+lig_chains)
             if a["resn"] in ("HOH","WAT") and a["name"]=="O"]
    
    results=[]
    for w in waters:
        near_lig  = [a for a in lig   if dist(w,a)<=cutoff and element(a["name"])!="H"]
        near_p1   = [a for a in prot1 if dist(w,a)<=cutoff and element(a["name"])!="H"]
        near_p2   = [a for a in prot2 if dist(w,a)<=cutoff and element(a["name"])!="H"]
        if not (near_lig or near_p1 or near_p2): continue
        bf = burial_fraction(w, [x for x in all_nw if dist(w,x)<8.0])
        bridges_lig_p1 = bool(near_lig and near_p1)
        bridges_lig_p2 = bool(near_lig and near_p2)
        bridges_p1_p2  = bool(near_p1 and near_p2)
        # Conserved candidate: high burial (>60%), low B-factor (<50), bridges proteins
        conserved = (bf>0.60 and w["bfac"]<60 and (bridges_lig_p1 or bridges_p1_p2 or bridges_lig_p2))
        displace  = (bf<0.50 or w["bfac"]>60)
        results.append({
            "chain":w["chain"],"resi":w["resi"],"bfac":w["bfac"],"occ":w["occ"],
            "burial":bf,"near_lig":[(a["resn"],a["name"]) for a in near_lig[:3]],
            "near_p1":[(a["resn"],a["resi"],a["name"]) for a in near_p1[:3]],
            "near_p2":[(a["resn"],a["resi"],a["name"]) for a in near_p2[:3]],
            "bridges_lig_p1":bridges_lig_p1,"bridges_lig_p2":bridges_lig_p2,
            "bridges_p1_p2":bridges_p1_p2,"conserved":conserved,"displaceable":displace,
        })
    return results

print("=== 6H0F: waters near pomalidomide/CRBN/IKZF1 ===")
w6 = analyse_waters(p6h0f, ["B"], ["B"], ["C"])
for w in sorted(w6, key=lambda x:-x["burial"]):
    status = "CONSERVED" if w["conserved"] else ("DISPLACEABLE" if w["displaceable"] else "uncertain")
    bridge = []
    if w["bridges_lig_p1"]: bridge.append("lig↔CRBN")
    if w["bridges_lig_p2"]: bridge.append("lig↔IKZF1")
    if w["bridges_p1_p2"]:  bridge.append("CRBN↔IKZF1")
    print(f"  HOH {w['chain']}{w['resi']:>4}  B={w['bfac']:.1f}  burial={w['burial']:.2f}  "
          f"{status}  bridges={bridge or 'none'}  "
          f"p1:[{','.join(f'{r}{i}:{n}' for r,i,n in w['near_p1'][:2])}]  "
          f"p2:[{','.join(f'{r}{i}:{n}' for r,i,n in w['near_p2'][:2])}]")

print(f"\n=== 2O98: waters near fusicoccin/14-3-3/ATPase ===")
w2 = analyse_waters(p2o98, ["A"], ["A"], ["P"])
for w in sorted(w2, key=lambda x:-x["burial"]):
    status = "CONSERVED" if w["conserved"] else ("DISPLACEABLE" if w["displaceable"] else "uncertain")
    bridge = []
    if w["bridges_lig_p1"]: bridge.append("lig↔14-3-3")
    if w["bridges_lig_p2"]: bridge.append("lig↔ATPase")
    if w["bridges_p1_p2"]:  bridge.append("14-3-3↔ATPase")
    print(f"  HOH {w['chain']}{w['resi']:>4}  B={w['bfac']:.1f}  burial={w['burial']:.2f}  "
          f"{status}  bridges={bridge or 'none'}  "
          f"p1:[{','.join(f'{r}{i}:{n}' for r,i,n in w['near_p1'][:2])}]  "
          f"p2:[{','.join(f'{r}{i}:{n}' for r,i,n in w['near_p2'][:2])}]")
