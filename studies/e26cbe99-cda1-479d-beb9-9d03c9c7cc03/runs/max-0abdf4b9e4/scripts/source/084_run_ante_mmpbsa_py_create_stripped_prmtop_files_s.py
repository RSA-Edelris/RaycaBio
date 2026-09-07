
import subprocess, os

# ── Run ante-MMPBSA.py to create stripped prmtop files ───────────────────
# -s strips solvent+ions, -n is the ligand mask, --radii for GB
r = subprocess.run([
    'ante-MMPBSA.py',
    '-p', f'{MD_DIR}/complex.prmtop',
    '-c', f'{MD_DIR}/complex_nowater.prmtop',    # complex without solvent
    '-r', f'{MD_DIR}/receptor.prmtop',            # receptor only
    '-l', f'{MD_DIR}/ligand.prmtop',              # ligand only
    '-s', ':WAT,Cl-',                              # strip water + ions
    '-n', ':LIG',                                  # ligand residue mask
    '--radii', 'mbondi2',                          # mbondi2 radii for GBSA
], capture_output=True, text=True, cwd=MD_DIR)

print("ante-MMPBSA.py stdout:", r.stdout[-500:] if r.stdout else "(none)")
if r.returncode != 0:
    print("STDERR:", r.stderr[-800:])

for fname in ['complex_nowater.prmtop', 'receptor.prmtop', 'ligand.prmtop']:
    path = f'{MD_DIR}/{fname}'
    sz = os.path.getsize(path) if os.path.exists(path) else None
    print(f"  {fname}: {'OK ' + str(sz) + ' bytes' if sz else 'MISSING'}")
