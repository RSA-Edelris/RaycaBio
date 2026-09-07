
import os, subprocess

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
REC_PDB = f'{WD}/md_EDS01806218_ent2/receptor_tleap.pdb'
compounds = ['EDS01357518_ent1','EDS01357518_ent2',
             'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']
env = {**os.environ, 'AMBERHOME': AMBERHOME}

for cid in compounds:
    d = f'{WD}/mmgbsa_{cid}'
    # Rebuild complex.prmtop with mbondi2 radii set
    tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
LIG = loadmol2 {d}/lig.mol2
loadamberparams {d}/lig.frcmod
REC = loadpdb {REC_PDB}
complex = combine {{ REC LIG }}
set default PBRadii mbondi2
saveamberparm complex {d}/complex.prmtop {d}/complex.inpcrd
quit
"""
    with open(f'{d}/tleap_mbondi2.in', 'w') as fh:
        fh.write(tleap_in)
    r = subprocess.run(['tleap', '-f', f'{d}/tleap_mbondi2.in'],
                       capture_output=True, text=True, cwd=d)
    ok = os.path.exists(f'{d}/complex.prmtop')

    # Re-run ante-MMPBSA.py with new complex.prmtop
    r2 = subprocess.run([
        'ante-MMPBSA.py',
        '-p', f'{d}/complex.prmtop',
        '-c', f'{d}/cpx.prmtop',
        '-r', f'{d}/rec.prmtop',
        '-l', f'{d}/lig.prmtop',
        '-n', ':LIG',
        '--radii', 'mbondi2'],
        capture_output=True, text=True, cwd=d, env=env)
    all_ok = all(os.path.exists(f'{d}/{f}') for f in ['cpx.prmtop','rec.prmtop','lig.prmtop'])
    print(f"{cid}: tleap={'OK' if ok else 'FAIL'}  ante-MMPBSA={'OK' if all_ok else 'FAIL'}")
    if not all_ok:
        print("  STDERR:", r2.stderr[-200:])
