
import numpy as np
from scipy.spatial.distance import cdist
import os, re, json

# ── parse receptor PDB (protein only, no ligand, with H) ─────────────────────
def parse_pdb_atoms(pdb_path, exclude_hetatm=True):
    """Returns dict with arrays: coords, elements, residue_names, residue_nums, atom_names, chain_ids"""
    coords, elems, res_names, res_nums, atom_names, chains = [], [], [], [], [], []
    with open(pdb_path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec == 'ATOM' or (rec == 'HETATM' and not exclude_hetatm):
                try:
                    x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                    elem = line[76:78].strip() if len(line) > 76 else line[12:16].strip().lstrip('0123456789')[:1]
                    aname = line[12:16].strip()
                    rname = line[17:20].strip()
                    rnum  = int(line[22:26].strip())
                    cid   = line[21].strip()
                    coords.append([x, y, z])
                    elems.append(elem)
                    res_names.append(rname)
                    res_nums.append(rnum)
                    atom_names.append(aname)
                    chains.append(cid)
                except:
                    pass
    return {
        'coords':    np.array(coords),
        'elements':  np.array(elems),
        'res_names': np.array(res_names),
        'res_nums':  np.array(res_nums),
        'atom_names':np.array(atom_names),
        'chains':    np.array(chains),
    }

def parse_sdf_atoms(sdf_path):
    """Returns coords and elements for first molecule in SDF (V2000)"""
    coords, elems = [], []
    with open(sdf_path) as f:
        lines = f.readlines()
    # find counts line
    for i, ln in enumerate(lines):
        if 'V2000' in ln or 'V3000' in ln:
            try:
                n_atoms = int(ln[:3])
                for j in range(i+1, i+1+n_atoms):
                    parts = lines[j].split()
                    if len(parts) >= 4:
                        coords.append([float(parts[0]), float(parts[1]), float(parts[2])])
                        elems.append(parts[3])
            except:
                pass
            break
    return {'coords': np.array(coords), 'elements': np.array(elems)}

# Load receptor once
rec = parse_pdb_atoms(RECEPTOR, exclude_hetatm=True)
# Remove hydrogens from receptor for heavy-atom contacts
heavy_mask = np.array([e not in ('H','D') for e in rec['elements']])
rec_coords  = rec['coords'][heavy_mask]
rec_elems   = rec['elements'][heavy_mask]
rec_rnames  = rec['res_names'][heavy_mask]
rec_rnums   = rec['res_nums'][heavy_mask]
rec_anames  = rec['atom_names'][heavy_mask]

print(f"Receptor heavy atoms: {len(rec_coords)}")

# Test on one ligand
test = parse_sdf_atoms(f"{WORK}/best_poses/EDEL-CRBN-0001_pose1.sdf")
print(f"Ligand EDEL-CRBN-0001: {len(test['coords'])} heavy atoms, elems: {set(test['elements'])}")
