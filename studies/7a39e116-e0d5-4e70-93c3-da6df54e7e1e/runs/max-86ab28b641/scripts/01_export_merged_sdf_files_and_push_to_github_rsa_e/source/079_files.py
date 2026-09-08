
import re, glob, json, os

ART = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

ligand_names = ['EL2003A-A2U1', 'EL2003A', 'EL2003A-A4U1', 'BX912', 'EL5001A', 'EL5003A']
pic50_map    = {'EL2003A-A2U1': 7.6, 'EL2003A': 7.5, 'EL2003A-A4U1': 7.5,
                'BX912': 6.0, 'EL5001A': 6.5, 'EL5003A': 6.8}

# Rebuild pose_table and full_table from JSON files (context may have dropped them)
import gzip
pose_table = []
rank_counter = {}
ligand_names_sorted = sorted(ligand_names, key=len, reverse=True)

with gzip.open(f"{ART}/gnina_docked.sdf.gz", 'rt') as fh:
    lines = fh.readlines()

in_mol, current_name, mol_lines = False, None, []
for ln in lines:
    if not in_mol:
        cand = ln.strip()
        if cand:
            current_name = cand; in_mol = True; mol_lines = [ln]
    else:
        mol_lines.append(ln)
        if ln.strip() == '$$$$':
            props = {}
            for j, ml in enumerate(mol_lines):
                m = re.match(r'> {1,2}<(.+?)>', ml)
                if m and j+1 < len(mol_lines):
                    props[m.group(1)] = mol_lines[j+1].strip()
            matched = next((l for l in ligand_names_sorted if current_name.startswith(l)), current_name)
            rank_counter[matched] = rank_counter.get(matched, 0) + 1
            pose_table.append({'mol_name': matched, 'rank': rank_counter[matched],
                               'affinity': float(props.get('minimizedAffinity','nan')),
                               'cnn_score': float(props.get('CNNscore','nan')),
                               'cnn_aff':   float(props.get('CNNaffinity','nan')),
                               'mol_lines': list(mol_lines)})
            in_mol = False; mol_lines = []; current_name = None

# Load GBSA per-pose results
gbsa_by_lig = {}
for jpath in sorted(glob.glob(f"{ART}/gbsa_*.json")):
    lig = os.path.basename(jpath).replace('gbsa_','').replace('.json','')
    with open(jpath) as fh:
        gbsa_by_lig[lig] = json.load(fh).get('results', [])

# Merge into full_table with mmgbsa
full_table = []
for row in pose_table:
    lig = row['mol_name']; rank = row['rank']
    gb = gbsa_by_lig.get(lig, [])
    gb_row = gb[rank-1] if rank-1 < len(gb) else {}
    full_table.append({**row,
        'vdw':    float(gb_row.get('Van der Waals','nan')),
        'elec':   float(gb_row.get('Electrostatic','nan')),
        'polar':  float(gb_row.get('Polar Solvation','nan')),
        'npsolv': float(gb_row.get('Non-Polar Solvation','nan')),
        'mmgbsa': float(gb_row.get('TOTAL','nan'))})

# Best pose per ligand by GBSA
best_poses = {}
for lig in ligand_names:
    rows = [r for r in full_table if r['mol_name'] == lig]
    best_poses[lig] = min(rows, key=lambda r: r['mmgbsa'])

print(f"pose_table: {len(pose_table)}, full_table: {len(full_table)}")
for lig, bp in best_poses.items():
    print(f"  {lig:22s} best_rank={bp['rank']}  ΔG={bp['mmgbsa']:.3f}")
