
import numpy as np
from rdkit import Chem
import json

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

# ── 1. Load receptor atoms (N, O, C backbone + sidechain) ─────────────────────
with open(f'{WD}/PB-20260903-4CI2_receptor_trimmed_fixed.pdb') as f:
    rec_lines = f.readlines()

prot_atoms = []   # (resi, resn, aname, elem, x, y, z)
for line in rec_lines:
    if line[:4] != 'ATOM': continue
    if len(line) < 54: continue
    try:
        x,y,z = float(line[30:38]), float(line[38:46]), float(line[46:54])
    except: continue
    resi  = int(line[22:26].strip())
    resn  = line[17:20].strip()
    aname = line[12:16].strip()
    elem  = line[76:78].strip() if len(line) > 76 else aname[0]
    prot_atoms.append((resi, resn, aname, elem, x, y, z))

prot_arr = np.array([[x,y,z] for *_, x,y,z in prot_atoms])

# ── 2. TRP ring centroids (indole 6-ring: CG CD1 CD2 CE2 CE3 CZ2 CZ3 CH2)
TRP_RESI = [336, 342, 356]
trp_ring_atoms = {'CG','CD1','CD2','CE2','CE3','CZ2','CZ3','CH2'}  # indole C atoms

trp_centroids = {}
for trp_r in TRP_RESI:
    coords = np.array([[x,y,z] for (resi,resn,aname,elem,x,y,z) in prot_atoms
                        if resi==trp_r and aname in trp_ring_atoms])
    if len(coords) >= 4:
        trp_centroids[trp_r] = coords.mean(axis=0)
        # normal vector from SVD
        centered = coords - trp_centroids[trp_r]
        _, _, Vt = np.linalg.svd(centered)
        trp_centroids[trp_r] = (trp_centroids[trp_r], Vt[-1])  # (centroid, normal)
    print(f"TRP {trp_r}: {len(coords)} ring atoms")

# ── 3. H-bond donor/acceptor atoms in protein (N and O, within contact residues)
HB_ELEMS = {'N', 'O'}
contacts_union = {306,307,308,309,311,313,333,334,335,336,337,342,344,346,
                  353,356,358,371,376}

prot_hb = [(resi,resn,aname,elem,x,y,z) for (resi,resn,aname,elem,x,y,z)
           in prot_atoms if elem in HB_ELEMS and resi in contacts_union]
prot_hb_arr = np.array([[x,y,z] for *_,x,y,z in prot_hb])
print(f"\nProtein H-bond atoms in contact zone: {len(prot_hb)}")
print("TRP centroids computed:", list(trp_centroids.keys()))
