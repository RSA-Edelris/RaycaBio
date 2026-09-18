
# Full contact map: ligand vs each protein chain, interaction typing

import math, json
from collections import defaultdict

HBOND_DONORS_ACCEPTORS = {"N","O","S"}
CUTOFF_CONTACT = 4.5   # generous vdW/hydrophobic
CUTOFF_HBOND   = 3.5   # N/O heavy-atom distance
CUTOFF_IONIC   = 4.0   # charged groups

def dist(a, b):
    return math.sqrt((a["x"]-b["x"])**2 + (a["y"]-b["y"])**2 + (a["z"]-b["z"])**2)

def element(atom_name):
    # first non-digit, non-space character
    for c in atom_name:
        if c.isalpha():
            return c.upper()
    return "?"

def interaction_type(lig_atom, prot_atom):
    le = element(lig_atom["name"])
    pe = element(prot_atom["name"])
    d = dist(lig_atom, prot_atom)
    types = []
    # H-bond: both heavy atoms must be N or O
    if d <= CUTOFF_HBOND and le in HBOND_DONORS_ACCEPTORS and pe in HBOND_DONORS_ACCEPTORS:
        types.append(f"H-bond({d:.2f}Å)")
    # Hydrophobic / vdW
    elif d <= CUTOFF_CONTACT and le == "C" and pe == "C":
        types.append(f"hydrophobic({d:.2f}Å)")
    # Halogen / other polar
    elif d <= CUTOFF_CONTACT and (le in HBOND_DONORS_ACCEPTORS or pe in HBOND_DONORS_ACCEPTORS):
        if d <= CUTOFF_HBOND:
            types.append(f"polar({d:.2f}Å)")
        else:
            types.append(f"polar-weak({d:.2f}Å)")
    elif d <= CUTOFF_CONTACT:
        types.append(f"vdW({d:.2f}Å)")
    return types

def parse_chain_atoms(path, chain, rec_types=("ATOM","HETATM")):
    atoms = []
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec not in rec_types:
                continue
            ch = line[21]
            if ch != chain:
                continue
            alt = line[16].strip()
            if alt and alt not in ('', 'A', ' '):
                continue
            try:
                atoms.append({
                    "rec": rec, "name": line[12:16].strip(),
                    "resn": line[17:20].strip(), "chain": ch,
                    "resi": int(line[22:26]),
                    "x": float(line[30:38]), "y": float(line[38:46]), "z": float(line[46:54]),
                    "occ": float(line[54:60]), "bfac": float(line[60:66]),
                })
            except:
                pass
    return atoms

def contacts_lig_vs_prot(lig_atoms, prot_atoms, cutoff=4.5):
    """Return list of (lig_atom, prot_atom, [interaction_types], distance)."""
    result = []
    for la in lig_atoms:
        for pa in prot_atoms:
            if pa["resn"] in ("HOH","WAT"):
                continue
            d = dist(la, pa)
            if d <= cutoff:
                itypes = interaction_type(la, pa)
                if itypes:
                    result.append((la, pa, itypes, d))
    return result

def summarise_contacts(contacts, label):
    """Group by protein residue and print."""
    res_contacts = defaultdict(list)
    for la, pa, itypes, d in contacts:
        key = (pa["resn"], pa["resi"])
        res_contacts[key].append((la["name"], pa["name"], itypes[0], d))
    print(f"\n  -- {label}: {len(res_contacts)} contacting residues --")
    for (resn, resi), clist in sorted(res_contacts.items(), key=lambda x: x[0][1]):
        # summarise interaction types
        hb = [c for c in clist if "H-bond" in c[2] or "polar(" in c[2]]
        hyd = [c for c in clist if "hydrophobic" in c[2]]
        weak = [c for c in clist if "weak" in c[2] or "vdW" in c[2]]
        summary_parts = []
        if hb:
            dists = [c[3] for c in hb]
            atoms = "; ".join(f"{c[0]}→{c[1]}({c[3]:.2f})" for c in hb[:3])
            summary_parts.append(f"H-bond/polar [{atoms}]")
        if hyd:
            count = len(hyd)
            summary_parts.append(f"{count}×hydrophobic")
        if weak:
            summary_parts.append(f"{len(weak)}×vdW")
        print(f"    {resn}{resi}: {' | '.join(summary_parts)}")
    return res_contacts

# ─── 6H0F analysis: chain B = CRBN, chain C = IKZF1, Y70/502 = pomalidomide ───
print("="*65)
print("6H0F — POMALIDOMIDE (Y70 B502) contacts")
print("="*65)

lig_6h0f = [a for a in parse_chain_atoms(p6h0f, "B", ("HETATM",)) if a["resn"]=="Y70"]
crbn_atoms = [a for a in parse_chain_atoms(p6h0f, "B", ("ATOM",))]
ikzf1_atoms = parse_chain_atoms(p6h0f, "C", ("ATOM",))

contacts_crbn = contacts_lig_vs_prot(lig_6h0f, crbn_atoms)
contacts_ikzf = contacts_lig_vs_prot(lig_6h0f, ikzf1_atoms)

rc_crbn = summarise_contacts(contacts_crbn, "CRBN (chain B)")
rc_ikzf = summarise_contacts(contacts_ikzf, "IKZF1-ZF2 (chain C)")

# bridging = lig atoms that touch BOTH partners
lig_touch_crbn = {la["name"] for la,pa,it,d in contacts_crbn}
lig_touch_ikzf = {la["name"] for la,pa,it,d in contacts_ikzf}
bridging_atoms = lig_touch_crbn & lig_touch_ikzf
print(f"\n  Pomalidomide atoms bridging BOTH partners: {sorted(bridging_atoms)}")
print(f"  Touching only CRBN: {sorted(lig_touch_crbn - lig_touch_ikzf)}")
print(f"  Touching only IKZF1: {sorted(lig_touch_ikzf - lig_touch_crbn)}")
