#!/usr/bin/env python3
"""RDKit-only protein-ligand interaction analysis — no MDAnalysis/ProLIF.
   Parses receptor PDB manually, computes H-bond/hydrophobic/pi interactions
   from atom coordinates for each best-pose ligand SDF.
"""

import json, math, re
from pathlib import Path
from collections import defaultdict, Counter

VENV_PYTHON = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
BEST_DIR  = BASE / "best_poses2_top1"
REC_PDB   = BASE / "mmgbsa2" / "receptor_amber.pdb"  # HID/HIE fixed
OUT_FILE  = BASE / "interaction_fingerprints.json"

# --- Interaction geometry thresholds ---
HBOND_DA_DIST   = 3.5   # Å donor-acceptor
HBOND_DHA_ANGLE = 120.0 # degrees minimum D-H...A angle
HYDROPHOB_DIST  = 4.0   # Å C-C (non-polar)
PI_STACK_DIST   = 5.5   # Å centroid-centroid
PI_STACK_ANGLE_PAR  = 30.0   # ±° from parallel (face-to-face)
PI_STACK_ANGLE_PERP = 30.0   # ±° from 90° (T-shape)
PI_CAT_DIST     = 5.0   # Å ring centroid to cation N

# Residue H-bond roles per AMBER/PDB naming
HB_DONORS    = {'N', 'O', 'S'}   # heavy atom elements that can donate
HB_ACCEPTORS = {'N', 'O', 'S'}   # heavy atom elements that can accept
HYDROPHOBIC_ELEMENTS = {'C', 'S'}
CATION_NAMES = {'NZ', 'NH1', 'NH2', 'ND1', 'NE', 'NE2'}  # Lys, Arg, His
AROMATIC_RES = {'PHE', 'TYR', 'TRP', 'HIS', 'HID', 'HIE', 'HIP'}
AROMATIC_ATOMS = {
    'PHE': ['CG','CD1','CD2','CE1','CE2','CZ'],
    'TYR': ['CG','CD1','CD2','CE1','CE2','CZ'],
    'TRP': ['CD2','CE2','CE3','CZ2','CZ3','CH2'],
    'HIS': ['CG','ND1','CD2','CE1','NE2'],
    'HID': ['CG','ND1','CD2','CE1','NE2'],
    'HIE': ['CG','ND1','CD2','CE1','NE2'],
    'HIP': ['CG','ND1','CD2','CE1','NE2'],
}


def dist(a, b):
    return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))

def angle_deg(a, b, c):
    """Angle at vertex b (a-b-c)."""
    v1 = tuple(a[i]-b[i] for i in range(3))
    v2 = tuple(c[i]-b[i] for i in range(3))
    n1 = math.sqrt(sum(x*x for x in v1))
    n2 = math.sqrt(sum(x*x for x in v2))
    if n1 < 1e-6 or n2 < 1e-6:
        return 0.0
    cos_a = max(-1.0, min(1.0, sum(v1[i]*v2[i] for i in range(3))/(n1*n2)))
    return math.degrees(math.acos(cos_a))

def centroid(coords):
    n = len(coords)
    return tuple(sum(c[i] for c in coords)/n for i in range(3))

def normal(coords):
    """Normal to the plane of coords (first 3 used for cross product)."""
    if len(coords) < 3:
        return (0,0,1)
    A, B, C = coords[0], coords[1], coords[2]
    v1 = tuple(B[i]-A[i] for i in range(3))
    v2 = tuple(C[i]-A[i] for i in range(3))
    nx = v1[1]*v2[2]-v1[2]*v2[1]
    ny = v1[2]*v2[0]-v1[0]*v2[2]
    nz = v1[0]*v2[1]-v1[1]*v2[0]
    mag = math.sqrt(nx*nx+ny*ny+nz*nz)
    if mag < 1e-6:
        return (0,0,1)
    return (nx/mag, ny/mag, nz/mag)


# ─── Parse receptor PDB ───────────────────────────────────────────────────────
print("Loading receptor...", flush=True)
rec_atoms = []   # list of dicts
res_map   = defaultdict(list)  # (resname, chain, resseq) → [atom_idx]

for line in REC_PDB.read_text().splitlines():
    if not line.startswith('ATOM'):
        continue
    atom_name = line[12:16].strip()
    resname   = line[17:20].strip()
    chain     = line[21]
    resseq    = int(line[22:26].strip())
    try:
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
    except ValueError:
        continue
    element = line[76:78].strip() if len(line)>=78 else atom_name[0]
    idx = len(rec_atoms)
    rec_atoms.append({
        'name': atom_name, 'resname': resname, 'chain': chain,
        'resseq': resseq, 'coord': (x,y,z), 'element': element,
        'res_key': (resname, chain, resseq)
    })
    res_map[(resname, chain, resseq)].append(idx)

print(f"  {len(rec_atoms)} protein atoms, {len(res_map)} residues", flush=True)

# Build H lookup: for each heavy atom, find covalently bonded H atoms
# (distance < 1.25 Å within same residue)
h_bonds_map = defaultdict(list)  # heavy_idx → [h_idx]
for res_key, idxs in res_map.items():
    atoms_in_res = [rec_atoms[i] for i in idxs]
    for i, a in zip(idxs, atoms_in_res):
        if a['element'] not in ('H',):
            continue
        for j, b in zip(idxs, atoms_in_res):
            if b['element'] in ('H',):
                continue
            if dist(a['coord'], b['coord']) < 1.25:
                h_bonds_map[j].append(i)

# Build ring systems for aromatic residues
ring_map = {}  # res_key → {'centroid': xyz, 'normal': xyz}
for res_key, idxs in res_map.items():
    resname = res_key[0]
    if resname not in AROMATIC_ATOMS:
        continue
    expected = AROMATIC_ATOMS[resname]
    coords = [rec_atoms[i]['coord'] for i in idxs
              if rec_atoms[i]['name'] in expected]
    if len(coords) >= 5:
        ring_map[res_key] = {
            'centroid': centroid(coords),
            'normal': normal(coords)
        }

print(f"  {len(ring_map)} aromatic residues indexed", flush=True)


# ─── Per-ligand analysis ───────────────────────────────────────────────────────
from rdkit import Chem

names = sorted([f.stem.replace('_pose1','') for f in BEST_DIR.glob('*_pose1.sdf')])
print(f"\nAnalysing {len(names)} poses...", flush=True)

all_fp   = {}
res_type = Counter()
int_type = Counter()
res_cnt  = Counter()

POCKET_RADIUS = 6.0  # Å for residue pre-filtering

for name in names:
    sdf = BEST_DIR / f"{name}_pose1.sdf"
    mol = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)[0]
    if mol is None:
        print(f"  {name}: RDKit load failed", flush=True)
        all_fp[name] = []
        continue

    conf = mol.GetConformer()
    lig_pos = [conf.GetAtomPosition(i) for i in range(mol.GetNumAtoms())]
    lig_coords = [(p.x, p.y, p.z) for p in lig_pos]
    lig_cx, lig_cy, lig_cz = centroid(lig_coords)

    # Ligand atom properties
    lig_atoms = []
    for atom in mol.GetAtoms():
        idx = atom.GetIdx()
        coord = lig_coords[idx]
        el = atom.GetSymbol()
        in_ring = atom.IsInRing()
        arom   = atom.GetIsAromatic()
        charge = atom.GetFormalCharge()
        # H-bond donor: N or O with attached H
        hb_don = el in ('N','O') and any(
            mol.GetAtomWithIdx(nb.GetIdx()).GetSymbol()=='H'
            for nb in atom.GetNeighbors()
        )
        hb_acc = el in ('N','O','S')
        hb_h_coords = [lig_coords[nb.GetIdx()]
                       for nb in atom.GetNeighbors()
                       if mol.GetAtomWithIdx(nb.GetIdx()).GetSymbol()=='H']
        lig_atoms.append({
            'idx': idx, 'coord': coord, 'element': el,
            'in_ring': in_ring, 'aromatic': arom, 'charge': charge,
            'hb_donor': hb_don, 'hb_acceptor': hb_acc,
            'hb_h_coords': hb_h_coords,
            'hydrophobic': el == 'C' and not arom
        })

    # Ligand aromatic rings
    lig_rings = []
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        atoms_in_ring = [mol.GetAtomWithIdx(i) for i in ring]
        if all(a.GetIsAromatic() for a in atoms_in_ring):
            coords_r = [lig_coords[i] for i in ring]
            lig_rings.append({
                'centroid': centroid(coords_r),
                'normal': normal(coords_r)
            })

    # Cationic atoms in ligand (formal charge + N)
    lig_cations = [a['coord'] for a in lig_atoms
                   if a['element'] == 'N' and a['charge'] >= 0
                   and not a['aromatic']]

    # Pre-filter residues within pocket radius
    pocket_res = set()
    for res_key, idxs in res_map.items():
        for i in idxs:
            if dist(rec_atoms[i]['coord'], (lig_cx, lig_cy, lig_cz)) < POCKET_RADIUS + 4.0:
                pocket_res.add(res_key)
                break

    interactions = []
    seen_interactions = set()

    for res_key in pocket_res:
        resname, chain, resseq = res_key
        label = f"{resname}{resseq}"
        idxs = res_map[res_key]
        rec_res_atoms = [rec_atoms[i] for i in idxs]

        for rec_atom in rec_res_atoms:
            ra_coord = rec_atom['coord']
            ra_el    = rec_atom['element']
            ra_name  = rec_atom['name']
            if ra_el == 'H':
                continue

            # H-bond: receptor as donor (D=rec heavy, H=rec H, A=lig acceptor)
            if ra_el in HB_DONORS:
                for h_idx in h_bonds_map.get(rec_atoms.index(rec_atom) if rec_atom in rec_atoms else -1, []):
                    pass  # skip — expensive; use shortcut below
                # Shortcut: check if any lig acceptor is within HB distance of rec heavy
                for la in lig_atoms:
                    if not la['hb_acceptor']:
                        continue
                    d = dist(ra_coord, la['coord'])
                    if d > HBOND_DA_DIST:
                        continue
                    # Check H position: use rec H atoms
                    h_list = h_bonds_map.get(rec_atom['idx'], [])
                    if h_list:
                        for h_i in h_list:
                            h_coord = rec_atoms[h_i]['coord']
                            ang = angle_deg(ra_coord, h_coord, la['coord'])
                            if ang >= HBOND_DHA_ANGLE:
                                key = (label, 'HBDonor')
                                if key not in seen_interactions:
                                    seen_interactions.add(key)
                                    interactions.append({'protein_residue': label, 'interaction': 'HBDonor'})
                                break
                    else:
                        # No H found; use distance only
                        if d < 3.2:
                            key = (label, 'HBDonor')
                            if key not in seen_interactions:
                                seen_interactions.add(key)
                                interactions.append({'protein_residue': label, 'interaction': 'HBDonor'})

            # H-bond: receptor as acceptor (D=lig, H=lig H, A=rec heavy)
            if ra_el in HB_ACCEPTORS:
                for la in lig_atoms:
                    if not la['hb_donor']:
                        continue
                    d = dist(ra_coord, la['coord'])
                    if d > HBOND_DA_DIST:
                        continue
                    if la['hb_h_coords']:
                        for h_c in la['hb_h_coords']:
                            ang = angle_deg(la['coord'], h_c, ra_coord)
                            if ang >= HBOND_DHA_ANGLE:
                                key = (label, 'HBAcceptor')
                                if key not in seen_interactions:
                                    seen_interactions.add(key)
                                    interactions.append({'protein_residue': label, 'interaction': 'HBAcceptor'})
                                break
                    else:
                        if d < 3.2:
                            key = (label, 'HBAcceptor')
                            if key not in seen_interactions:
                                seen_interactions.add(key)
                                interactions.append({'protein_residue': label, 'interaction': 'HBAcceptor'})

            # Hydrophobic contacts
            if ra_el == 'C' and not ra_name.startswith(('C=','C ')):
                for la in lig_atoms:
                    if not la['hydrophobic']:
                        continue
                    if dist(ra_coord, la['coord']) <= HYDROPHOB_DIST:
                        key = (label, 'Hydrophobic')
                        if key not in seen_interactions:
                            seen_interactions.add(key)
                            interactions.append({'protein_residue': label, 'interaction': 'Hydrophobic'})
                        break

            # Cation-Pi: receptor cationic N near ligand aromatic ring
            if ra_name in CATION_NAMES:
                for lr in lig_rings:
                    if dist(ra_coord, lr['centroid']) <= PI_CAT_DIST:
                        key = (label, 'CationPi')
                        if key not in seen_interactions:
                            seen_interactions.add(key)
                            interactions.append({'protein_residue': label, 'interaction': 'CationPi'})
                        break

        # Pi-stacking: receptor aromatic ring vs ligand aromatic ring
        if res_key in ring_map:
            rr = ring_map[res_key]
            for lr in lig_rings:
                d_cent = dist(rr['centroid'], lr['centroid'])
                if d_cent > PI_STACK_DIST:
                    continue
                # Angle between ring normals
                rn, ln = rr['normal'], lr['normal']
                cos_a = abs(sum(rn[i]*ln[i] for i in range(3)))
                cos_a = min(1.0, cos_a)
                ang = math.degrees(math.acos(cos_a))
                # Parallel (face-to-face) or perpendicular (T-shape)
                if ang <= PI_STACK_ANGLE_PAR or ang >= (90.0 - PI_STACK_ANGLE_PERP):
                    key = (label, 'PiStacking')
                    if key not in seen_interactions:
                        seen_interactions.add(key)
                        interactions.append({'protein_residue': label, 'interaction': 'PiStacking'})
                    break

        # Pi-Cation: receptor aromatic ring near ligand cation
        if res_key in ring_map and lig_cations:
            rr = ring_map[res_key]
            for cat_coord in lig_cations:
                if dist(rr['centroid'], cat_coord) <= PI_CAT_DIST:
                    key = (label, 'PiCation')
                    if key not in seen_interactions:
                        seen_interactions.add(key)
                        interactions.append({'protein_residue': label, 'interaction': 'PiCation'})
                    break

    all_fp[name] = interactions
    types_seen = sorted(set(i['interaction'] for i in interactions))
    by_res = sorted(set(i['protein_residue'] for i in interactions))
    print(f"  {name}: {len(interactions)} interactions | residues: {', '.join(by_res[:6])}{'...' if len(by_res)>6 else ''}", flush=True)

    for inter in interactions:
        k = (inter['protein_residue'], inter['interaction'])
        res_type[k] += 1
        res_cnt[inter['protein_residue']] += 1
        int_type[inter['interaction']] += 1

n = len(names)
print(f"\n=== INTERACTION FREQUENCY (n={n} compounds) ===")
print(f"{'Residue':<18} {'Type':<15} {'#':>4} {'Freq':>7}")
print("─" * 46)
for (res, itype), cnt in res_type.most_common(30):
    print(f"{res:<18} {itype:<15} {cnt:>4} {100*cnt/n:>6.0f}%")

print(f"\nInteraction type totals:")
for itype, cnt in int_type.most_common():
    print(f"  {itype:<18} {cnt:>4}  ({100*cnt/n:.0f}%)")

out = {
    'fingerprints': all_fp,
    'residue_type_freq': {f"{k[0]}|{k[1]}": v for k,v in res_type.most_common()},
    'interaction_type_counts': dict(int_type),
    'residue_counts': dict(res_cnt.most_common(25)),
    'n_compounds': n,
}
OUT_FILE.write_text(json.dumps(out, indent=2))
print(f"\nSaved → {OUT_FILE}")
