
# Corrected SASA: compute per-atom areas with full context, then sum only target atoms

import math
from collections import defaultdict

PROBE_R = 1.4
VDW_R = {"C":1.7,"N":1.55,"O":1.52,"S":1.8,"P":1.8,"ZN":1.39,"CL":1.75,"F":1.47,"H":1.1}

def dist(a,b):
    return math.sqrt((a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2)

def element(n):
    for c in n:
        if c.isalpha(): return c.upper()
    return "C"

def _sphere_points(n=92):
    pts=[]; inc=math.pi*(3-math.sqrt(5)); off=2.0/n
    for k in range(n):
        y=k*off-1+(off/2); r=math.sqrt(max(0,1-y*y)); phi=k*inc
        pts.append((math.cos(phi)*r, y, math.sin(phi)*r))
    return pts
SPHERE=_sphere_points(92)

def sasa_masked(context_atoms, target_indices):
    """SASA for target_indices atoms computed in the context of all context_atoms."""
    heavy=[a for a in context_atoms if element(a["name"])!="H"]
    radii=[VDW_R.get(element(a["name"]),1.7)+PROBE_R for a in heavy]
    total=0.0
    for i in target_indices:
        ai,ri=heavy[i],radii[i]
        exposed=0
        for sp in SPHERE:
            px=ai["x"]+ri*sp[0]; py=ai["y"]+ri*sp[1]; pz=ai["z"]+ri*sp[2]
            buried=False
            for j,aj in enumerate(heavy):
                if j==i: continue
                rj=radii[j]
                dx=px-aj["x"]; dy=py-aj["y"]; dz=pz-aj["z"]
                if dx*dx+dy*dy+dz*dz<rj*rj: buried=True; break
            if not buried: exposed+=1
        total+=4*math.pi*ri*ri*exposed/len(SPHERE)
    return total

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

def interface_atoms(atoms, ref_atoms, cutoff=8.0):
    intf=[]
    for a in atoms:
        for r in ref_atoms:
            if dist(a,r)<=cutoff: intf.append(a); break
    return intf

# Reload
lig_6h0f = [a for a in parse_chain(p6h0f,"B",("HETATM",)) if a["resn"]=="Y70"]
crbn_B   = parse_chain(p6h0f,"B",("ATOM",))
ikzf1_C  = parse_chain(p6h0f,"C",("ATOM",))
fsc_A    = [a for a in parse_chain(p2o98,"A",("HETATM",)) if a["resn"]=="FSC"]
p14_A    = parse_chain(p2o98,"A",("ATOM",))
atpase_P = parse_chain(p2o98,"P",("ATOM",))

# ── Correct ligand SASA free vs bound ──
def lig_burial(lig, prot_context):
    heavy_lig=[a for a in lig if element(a["name"])!="H"]
    # free: only lig heavy atoms
    sasa_free = sasa_masked(heavy_lig, list(range(len(heavy_lig))))
    # bound: lig + nearby prot (8Å shell)
    nb_prot = interface_atoms(prot_context, lig, 8.0)
    context = heavy_lig + nb_prot
    sasa_bound = sasa_masked(context, list(range(len(heavy_lig))))
    return sasa_free, sasa_bound

print("Computing ligand burial fractions...")
f6,b6 = lig_burial(lig_6h0f, crbn_B+ikzf1_C)
print(f"  6H0F pomalidomide: free={f6:.0f} Å²  bound={b6:.0f} Å²  "
      f"buried={f6-b6:.0f} Å²  ({100*(f6-b6)/f6:.0f}%)")

ff,bf = lig_burial(fsc_A, p14_A+atpase_P)
print(f"  2O98 fusicoccin:   free={ff:.0f} Å²  bound={bf:.0f} Å²  "
      f"buried={ff-bf:.0f} Å²  ({100*(ff-bf)/ff:.0f}%)")

# ── PPI BSA (protein–protein only, no ligand) ──
# Use 6Å interface shell, compute SASA in isolation vs together
def ppi_bsa(prot1, prot2, shell=7.0):
    p1i=interface_atoms(prot1,prot2,shell)
    p2i=interface_atoms(prot2,prot1,shell)
    h1=[a for a in p1i if element(a["name"])!="H"]
    h2=[a for a in p2i if element(a["name"])!="H"]
    s1=sasa_masked(h1, list(range(len(h1))))
    s2=sasa_masked(h2, list(range(len(h2))))
    combined=h1+h2
    s1_in_cx=sasa_masked(combined, list(range(len(h1))))
    s2_in_cx=sasa_masked(combined, list(range(len(h1),len(combined))))
    bsa_val=((s1-s1_in_cx)+(s2-s2_in_cx))/2
    return bsa_val, s1+s2

print("\nComputing PPI BSA...")
bsa6,tot6=ppi_bsa(crbn_B, ikzf1_C)
print(f"  6H0F CRBN/IKZF1 BSA: {bsa6:.0f} Å²  (total interface shell SASA: {tot6:.0f} Å²)")
bsa2,tot2=ppi_bsa(p14_A, atpase_P)
print(f"  2O98 14-3-3/ATPase BSA: {bsa2:.0f} Å²  (total: {tot2:.0f} Å²)")
