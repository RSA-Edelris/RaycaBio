
import subprocess, os

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
amber_home = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
env = os.environ.copy()
env['AMBERHOME'] = amber_home
mmpbsa = f"{amber_home}/bin/MMPBSA.py"
python  = f"{amber_home}/bin/python"

# igb=8 (GB-Neck2, 2014, better for charged molecules)
mmpbsa_igb8 = """\
&general
  startframe=1, endframe=1, interval=1,
  keep_files=0, verbose=1,
/
&gb
  igb=8, saltcon=0.150,
/
"""
with open(f'{wd}/mmpbsa_igb8.in', 'w') as f:
    f.write(mmpbsa_igb8)

r8 = subprocess.run(
    [python, mmpbsa,
     '-O', '-i', 'mmpbsa_igb8.in',
     '-o', 'RESULTS_IGB8.dat',
     '-sp', 'complex.prmtop',
     '-rp', 'receptor.prmtop',
     '-lp', 'ligand_amber.prmtop',
     '-y',  'complex.inpcrd'],
    capture_output=True, text=True, cwd=wd, env=env, timeout=600)

print("igb=8 RC:", r8.returncode)
# Parse result
for line in (r8.stdout + r8.stderr).splitlines():
    if 'DELTA TOTAL' in line or 'DELTA G' in line or 'EEL' in line or 'EGB' in line or 'VDWAALS' in line or 'ESURF' in line:
        print(line)
