
# 2O98 contact analysis: FSC vs 14-3-3 (chain A) and H+-ATPase (chain P)

import math
from collections import defaultdict

CUTOFF_CONTACT = 4.5
CUTOFF_HBOND   = 3.5

def dist(a, b):
    return math.sqrt((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2)

def element(name):
    for c in name:
        if c.isalpha():
            return c.upper()
    return "?"

def parse_chain(path, chain, recs=("ATOM","HETATM")):
    atoms = []
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec not in recs: continue
            if line[21] != chain: continue
            alt = line[16].strip()
            if alt and alt not in ('', 'A', ' '): continue
            try:
                atoms.append({
                    "rec": rec, "name": line[12:16].strip(),
                    "resn": line[17:20].strip(), "chain": line[21],
                    "resi": int(line[22:26]),
                    "x": float(line[30:38]), "y": float(line[38:46]), "z": float(line[46:54]),
                    "occ": float(line[54:60]), "bfac": float(line[60:66]),
                })
            except: pass
    return atoms

def interact_type(la, pa):
    le, pe = element(la["name"]), element(pa["name"])
    d = dist(la, pa)
    polar = {"N","O","S"}
    if d <= CUTOFF_HBOND and le in polar and pe in polar:
        return f"H-bond({d:.2f}Å)"
    elif d <= CUTOFF_CONTACT and le == "C" and pe == "C":
        return f"hydrophobic({d:.2f}Å)"
    elif d <= CUTOFF_CONTACT and (le in polar or pe in polar):
        return f"polar({d:.2f}Å)"
    elif d <= CUTOFF_CONTACT:
        return f"vdW({d:.2f}Å)"
    return None

def contact_map(lig, prot, label):
    res_contacts = defaultdict(list)
    for la in lig:
        for pa in prot:
            if pa["resn"] in ("HOH","WAT"): continue
            it = interact_type(la, pa)
            if it:
                res_contacts[(pa["resn"], pa["resi"])].append(
                    (la["name"], pa["name"], it))
    print(f"\n  -- {label}: {len(res_contacts)} contacting residues --")
    for (resn, resi), clist in sorted(res_contacts.items(), key=lambda x: x[0][1]):
        hb  = [c for c in clist if "H-bond" in c[2]]
        pol = [c for c in clist if "polar" in c[2] and "H-bond" not in c[2]]
        hyd = [c for c in clist if "hydrophobic" in c[2]]
        vdw = [c for c in clist if "vdW" in c[2]]
        parts = []
        if hb:  parts.append("H-bond[" + "; ".join(f"{c[0]}→{c[1]} {c[2]}" for c in hb[:3]) + "]")
        if pol: parts.append(f"{len(pol)}×polar")
        if hyd: parts.append(f"{len(hyd)}×hydrophobic")
        if vdw: parts.append(f"{len(vdw)}×vdW")
        print(f"    {resn}{resi}: {' | '.join(parts)}")
    return res_contacts

print("="*65)
print("2O98 — FUSICOCCIN (FSC A1001) contacts")
print("="*65)

fsc_A = [a for a in parse_chain(p2o98, "A", ("HETATM",)) if a["resn"]=="FSC"]
p14_A  = parse_chain(p2o98, "A", ("ATOM",))
atpase_P = parse_chain(p2o98, "P", ("ATOM",))

rc_14 = contact_map(fsc_A, p14_A,   "14-3-3 (chain A)")
rc_atp= contact_map(fsc_A, atpase_P, "H+-ATPase (chain P)")

# Bridging analysis
lig_touch_14   = {la["name"] for la,pa,it,d_ in [(la,pa,it,0) 
    for la in fsc_A for pa in p14_A if pa["resn"] not in ("HOH","WAT") and interact_type(la,pa)]
    if interact_type(la,pa)}

# redo cleanly
touch14 = set()
touchATP = set()
for la in fsc_A:
    for pa in p14_A:
        if pa["resn"] not in ("HOH","WAT") and interact_type(la, pa):
            touch14.add(la["name"])
    for pa in atpase_P:
        if pa["resn"] not in ("HOH","WAT") and interact_type(la, pa):
            touchATP.add(la["name"])

print(f"\n  FSC atoms bridging BOTH partners: {sorted(touch14 & touchATP)}")
print(f"  Touching only 14-3-3: {sorted(touch14 - touchATP)}")
print(f"  Touching only ATPase: {sorted(touchATP - touch14)}")
print(f"\n  FSC total atoms: {len(fsc_A)}")
