
import numpy as np
from scipy.spatial import ConvexHull

AA3 = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
    'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
    'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'
}
HYDROPHOBIC = set('AILVMFYWP')
POLAR       = set('STNQ')
CHARGED_POS = set('KRH')
CHARGED_NEG = set('DE')
AROMATIC    = set('FYW')

def residue_descriptors(res_triples, all_atoms_dict):
    ca_coords, aa_codes = [], []
    for chain, resseq, resname in res_triples:
        aa = AA3.get(resname, 'X')
        aa_codes.append(aa)
        for a in all_atoms_dict.get((chain, resseq), []):
            if a['name'] == 'CA':
                ca_coords.append([a['x'], a['y'], a['z']])
                break
    n = len(aa_codes)
    if n == 0:
        return {}
    f_hydro = sum(1 for a in aa_codes if a in HYDROPHOBIC) / n
    f_polar = sum(1 for a in aa_codes if a in POLAR)       / n
    f_pos   = sum(1 for a in aa_codes if a in CHARGED_POS) / n
    f_neg   = sum(1 for a in aa_codes if a in CHARGED_NEG) / n
    f_arom  = sum(1 for a in aa_codes if a in AROMATIC)    / n
    ca = np.array(ca_coords)
    vol = 0.0
    if len(ca) >= 4:
        try:
            vol = ConvexHull(ca).volume
        except Exception:
            pass
    return dict(n_res=n, f_hydro=round(f_hydro,2), f_polar=round(f_polar,2),
                f_pos=round(f_pos,2), f_neg=round(f_neg,2),
                f_arom=round(f_arom,2), vol_hull=round(vol,0))
