
# ---- Pocket druggability descriptors ----
# For each pocket: collect residue Cα coordinates from the parsed structures,
# compute convex hull volume, hydrophobic fraction, charged fraction, polar fraction.

import numpy as np
from scipy.spatial import ConvexHull

# Amino acid classifications
HYDROPHOBIC = set('AILVMFYWP')
POLAR       = set('STNQ')
CHARGED_POS = set('KRH')
CHARGED_NEG = set('DE')
AROMATIC    = set('FYW')

AA3 = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
    'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
    'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'
}

def residue_descriptors(res_triples, all_atoms_dict):
    """
    res_triples: list of (chain, resseq, resname)
    all_atoms_dict: dict keyed (chain,resseq) -> list of atom dicts
    Returns dict of descriptors.
    """
    ca_coords = []
    aa_codes  = []
    for chain, resseq, resname in res_triples:
        atoms_here = all_atoms_dict.get((chain, resseq), [])
        aa = AA3.get(resname, 'X')
        aa_codes.append(aa)
        for a in atoms_here:
            if a['name'] == 'CA':
                ca_coords.append([a['x'], a['y'], a['z']])
                break

    n = len(aa_codes)
    if n == 0:
        return {}

    f_hydro   = sum(1 for a in aa_codes if a in HYDROPHOBIC) / n
    f_polar   = sum(1 for a in aa_codes if a in POLAR)       / n
    f_pos     = sum(1 for a in aa_codes if a in CHARGED_POS) / n
    f_neg     = sum(1 for a in aa_codes if a in CHARGED_NEG) / n
    f_arom    = sum(1 for a in aa_codes if a in AROMATIC)    / n

    ca = np.array(ca_coords)
    vol = 0.0
    if len(ca) >= 4:
        try:
            hull = ConvexHull(ca)
            vol  = hull.volume
        except Exception:
            vol = 0.0

    return dict(n_res=n, f_hydro=round(f_hydro,2), f_polar=round(f_polar,2),
                f_pos=round(f_pos,2),   f_neg=round(f_neg,2),
                f_arom=round(f_arom,2), vol_hull=round(vol,0))


# ---- Build atom lookup dicts for each structure ----

# CRBN
crbn_path = "/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb"
crbn_atoms_dict = {}
with open(crbn_path) as fh:
    for line in fh:
        rec = line[:6].strip()
        if rec != 'ATOM': continue
        try:
            name=line[12:16].strip(); resn=line[17:20].strip()
            chain=line[21]; resseq=int(line[22:26])
            x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
            crbn_atoms_dict.setdefault((chain,resseq),[]).append(
                dict(name=name,resn=resn,x=x,y=y,z=z))
        except: pass

# dpCDK2-CCNE1 (apo)
apo_path = "/home/ubuntu/rayca-artifacts/0e2dd53329c8b2ef8e1bf379/files/dpCDK2-CCNE1_without ligand.pdb"
apo_atoms_dict = {}
with open(apo_path) as fh:
    for line in fh:
        rec = line[:6].strip()
        if rec != 'ATOM': continue
        try:
            name=line[12:16].strip(); resn=line[17:20].strip()
            chain=line[21]; resseq=int(line[22:26])
            x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
            apo_atoms_dict.setdefault((chain,resseq),[]).append(
                dict(name=name,resn=resn,x=x,y=y,z=z))
        except: pass

# CDK2-CCNE (holo, CTX)
holo_path = "/home/ubuntu/rayca-artifacts/5e3a2eab5918b528d391eb88/files/CDK2-CCNE.pdb"
holo_atoms_dict = {}
with open(holo_path) as fh:
    for line in fh:
        rec = line[:6].strip()
        if rec != 'ATOM': continue
        try:
            name=line[12:16].strip(); resn=line[17:20].strip()
            chain=line[21]; resseq=int(line[22:26])
            x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
            holo_atoms_dict.setdefault((chain,resseq),[]).append(
                dict(name=name,resn=resn,x=x,y=y,z=z))
        except: pass

print("Atom dicts: CRBN", len(crbn_atoms_dict), "| apo CDK2", len(apo_atoms_dict), "| holo CDK2", len(holo_atoms_dict))
