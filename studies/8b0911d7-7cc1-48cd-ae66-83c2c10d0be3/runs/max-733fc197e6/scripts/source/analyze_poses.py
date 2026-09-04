#!/usr/bin/env python3
"""
Analyze PDBQT pose files, extract per-pose coordinates,
write protein-ligand complex PDB files, calculate interaction distances.
Run after all *_poses.pdbqt files are available.
"""
import os, re, json, math
import numpy as np

WORKDIR = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc'
LIG_DIR = os.path.join(WORKDIR, 'ligands')
FIG_DIR = os.path.join(WORKDIR, 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

RECEPTOR_PDB = os.path.join(WORKDIR, '9C56_receptor.pdb')

# Pocket residues from FRJ co-crystal analysis
POCKET_RESIDUES = {188, 189, 190, 193, 194, 197, 198, 201, 274, 275, 277, 278, 279, 280}
POCKET_LABELS = {
    188: 'SER188', 189: 'PRO189', 190: 'ALA190', 193: 'LEU193',
    194: 'ASN194', 197: 'PHE197', 198: 'LYS198', 201: 'GLU201',
    274: 'GLU274', 275: 'GLY275', 277: 'LYS277', 278: 'CYS278',
    279: 'ILE279', 280: 'LYS280'
}

# Load receptor atoms
def load_receptor_atoms(pdb_path):
    atoms = []
    with open(pdb_path) as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    aname = line[12:16].strip()
                    rname = line[17:20].strip()
                    rnum  = int(line[22:26].strip())
                    x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
                    atoms.append({'name':aname,'res':rname,'rnum':rnum,'x':x,'y':y,'z':z})
                except: pass
    return atoms

rec_atoms = load_receptor_atoms(RECEPTOR_PDB)
rec_coords = np.array([[a['x'],a['y'],a['z']] for a in rec_atoms])

def parse_pdbqt_poses(pdbqt_path):
    """Parse multi-model PDBQT, return list of (score, atoms[]) per pose."""
    poses = []
    current_score = None
    current_atoms = []
    in_model = False
    with open(pdbqt_path) as f:
        for line in f:
            if line.startswith('MODEL'):
                in_model = True
                current_atoms = []
                current_score = None
            elif line.startswith('REMARK VINA RESULT:'):
                parts = line.split()
                try: current_score = float(parts[3])
                except: pass
            elif line.startswith('ATOM') or line.startswith('HETATM'):
                if in_model:
                    try:
                        x,y,z = float(line[30:38]),float(line[38:46]),float(line[46:54])
                        el = line[12:16].strip()
                        current_atoms.append((el,x,y,z))
                    except: pass
            elif line.startswith('ENDMDL'):
                if current_atoms:
                    poses.append({'score': current_score, 'atoms': current_atoms})
                in_model = False
    return poses

def find_contacts(pose_atoms, rec_atoms, rec_coords, cutoff=4.5):
    """Find receptor residues within cutoff of any ligand heavy atom."""
    lig_coords = np.array([[a[1],a[2],a[3]] for a in pose_atoms if not a[0].startswith('H')])
    contacts = {}
    for lc in lig_coords:
        dists = np.linalg.norm(rec_coords - lc, axis=1)
        for i in np.where(dists < cutoff)[0]:
            ra = rec_atoms[i]
            if not ra['name'].startswith('H'):
                key = (ra['rnum'], ra['res'])
                if key not in contacts:
                    contacts[key] = []
                contacts[key].append(float(dists[i]))
    return {k: min(v) for k,v in contacts.items()}

def write_complex_pdb(receptor_pdb, pose_atoms, out_path, lig_id, pose_num):
    """Write receptor + ligand pose as PDB for visualization."""
    with open(receptor_pdb) as f:
        rec_lines = [l for l in f if l.startswith('ATOM')]
    with open(out_path, 'w') as f:
        f.write(f'REMARK Protein-ligand complex: {lig_id} pose {pose_num}\n')
        for line in rec_lines:
            f.write(line)
        f.write('TER\n')
        for i, (el, x, y, z) in enumerate(pose_atoms, 1):
            f.write(f'HETATM{i:5d}  {el:<4s}LIG A 901    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           {el[0]}\n')
        f.write('END\n')

# Process all available PDBQT files
all_results = []
for lig_id in ['EDS00760714-1', 'EDS00760714-2', 'EDS00760778-1', 'EDS00760778-2']:
    pdbqt_path = os.path.join(LIG_DIR, f'{lig_id}_poses.pdbqt')
    if not os.path.exists(pdbqt_path):
        print(f'SKIP {lig_id}: no poses file')
        continue

    print(f'\nProcessing {lig_id}...')
    poses = parse_pdbqt_poses(pdbqt_path)
    print(f'  {len(poses)} poses')

    pose_data = []
    for pi, pose in enumerate(poses[:5], 1):
        score = pose['score']
        contacts = find_contacts(pose['atoms'], rec_atoms, rec_coords, cutoff=4.5)
        pocket_contacts = {k:v for k,v in contacts.items() if k[0] in POCKET_RESIDUES}

        # Write complex PDB for best pose (pose 1)
        if pi == 1:
            complex_path = os.path.join(FIG_DIR, f'{lig_id}_best_complex.pdb')
            write_complex_pdb(RECEPTOR_PDB, pose['atoms'], complex_path, lig_id, pi)
            print(f'  Complex PDB: {complex_path}')

        print(f'  Pose {pi}: score={score} | pocket contacts: {[POCKET_LABELS.get(k[0],str(k)) for k in pocket_contacts]}')
        pose_data.append({
            'pose': pi, 'score_kcal_mol': score,
            'pocket_contacts': {f"{k[1]}{k[0]}": round(v,2) for k,v in pocket_contacts.items()},
            'total_contacts': len(contacts)
        })

    # Load result JSON if available
    res_json = os.path.join(LIG_DIR, f'{lig_id}_results.json')
    best_score = poses[0]['score'] if poses else None
    if os.path.exists(res_json):
        with open(res_json) as f:
            rj = json.load(f)
        best_score = rj.get('best_affinity_kcal_mol', best_score)

    all_results.append({
        'id': lig_id, 'best_score': best_score, 'poses': pose_data,
        'num_poses': len(poses)
    })

# Save analysis
out = os.path.join(WORKDIR, 'pose_analysis.json')
with open(out, 'w') as f:
    json.dump(all_results, f, indent=2)
print(f'\nAnalysis saved: {out}')
print('DONE')
