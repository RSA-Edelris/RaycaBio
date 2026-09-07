
import json

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

mmgbsa_results = {
    'EDS01357518_ent1': -19.6106,
    'EDS01357518_ent2': -16.9384,
    'EDS01806218_ent1': 8.4854,
    'EDS01806218_ent2': 16.6724,
    'EDS01889984':     47.843,
}

meta = {
    'EDS01357518_ent1': ('EDS01357518', 'S',      'Thiazolyl-piperidine'),
    'EDS01357518_ent2': ('EDS01357518', 'R',      'Thiazolyl-piperidine'),
    'EDS01806218_ent1': ('EDS01806218', '1R,2R',  'Cyclopropyl-amide'),
    'EDS01806218_ent2': ('EDS01806218', '1S,2S',  'Cyclopropyl-amide'),
    'EDS01889984':      ('EDS01889984', '—',       'Sulfonyl-piperazine'),
}

with open(f'{WD}/final_results.json') as fh:
    scores = json.load(fh)

rows = []
for cid in ['EDS01357518_ent1','EDS01357518_ent2',
            'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']:
    s = scores[cid]
    parent, stereo, scaffold = meta[cid]
    rows.append({
        'cid': cid, 'parent': parent, 'stereo': stereo, 'scaffold': scaffold,
        'vina': s['vina'], 'dG_cnn': s['dG_cnn'],
        'cnn_pose': s['cnn_pose'],
        'dG_mmgbsa': mmgbsa_results[cid],
    })

# Print table
print(f"{'Compound':<22} {'Stereo':<8} {'Vina':>10} {'ΔG_CNN':>12} {'ΔG_MM-GBSA†':>14}")
print("-" * 70)
for r in rows:
    flag = " ⚑" if r['dG_mmgbsa'] > 0 else ""
    print(f"{r['cid']:<22} {r['stereo']:<8} {r['vina']:>10.2f} {r['dG_cnn']:>12.2f} {r['dG_mmgbsa']:>12.2f}{flag}")

print()
print("† Single-point MM-GBSA (OBC2/igb=5, mbondi2, 0.15 M NaCl).")
print("  Positive values (⚑) indicate strained poses; minimization required.")
