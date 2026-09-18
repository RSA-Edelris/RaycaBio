
# SASA-based BSA + bridging water analysis

import math
from collections import defaultdict

PROBE_R = 1.4
VDW = {"C":1.7,"N":1.55,"O":1.52,"S":1.8,"P":1.8,"ZN":1.39,"CL":1.75,"F":1.47,"H":1.1}

def dist(a,b):
    return math.sqrt((a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2)

def element(name):
    for c in name:
        if c.isalpha(): return c.upper()
    return "C"

def parse_chain(path, chain, recs=("ATOM","HETATM")):
    atoms = []
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec not in recs: continue
            if line[21] != chain: continue
            alt = line[16].strip()
            if alt and alt not in ('','A',' '): continue
            try:
                atoms.append({
                    "rec":rec,"name":line[12:16].strip(),
                    "resn":line[17:20].strip(),"chain":line[21],
                    "resi":int(line[22:26]),
                    "x":float(line[30:38]),"y":float(line[38:46]),"z":float(line[46:54]),
                    "occ":float(line[54:60]),"bfac":float(line[60:66]),
                })
            except: pass
    return atoms

# Shrake-Rupley (92-point sphere)
def _sphere_points(n=92):
    pts = []
    inc = math.pi*(3-math.sqrt(5))
    off = 2.0/n
    for k in range(n):
        y = k*off-1+(off/2)
        r = math.sqrt(max(0,1-y*y))
        phi = k*inc
        pts.append((math.cos(phi)*r, y, math.sin(phi)*r))
    return pts

SPHERE = _sphere_points(92)

def sasa_atoms(atoms, probe=1.4):
    """Return per-atom SASA (Å²). Heavy atoms only."""
    heavy = [a for a in atoms if element(a["name"]) != "H"]
    radii = [VDW.get(element(a["name"]),1.7)+probe for a in heavy]
    n = len(heavy)
    areas = []
    for i,ai in enumerate(heavy):
        ri = radii[i]
        exposed = 0
        for sx,sy,sz in SPHERE:
            px = ai["x"]+ri*sx
            py = ai["y"]+ri*sy
            pz = ai["z"]+ri*sz
            buried = False
            for j,aj in enumerate(heavy):
                if j==i: continue
                rj = radii[j]
                dx = px-aj["x"]; dy = py-aj["y"]; dz = pz-aj["z"]
                if dx*dx+dy*dy+dz*dz < rj*rj:
                    buried = True; break
            if not buried:
                exposed += 1
        areas.append(4*math.pi*ri*ri*exposed/len(SPHERE))
    return sum(areas)

def bsa(atoms_complex, atoms_free1, atoms_free2):
    """BSA = (SASA_free1 + SASA_free2 - SASA_complex) / 2"""
    s_c  = sasa_atoms(atoms_complex)
    s_f1 = sasa_atoms(atoms_free1)
    s_f2 = sasa_atoms(atoms_free2)
    return (s_f1 + s_f2 - s_c)/2, s_c, s_f1, s_f2

# ── Load atoms ──
lig_6h0f  = [a for a in parse_chain(p6h0f,"B",("HETATM",)) if a["resn"]=="Y70"]
crbn_B    = parse_chain(p6h0f,"B",("ATOM",))
ikzf1_C   = parse_chain(p6h0f,"C",("ATOM",))

fsc_A     = [a for a in parse_chain(p2o98,"A",("HETATM",)) if a["resn"]=="FSC"]
p14_A     = parse_chain(p2o98,"A",("ATOM",))
atpase_P  = parse_chain(p2o98,"P",("ATOM",))

# ── Restrict to interface atoms only to keep SASA tractable ──
def interface_atoms(atoms, ref_atoms, cutoff=8.0):
    intf = []
    for a in atoms:
        for r in ref_atoms:
            if dist(a,r) <= cutoff:
                intf.append(a); break
    return intf

# For each structure, compute BSA for lig+prot1 vs prot2 (stabiliser contribution)
# Also compute lig SASA free vs bound (burial fraction)
print("Computing SASA... (may take ~15s)")

# 6H0F: lig burial
lig6_free_sasa  = sasa_atoms(lig_6h0f)
lig6_bound_sasa = sasa_atoms(lig_6h0f + crbn_B[:] + ikzf1_C[:])
# Use only nearby atoms for speed
crbn_intf  = interface_atoms(crbn_B,  lig_6h0f, 8.0)
ikzf1_intf = interface_atoms(ikzf1_C, lig_6h0f, 8.0)
lig6_bound_sasa2 = sasa_atoms(lig_6h0f + crbn_intf + ikzf1_intf)

print(f"\n6H0F pomalidomide:")
print(f"  Free ligand SASA:  {lig6_free_sasa:.0f} Å²")
print(f"  Bound ligand SASA (interface only): {lig6_bound_sasa2:.0f} Å²")
print(f"  Ligand burial: {100*(1-lig6_bound_sasa2/lig6_free_sasa):.0f}%")

# CRBN/IKZF1 protein-protein BSA gained on ternary formation (approx)
# Use 5Å shell around interface
crbn_ppi  = interface_atoms(crbn_B,  ikzf1_C, 6.0)
ikzf1_ppi = interface_atoms(ikzf1_C, crbn_B,  6.0)
bsa6_ppi, _, _, _ = bsa(crbn_ppi+ikzf1_ppi, crbn_ppi, ikzf1_ppi)
print(f"\n  CRBN/IKZF1 PPI interface BSA (6Å shell): {bsa6_ppi:.0f} Å²")

# 2O98: fusicoccin burial
fsc_free_sasa   = sasa_atoms(fsc_A)
p14_intf  = interface_atoms(p14_A,   fsc_A, 8.0)
atp_intf  = interface_atoms(atpase_P,fsc_A, 8.0)
fsc_bound_sasa  = sasa_atoms(fsc_A + p14_intf + atp_intf)
print(f"\n2O98 fusicoccin:")
print(f"  Free ligand SASA:  {fsc_free_sasa:.0f} Å²")
print(f"  Bound ligand SASA: {fsc_bound_sasa:.0f} Å²")
print(f"  Ligand burial: {100*(1-fsc_bound_sasa/fsc_free_sasa):.0f}%")

p14_ppi  = interface_atoms(p14_A,   atpase_P, 6.0)
atp_ppi  = interface_atoms(atpase_P,p14_A,    6.0)
bsa2_ppi, _, _, _ = bsa(p14_ppi+atp_ppi, p14_ppi, atp_ppi)
print(f"\n  14-3-3/ATPase PPI interface BSA (6Å shell): {bsa2_ppi:.0f} Å²")
