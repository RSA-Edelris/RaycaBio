
# Fix: sort ligand_names longest-first so EL2003A-A4U1 matches before EL2003A
ligand_names_sorted = sorted(ligand_names, key=len, reverse=True)

pose_table = []
rank_counter = {}

with gzip.open(f"{ART}/gnina_docked.sdf.gz", 'rt') as fh:
    lines = fh.readlines()

in_mol = False
current_name = None
mol_lines = []

for ln in lines:
    if not in_mol:
        cand = ln.strip()
        if cand:
            current_name = cand
            in_mol = True
            mol_lines = [ln]
    else:
        mol_lines.append(ln)
        if ln.strip() == '$$$$':
            props = {}
            for j, ml in enumerate(mol_lines):
                m = re.match(r'> {1,2}<(.+?)>', ml)
                if m:
                    key = m.group(1)
                    if j+1 < len(mol_lines):
                        props[key] = mol_lines[j+1].strip()
            # longest-first match
            matched = None
            for lig in ligand_names_sorted:
                if lig == current_name or current_name.startswith(lig):
                    matched = lig
                    break
            if matched is None:
                matched = current_name
            rank_counter[matched] = rank_counter.get(matched, 0) + 1
            rank = rank_counter[matched]
            pose_table.append({
                'mol_name': matched, 'rank': rank,
                'pic50': pic50_map.get(matched, float('nan')),
                'affinity': float(props.get('minimizedAffinity', 'nan')),
                'cnn_score': float(props.get('CNNscore', 'nan')),
                'cnn_aff': float(props.get('CNNaffinity', 'nan')),
            })
            in_mol = False; mol_lines = []; current_name = None

# Verify counts
from collections import Counter
counts = Counter(r['mol_name'] for r in pose_table)
print("Pose counts per ligand:", dict(counts))
print(f"\nTotal: {len(pose_table)} poses")
for r in pose_table:
    print(f"  {r['mol_name']:22s} r{r['rank']} aff={r['affinity']:.3f} CNN={r['cnn_score']:.4f}")
