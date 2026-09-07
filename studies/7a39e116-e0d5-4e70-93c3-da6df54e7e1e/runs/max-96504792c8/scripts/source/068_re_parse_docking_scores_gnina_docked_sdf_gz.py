
import gzip, re

# Re-parse docking scores from gnina_docked.sdf.gz
ligand_names = ['EL2003A-A2U1', 'EL2003A', 'EL2003A-A4U1', 'BX912', 'EL5001A', 'EL5003A']
pic50_map = {'EL2003A-A2U1': 7.6, 'EL2003A': 7.5, 'EL2003A-A4U1': 7.5,
             'BX912': 6.0, 'EL5001A': 6.5, 'EL5003A': 6.8}

pose_table = []
with gzip.open(f"{ART}/gnina_docked.sdf.gz", 'rt') as fh:
    lines = fh.readlines()

mol_lines, mol_name, rank_counter = [], {}, {}
in_mol = False
current_name = None

i = 0
while i < len(lines):
    ln = lines[i]
    # Molecule name is the first non-blank line of each record
    if not in_mol:
        name_candidate = ln.strip()
        if name_candidate:
            current_name = name_candidate
            in_mol = True
            mol_lines = [ln]
    else:
        mol_lines.append(ln)
        if ln.strip() == '$$$$':
            # parse properties from mol_lines
            props = {}
            for j, ml in enumerate(mol_lines):
                m = re.match(r'> {1,2}<(.+?)>', ml)
                if m:
                    key = m.group(1)
                    if j+1 < len(mol_lines):
                        props[key] = mol_lines[j+1].strip()
            # map name to base ligand
            base = current_name.split('_pose')[0] if '_pose' in current_name else current_name
            # find which ligand this belongs to
            matched = None
            for lig in ligand_names:
                if lig in current_name or current_name == lig:
                    matched = lig
                    break
            if matched is None:
                matched = base
            rank_counter[matched] = rank_counter.get(matched, 0) + 1
            rank = rank_counter[matched]
            pose_table.append({
                'mol_name': matched,
                'rank': rank,
                'pic50': pic50_map.get(matched, float('nan')),
                'affinity': float(props.get('minimizedAffinity', 'nan')),
                'cnn_score': float(props.get('CNNscore', 'nan')),
                'cnn_aff': float(props.get('CNNaffinity', 'nan')),
            })
            in_mol = False
            mol_lines = []
            current_name = None
    i += 1

print(f"Parsed {len(pose_table)} poses")
for r in pose_table:
    print(f"  {r['mol_name']:22s} rank={r['rank']} aff={r['affinity']:.4f} CNN={r['cnn_score']:.4f} CNNaff={r['cnn_aff']:.4f}")
