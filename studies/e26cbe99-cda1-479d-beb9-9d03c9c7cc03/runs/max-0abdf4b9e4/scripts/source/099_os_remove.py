
import os, subprocess

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
env = {**os.environ, 'AMBERHOME': AMBERHOME}
d = f'{WD}/mmgbsa_EDS01357518_ent1'

for f in ['cpx.prmtop', 'rec.prmtop', 'lig.prmtop']:
    try: os.remove(f'{d}/{f}')
    except: pass

r = subprocess.run([
    'ante-MMPBSA.py',
    '-p', f'{d}/complex.prmtop',
    '-c', f'{d}/cpx.prmtop',
    '-r', f'{d}/rec.prmtop',
    '-l', f'{d}/lig.prmtop',
    '-n', ':LIG',
    '--radii', 'mbondi2'],
    capture_output=True, text=True, cwd=d, env=env)

print("RETURNCODE:", r.returncode)
print("STDOUT:", r.stdout[:1000])
print("STDERR:", r.stderr[:1000])
print("Files:", sorted(os.listdir(d)))
