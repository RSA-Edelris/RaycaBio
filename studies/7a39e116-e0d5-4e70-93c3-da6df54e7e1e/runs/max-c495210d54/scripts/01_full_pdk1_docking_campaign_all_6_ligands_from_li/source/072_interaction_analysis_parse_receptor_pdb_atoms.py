
# Interaction analysis: parse receptor PDB atoms
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

def parse_receptor_atoms(pdb_path):
    """Returns list of dicts: {resname, resnum, chain, atomname, element, xyz}"""
    atoms = []
    with open(pdb_path) as fh:
        for ln in fh:
            if not (ln.startswith('ATOM') or ln.startswith('HETATM')):
                continue
            aname  = ln[12:16].strip()
            resname= ln[17:20].strip()
            chain  = ln[21].strip()
            resnum = int(ln[22:26].strip())
            try:
                x = float(ln[30:38]); y = float(ln[38:46]); z = float(ln[46:54])
            except:
                continue
            elem = ln[76:78].strip() if len(ln) > 76 else aname[0]
            atoms.append({'resname': resname, 'resnum': resnum, 'chain': chain,
                          'aname': aname, 'elem': elem.upper(),
                          'xyz': np.array([x, y, z])})
    return atoms

rec_atoms = parse_receptor_atoms(f"{ART}/1Z5M_receptor_pH7.4.pdb")
print(f"Receptor: {len(rec_atoms)} atoms")

# Build numpy array for fast distance computation
rec_xyz   = np.array([a['xyz'] for a in rec_atoms])
rec_elem  = [a['elem'] for a in rec_atoms]
rec_resid = [f"{a['resname']}{a['resnum']}{a['chain']}" for a in rec_atoms]
rec_aname = [a['aname'] for a in rec_atoms]

# polar atoms (N, O, S) for H-bond analysis
POLAR = {'N', 'O', 'S'}
APOLAR_C = 'C'  # carbon without adjacent N/O counts as hydrophobic

print("Sample residues near box center (-4.3, 43.7, 44.5):")
cx, cy, cz = -4.283, 43.728, 44.510
dists = np.linalg.norm(rec_xyz - np.array([cx, cy, cz]), axis=1)
nearby_idx = np.where(dists < 8.0)[0]
seen = set()
for i in nearby_idx:
    rid = rec_resid[i]
    if rid not in seen:
        seen.add(rid)
        print(f"  {rid:12s} ({rec_atoms[i]['resname']:3s})")
