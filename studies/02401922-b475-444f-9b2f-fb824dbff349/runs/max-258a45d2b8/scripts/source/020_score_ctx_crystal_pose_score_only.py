
# Score CTX in crystal pose (score_only)
ctx_score_cmd = [
    'vina',
    '--receptor', 'receptor.pdbqt',
    '--ligand',   'ctx_ref.pdbqt',
    '--center_x', str(BOX_X), '--center_y', str(BOX_Y), '--center_z', str(BOX_Z),
    '--size_x',   str(BOX_W), '--size_y',   str(BOX_H), '--size_z',   str(BOX_D),
    '--score_only',
    '--seed', '42'
]

r_score = subprocess.run(ctx_score_cmd, capture_output=True, text=True, cwd=WS)
print(r_score.stdout)
if r_score.returncode != 0:
    print("STDERR:", r_score.stderr[:500])

# Extract Vina score from output
import re
match = re.search(r'Estimated Free Energy of Binding\s*:\s*([\-\d\.]+)', r_score.stdout)
if match:
    ctx_vina_score = float(match.group(1))
    print(f"\nCTX crystal pose Vina score: {ctx_vina_score} kcal/mol")
else:
    # Try the short table format
    lines = [l for l in r_score.stdout.split('\n') if 'Affinity' in l or re.match(r'\s+1\s+', l)]
    print("Score lines:", lines)
