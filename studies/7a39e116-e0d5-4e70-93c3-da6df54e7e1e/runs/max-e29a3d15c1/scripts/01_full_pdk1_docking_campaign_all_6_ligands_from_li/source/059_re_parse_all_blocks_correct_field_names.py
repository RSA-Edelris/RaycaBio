
from rdkit.Chem import SDWriter

# Re-parse all blocks with correct field names
pose_table = []
for i, blk in enumerate(blocks):
    lines = blk.splitlines()
    mol_name = lines[0].strip()
    props = {}
    for j, ln in enumerate(lines):
        m = re.match(r'>  <(.+?)>', ln)
        if m:
            key = m.group(1)
            val = lines[j+1].strip() if j+1 < len(lines) else ''
            props[key] = val
    
    aff       = float(props.get('minimizedAffinity', 'nan'))
    cnn_score = float(props.get('CNNscore',         'nan'))
    cnn_aff   = float(props.get('CNNaffinity',      'nan'))
    cnn_vs    = float(props.get('CNN_VS',           'nan'))
    pic50     = props.get('pIC50 PDK', '')
    
    # Pose rank within this ligand (reset per ligand)
    same = [p for p in pose_table if p['mol_name'] == mol_name]
    rank = len(same) + 1
    
    pose_table.append({
        'global_idx': i+1, 'mol_name': mol_name, 'rank': rank,
        'affinity': aff, 'cnn_score': cnn_score,
        'cnn_aff': cnn_aff, 'cnn_vs': cnn_vs,
        'pic50': pic50, 'block': blk, 'props': props
    })

# Print score table
print(f"{'Molecule':22s}  {'Rank':>4}  {'Affinity':>10}  {'CNNscore':>10}  {'CNNaff':>9}  {'pIC50':>6}")
print("-"*75)
for r in pose_table:
    print(f"{r['mol_name']:22s}  {r['rank']:>4}  {r['affinity']:>10.4f}  "
          f"{r['cnn_score']:>10.4f}  {r['cnn_aff']:>9.4f}  {r['pic50']:>6}")

# Save best pose per ligand summary
print("\n=== BEST POSE PER LIGAND (rank 1) ===")
best = {r['mol_name']: r for r in pose_table if r['rank'] == 1}
for name, r in best.items():
    print(f"  {name:22s}  aff={r['affinity']:.4f}  CNN={r['cnn_score']:.4f}  "
          f"CNNaff={r['cnn_aff']:.4f}  pIC50={r['pic50']}")
