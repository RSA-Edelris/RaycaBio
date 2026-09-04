
import subprocess, os

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
amber_home = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
env = os.environ.copy()
env['AMBERHOME'] = amber_home
python  = f"{amber_home}/bin/python"
mmpbsa  = f"{amber_home}/bin/MMPBSA.py"

r = subprocess.run(
    [python, mmpbsa, '-O',
     '-i', 'mmpbsa.in',               # igb=5, saltcon=0.15 (same as original)
     '-o', 'RESULTS_MINIMIZED.dat',
     '-cp', 'complex.prmtop',
     '-rp', 'receptor.prmtop',
     '-lp', 'ligand_amber.prmtop',
     '-y',  'complex_min.rst7'],       # minimized structure
    capture_output=True, text=True, cwd=wd, env=env, timeout=600)

print("RC:", r.returncode)
for line in (r.stdout + r.stderr).splitlines():
    if any(k in line for k in ('DELTA TOTAL','DELTA G sol','DELTA G gas','EEL','EGB','VDWAALS','ESURF')):
        print(line)

# Also check Isambard probe job status
