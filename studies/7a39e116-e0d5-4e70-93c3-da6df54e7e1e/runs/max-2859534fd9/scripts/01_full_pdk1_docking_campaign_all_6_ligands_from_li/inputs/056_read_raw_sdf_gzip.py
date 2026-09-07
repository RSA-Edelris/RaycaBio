
import gzip, re, json

# Read raw SDF from gzip
sdf_gz = f"{ART}/gnina_docked.sdf.gz"
with gzip.open(sdf_gz, 'rt') as fh:
    raw = fh.read()

print(f"SDF size: {len(raw):,} chars")
print(f"Number of $$$$ records: {raw.count('$$$$')}")

# Parse blocks
blocks = [b.strip() for b in raw.split('$$$$') if b.strip()]
print(f"Blocks parsed: {len(blocks)}\n")

pose_records = []
for i, blk in enumerate(blocks):
    lines = blk.splitlines()
    mol_name = lines[0].strip() if lines else f"pose_{i+1}"
    
    # Extract SDF properties
    props = {}
    for j, ln in enumerate(lines):
        m = re.match(r'>  <(.+?)>', ln)
        if m:
            key = m.group(1)
            val = lines[j+1].strip() if j+1 < len(lines) else ''
            props[key] = val
    
    aff = props.get('minimizedAffinity', props.get('CNNaffinity', props.get('Affinity', '?')))
    cnn_pose = props.get('CNNscore', props.get('cnn_pose_score', '?'))
    cnn_aff  = props.get('CNNaffinity', '?')
    
    pose_records.append({
        'idx': i+1, 'mol_name': mol_name,
        'affinity': aff, 'cnn_pose': cnn_pose, 'cnn_aff': cnn_aff,
        'props': props, 'block': blk
    })

# Print all poses grouped by molecule
print(f"{'Pose':>4}  {'Molecule':22s}  {'Affinity':>10}  {'CNN_pose':>10}  {'CNN_aff':>10}")
print("-"*65)
for r in pose_records:
    print(f"{r['idx']:>4}  {r['mol_name']:22s}  {r['affinity']:>10}  "
          f"{r['cnn_pose']:>10}  {r['cnn_aff']:>10}")
