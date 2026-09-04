
import os, subprocess

# Find AMBERHOME from tleap location
r = subprocess.run(['which','tleap'], capture_output=True, text=True)
tleap_path = r.stdout.strip()  # /home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/tleap
amber_home = os.path.dirname(os.path.dirname(tleap_path))
print("AMBERHOME:", amber_home)
os.environ['AMBERHOME'] = amber_home

# Retry MMPBSA.py
r_mmgb = subprocess.run([
    'MMPBSA.py', '-O',
    '-i', 'mmpbsa.in',
    '-o', 'FINAL_RESULTS_MMGBSA.dat',
    '-cp', 'complex.prmtop',
    '-rp', 'receptor.prmtop',
    '-lp', 'ligand_amber.prmtop',
    '-y',  'complex.inpcrd'
], capture_output=True, text=True, cwd=WS,
   env={**os.environ, 'AMBERHOME': amber_home})

print("MMPBSA.py rc:", r_mmgb.returncode)
print(r_mmgb.stdout[-2000:])
if r_mmgb.returncode != 0:
    print("STDERR:", r_mmgb.stderr[-1000:])
