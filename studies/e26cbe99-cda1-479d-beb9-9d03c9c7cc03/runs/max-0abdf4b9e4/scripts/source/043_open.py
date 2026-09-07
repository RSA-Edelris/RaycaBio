
WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

# ── Load all data ──────────────────────────────────────────────────────────────
with open(f'{WD}/PB-20260903-4CI2_receptor_trimmed_fixed.pdb') as f:
    receptor_pdb = f.read()

compounds = [
    ('EDS01357518_ent1',  'EDS01357518',  '(R)',      '#f97316'),
    ('EDS01357518_ent2',  'EDS01357518',  '(S)',      '#eab308'),
    ('EDS01806218_ent1',  'EDS01806218',  '(1R,2R)',  '#3b82f6'),
    ('EDS01806218_ent2',  'EDS01806218',  '(1S,2S)',  '#10b981'),
    ('EDS01889984',       'EDS01889984',  '',         '#a855f7'),
]

scores = {
    "EDS01357518_ent1": {"vina": -7.52, "cnn_pose": 0.558, "pKi": 7.03, "dG": -9.58},
    "EDS01357518_ent2": {"vina": -8.09, "cnn_pose": 0.769, "pKi": 6.98, "dG": -9.52},
    "EDS01806218_ent1": {"vina": -6.81, "cnn_pose": 0.304, "pKi": 6.33, "dG": -8.63},
    "EDS01806218_ent2": {"vina": -9.08, "cnn_pose": 0.740, "pKi": 7.43, "dG": -10.13},
    "EDS01889984":      {"vina": -6.63, "cnn_pose": 0.495, "pKi": 6.99, "dG": -9.53},
}

poses_data = {}
for (cid, *_) in compounds:
    with open(f'{WD}/poses_{cid}.sdf') as f:
        content = f.read()
    blocks = [b.strip() + '\n$$$$' for b in content.split('$$$$') if b.strip()]
    poses_data[cid] = blocks

# ── JS-escape helper ──────────────────────────────────────────────────────────
def js_str(s):
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

# ── Build JS data blobs ────────────────────────────────────────────────────────
receptor_js = js_str(receptor_pdb)
poses_js_parts = []
for (cid, *_) in compounds:
    blocks_js = ',\n'.join(f'`{js_str(b)}`' for b in poses_data[cid])
    poses_js_parts.append(f'  "{cid}": [{blocks_js}]')
poses_js = '{\n' + ',\n'.join(poses_js_parts) + '\n}'

import json
scores_js = json.dumps(scores, indent=2)
compounds_js = json.dumps([
    {'id': c[0], 'parent': c[1], 'stereo': c[2], 'color': c[3]}
    for c in compounds
], indent=2)

print("Data prepared:")
print(f"  Receptor: {len(receptor_pdb):,} chars")
for cid, *_ in compounds:
    total = sum(len(b) for b in poses_data[cid])
    print(f"  {cid}: {len(poses_data[cid])} poses, {total:,} chars")
