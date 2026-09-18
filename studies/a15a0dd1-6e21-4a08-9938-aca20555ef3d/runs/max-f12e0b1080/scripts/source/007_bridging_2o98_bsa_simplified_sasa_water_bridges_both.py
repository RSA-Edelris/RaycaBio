
# Bridging for 2O98, BSA (simplified SASA), water bridges for both structures

import math
from collections import defaultdict

CUTOFF_CONTACT = 4.5
CUTOFF_HBOND   = 3.5
PROBE_R        = 1.4   # solvent probe radius Å

VDW = {"C":1.7,"N":1.55,"O":1.52,"S":1.8,"P":1.8,
       "ZN":1.39,"CL":1.75,"BR":1.85,"F":1.47,"H":1.2}

def dist(a,b):
    return math.sqrt((a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2)

def element(name):
    for c in name:
        if c.isalpha(): return c.upper()
    return "C"

def interact_type(la, pa):
    le, pe = element(la["name"]), element(pa["name"])
    d = dist(la, pa)
    polar = {"N","O","S"}
    if d > CUTOFF_CONTACT: return None
    if d <= CUTOFF_HBOND and le in polar and pe in polar:
        return f"H-bond({d:.2f}Å)"
    if le == "C" and pe == "C": return f"hydrophobic({d:.2f}Å)"
    if le in polar or pe in polar: return f"polar({d:.2f}Å)"
    return f"vdW({d:.2f}Å)"

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

# ── 2O98 bridging analysis ──
fsc_A    = [a for a in parse_chain(p2o98,"A",("HETATM",)) if a["resn"]=="FSC"]
p14_A    = parse_chain(p2o98,"A",("ATOM",))
atpase_P = parse_chain(p2o98,"P",("ATOM",))

touch14, touchATP = set(), set()
for la in fsc_A:
    for pa in p14_A:
        if pa["resn"] not in ("HOH","WAT") and interact_type(la,pa):
            touch14.add(la["name"])
    for pa in atpase_P:
        if pa["resn"] not in ("HOH","WAT") and interact_type(la,pa):
            touchATP.add(la["name"])

print("FSC atoms bridging BOTH partners:", sorted(touch14 & touchATP))
print("FSC atoms touching only 14-3-3:  ", sorted(touch14 - touchATP))
print("FSC atoms touching only ATPase:  ", sorted(touchATP - touch14))
print()

# ── BSA: count interface-buried atoms at the lig/prot interface ──
# Simple: for each ligand, count protein heavy atoms within 5Å as "interface atoms"
# Then estimate BSA ~ N_interface_atoms × 15 Å² (avg ~15 Å²/atom at flat interface)
# More rigorous: BSA = SASA(lig) + SASA(prot) - SASA(complex), using sphere overlap count

def rough_bsa(lig_atoms, prot1_atoms, prot2_atoms):
    """Count unique prot residues at interface, estimate BSA from atom counts."""
    intf1, intf2 = set(), set()
    n_atoms1, n_atoms2 = 0, 0
    for la in lig_atoms:
        for pa in prot1_atoms:
            if pa["resn"] in ("HOH","WAT"): continue
            if dist(la,pa) <= 5.0:
                intf1.add((pa["resn"],pa["resi"]))
                n_atoms1 += 1
        for pa in prot2_atoms:
            if pa["resn"] in ("HOH","WAT"): continue
            if dist(la,pa) <= 5.0:
                intf2.add((pa["resn"],pa["resi"]))
                n_atoms2 += 1
    # also protein-protein interface (PPI itself)
    ppi_res1, ppi_res2 = set(), set()
    for a1 in prot1_atoms:
        if a1["resn"] in ("HOH","WAT"): continue
        for a2 in prot2_atoms:
            if a2["resn"] in ("HOH","WAT"): continue
            if dist(a1,a2) <= 5.0:
                ppi_res1.add((a1["resn"],a1["resi"]))
                ppi_res2.add((a2["resn"],a2["resi"]))
    return {
        "lig_prot1_res": sorted(intf1), "lig_prot2_res": sorted(intf2),
        "lig_prot1_atom_contacts": n_atoms1, "lig_prot2_atom_contacts": n_atoms2,
        "ppi_prot1_res": sorted(ppi_res1), "ppi_prot2_res": sorted(ppi_res2),
    }

# 6H0F
lig_6h0f = [a for a in parse_chain(p6h0f,"B",("HETATM",)) if a["resn"]=="Y70"]
crbn_B   = parse_chain(p6h0f,"B",("ATOM",))
ikzf1_C  = parse_chain(p6h0f,"C",("ATOM",))

bsa6 = rough_bsa(lig_6h0f, crbn_B, ikzf1_C)
print("=== 6H0F Interface ===")
print(f"  Lig→CRBN atom contacts: {bsa6['lig_prot1_atom_contacts']}")
print(f"  Lig→IKZF1 atom contacts: {bsa6['lig_prot2_atom_contacts']}")
print(f"  CRBN residues at CRBN/IKZF1 PPI (5Å): {[f'{r}{i}' for r,i in bsa6['ppi_prot1_res']]}")
print(f"  IKZF1 residues at PPI: {[f'{r}{i}' for r,i in bsa6['ppi_prot2_res']]}")

bsa2 = rough_bsa(fsc_A, p14_A, atpase_P)
print("\n=== 2O98 Interface ===")
print(f"  Lig→14-3-3 atom contacts: {bsa2['lig_prot1_atom_contacts']}")
print(f"  Lig→ATPase atom contacts: {bsa2['lig_prot2_atom_contacts']}")
print(f"  14-3-3 residues at PPI (5Å): {[f'{r}{i}' for r,i in bsa2['ppi_prot1_res']]}")
print(f"  ATPase residues at PPI: {[f'{r}{i}' for r,i in bsa2['ppi_prot2_res']]}")
