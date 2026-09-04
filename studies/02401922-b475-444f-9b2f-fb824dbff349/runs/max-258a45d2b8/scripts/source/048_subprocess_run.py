
import subprocess, os

amber_home = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

r_mmgb2 = subprocess.run([
    'MMPBSA.py', '-O',
    '-i', 'mmpbsa.in',
    '-o', 'FINAL_RESULTS_MMGBSA.dat',
    '-cp', 'complex.prmtop',
    '-rp', 'receptor.prmtop',
    '-lp', 'ligand_amber.prmtop',
    '-y',  'complex.inpcrd'
], capture_output=True, text=True, cwd=WS,
   env={**os.environ, 'AMBERHOME': amber_home})

print("MMPBSA.py rc:", r_mmgb2.returncode)
if r_mmgb2.returncode != 0:
    print("STDERR:", r_mmgb2.stderr[-500:])
else:
    # Parse key results
    with open('FINAL_RESULTS_MMGBSA.dat') as f:
        content = f.read()
    # Extract delta section
    idx = content.find('Differences')
    if idx >= 0:
        print(content[idx:idx+600])
    # Also show ligand VDWAALS to verify fix
    idx2 = content.find('Ligand:')
    if idx2 >= 0:
        print(content[idx2:idx2+300])
