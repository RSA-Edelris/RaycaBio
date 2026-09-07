"""Distance-based protein-ligand interaction analysis (heavy atoms only)."""
import numpy as np
from scipy.spatial.distance import cdist

HBOND_CUTOFF = 3.5       # Å, N/O donor-acceptor
HYDROPHOB_CUTOFF = 4.5   # Å, C-C
AROMATIC_CUTOFF = 5.5    # Å, ring centroid to ligand C/N
VDW_CUTOFF = 4.0         # Å, any-any (general contact)

AROMATIC_RES = {'PHE', 'TYR', 'TRP', 'HIS'}
HBOND_ELEMS  = {'N', 'O', 'F'}
HYDROPHOB_ELEMS = {'C', 'S'}

# Known CRBN-TBD residues from literature (4CI2 chain B numbering)
KNOWN_SITE = {351:'ASN', 374:'GLN', 377:'GLN', 378:'HIS', 380:'TRP',
              391:'ILE', 427:'GLY', 442:'CYS'}


def parse_pdb_atoms(pdb_path, exclude_hetatm=True):
    coords, elems, rnames, rnums, anames, chains = [], [], [], [], [], []
    with open(pdb_path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec == 'ATOM' or (rec == 'HETATM' and not exclude_hetatm):
                try:
                    x = float(line[30:38]); y = float(line[38:46]); z = float(line[46:54])
                    elem  = line[76:78].strip() if len(line) > 76 else ''
                    if not elem:
                        elem = line[12:16].strip().lstrip('0123456789')[:1]
                    if elem in ('H','D'): continue          # skip hydrogens
                    coords.append([x, y, z])
                    elems.append(elem)
                    rnames.append(line[17:20].strip())
                    rnums.append(int(line[22:26].strip()))
                    anames.append(line[12:16].strip())
                    chains.append(line[21].strip())
                except:
                    pass
    return {k: np.array(v) for k, v in zip(
        ['coords','elements','res_names','res_nums','atom_names','chains'],
        [coords, elems, rnames, rnums, anames, chains])}


def parse_sdf_atoms(sdf_path):
    coords, elems = [], []
    with open(sdf_path) as f:
        lines = f.readlines()
    for i, ln in enumerate(lines):
        if 'V2000' in ln or 'V3000' in ln:
            try:
                n_atoms = int(ln[:3].strip())
                for j in range(i+1, i+1+n_atoms):
                    parts = lines[j].split()
                    if len(parts) >= 4 and parts[3] not in ('H','D'):
                        coords.append([float(parts[0]), float(parts[1]), float(parts[2])])
                        elems.append(parts[3])
            except:
                pass
            break
    return {'coords': np.array(coords) if coords else np.empty((0,3)),
            'elements': np.array(elems)}


def get_contacts(rec, lig_coords, lig_elems):
    """Return list of contact dicts for one ligand pose."""
    if len(lig_coords) == 0:
        return []
    D = cdist(rec['coords'], lig_coords)          # (N_prot, N_lig)
    contacts = []

    for pi in range(len(rec['coords'])):
        re = rec['elements'][pi]
        rn = rec['res_names'][pi]
        rnum = int(rec['res_nums'][pi])
        an = rec['atom_names'][pi]
        res_label = f"{rn}{rnum}"

        for li in range(len(lig_coords)):
            le = lig_elems[li]
            d  = D[pi, li]

            # H-bond: N or O on both sides
            if d <= HBOND_CUTOFF and re in HBOND_ELEMS and le in HBOND_ELEMS:
                contacts.append({'type': 'H-bond', 'res': res_label,
                                  'prot_atom': an, 'dist': round(float(d),2)})

            # Hydrophobic
            elif d <= HYDROPHOB_CUTOFF and re == 'C' and le == 'C':
                contacts.append({'type': 'Hydrophobic', 'res': res_label,
                                  'prot_atom': an, 'dist': round(float(d),2)})

            # General VdW (not already categorised)
            elif d <= VDW_CUTOFF:
                contacts.append({'type': 'VdW', 'res': res_label,
                                  'prot_atom': an, 'dist': round(float(d),2)})

    # Deduplicate to one entry per (type, res) — keep shortest distance
    best = {}
    for c in contacts:
        key = (c['type'], c['res'])
        if key not in best or c['dist'] < best[key]['dist']:
            best[key] = c
    return list(best.values())


def summarise(contacts):
    """Count by type; list unique residues per type."""
    from collections import defaultdict
    by_type = defaultdict(set)
    for c in contacts:
        by_type[c['type']].add(c['res'])
    return {t: sorted(res) for t, res in by_type.items()}
