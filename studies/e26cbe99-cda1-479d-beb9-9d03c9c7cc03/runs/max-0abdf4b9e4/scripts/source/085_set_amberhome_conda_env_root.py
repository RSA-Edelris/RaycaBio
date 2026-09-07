
import subprocess, os

# Set AMBERHOME to the conda env root
env = os.environ.copy()
env['AMBERHOME'] = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

r = subprocess.run([
    'ante-MMPBSA.py',
    '-p', f'{MD_DIR}/complex.prmtop',
    '-c', f'{MD_DIR}/complex_nowater.prmtop',
    '-r', f'{MD_DIR}/receptor.prmtop',
    '-l', f'{MD_DIR}/ligand.prmtop',
    '-s', ':WAT,Cl-',
    '-n', ':LIG',
    '--radii', 'mbondi2',
], capture_output=True, text=True, cwd=MD_DIR, env=env)

print("rc:", r.returncode)
print(r.stdout[-400:] if r.stdout else "")
if r.returncode != 0:
    print("STDERR:", r.stderr[-600:])

for fname in ['complex_nowater.prmtop', 'receptor.prmtop', 'ligand.prmtop']:
    path = f'{MD_DIR}/{fname}'
    sz = os.path.getsize(path) if os.path.exists(path) else None
    print(f"  {fname}: {'OK  ' + str(sz) + ' bytes' if sz else 'MISSING'}")
