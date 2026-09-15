
# Write helper to disk so it persists across calls
helper_code = '''
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
'''
import sys, os
with open('/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/drug_utils.py','w') as fh:
    fh.write(helper_code)
sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
from drug_utils import residue_descriptors

# ---- Define all pocket residue triples ----

# CRBN: residue->resname lookup
crbn_resname = {}
for (ch,rs), alist in crbn_atoms_dict.items():
    crbn_resname[(ch,rs)] = alist[0]['resn']

# CRBN main pocket (LVY contact shell, from previous analysis)
crbn_main_resids = {
    ('B',382):None,('B',383):None,('B',385):None,('B',386):None,
    ('B',388):None,('B',389):None,('B',390):None,('B',391):None,
    ('B',392):None,('B',393):None,('B',394):None,('B',396):None,
    ('B',399):None,('B',400):None,('B',401):None,('B',402):None,
    ('B',403):None,('B',404):None,('B',405):None,('B',406):None,
    ('B',407):None,('B',408):None,('B',409):None,('B',410):None,
    ('B',411):None,('B',412):None,('B',413):None,('B',414):None,
    ('B',415):None,('B',416):None,('B',417):None,('B',418):None,
    ('B',419):None,('B',420):None,('B',421):None,('B',422):None,
}
crbn_main = [(ch,rs, crbn_resname.get((ch,rs),'UNK')) for (ch,rs) in crbn_main_resids]

# CRBN allosteric (zinc shell + adjacent cavity, from previous analysis)
crbn_allo_resids = [('B',325),('B',328),('B',329),('B',330),('B',331),
                    ('B',332),('B',333),('B',334),('B',335),('B',336),
                    ('B',393),('B',394),('B',395),('B',396),('B',397)]
crbn_allo = [(ch,rs, crbn_resname.get((ch,rs),'UNK')) for (ch,rs) in crbn_allo_resids]

print("CRBN main pocket:", len(crbn_main), "residues")
print("CRBN allosteric :", len(crbn_allo),  "residues")
# Show resnames
for ch,rs,rn in crbn_main[:8]:
    print(f"  {rn}{rs}", end=' ')
print()
