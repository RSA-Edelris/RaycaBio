
import os, subprocess, json

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
compounds = ['EDS01357518_ent1','EDS01357518_ent2',
             'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']
env = {**os.environ, 'AMBERHOME': AMBERHOME}

# Gas-phase complex: no solvent to strip. Use -n :LIG to define ligand mask.
for cid in compounds:
    d = f'{WD}/mmgbsa_{cid}'
    r = subprocess.run([
        'ante-MMPBSA.py',
        '-p', f'{d}/complex.prmtop',
        '-c', f'{d}/cpx.prmtop',
        '-r', f'{d}/rec.prmtop',
        '-l', f'{d}/lig.prmtop',
        '-n', ':LIG',
        '--radii', 'mbondi2'],
        capture_output=True, text=True, cwd=d, env=env)
    ok = os.path.exists(f'{d}/lig.prmtop')
    print(f"{cid}: ante-MMPBSA={'OK' if ok else 'FAIL'}")
    if not ok:
        print("  STDERR:", r.stderr[-400:])
