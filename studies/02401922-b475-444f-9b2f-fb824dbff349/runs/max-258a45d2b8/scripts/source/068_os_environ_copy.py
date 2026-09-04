
import subprocess, os

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
amber_home = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
env = os.environ.copy()
env['AMBERHOME'] = amber_home
python  = f"{amber_home}/bin/python"
mmpbsa  = f"{amber_home}/bin/MMPBSA.py"

# igb=8 (GB-Neck2)
with open(f'{wd}/mmpbsa_igb8.in', 'w') as f:
    f.write("&general\n  startframe=1, endframe=1, interval=1,\n  keep_files=0, verbose=1,\n/\n&gb\n  igb=8, saltcon=0.150,\n/\n")

r8 = subprocess.run(
    [python, mmpbsa, '-O',
     '-i', 'mmpbsa_igb8.in',
     '-o', 'RESULTS_IGB8.dat',
     '-cp', 'complex.prmtop',
     '-rp', 'receptor.prmtop',
     '-lp', 'ligand_amber.prmtop',
     '-y',  'complex.inpcrd'],
    capture_output=True, text=True, cwd=wd, env=env, timeout=600)

print("igb=8 RC:", r8.returncode)
for line in (r8.stdout + r8.stderr).splitlines():
    if any(k in line for k in ('DELTA TOTAL','DELTA G','EEL','EGB','VDWAALS','ESURF','error','Error','fatal','Fatal')):
        print(line)
