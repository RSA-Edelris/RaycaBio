
import os, subprocess

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
compounds = ['EDS01357518_ent1','EDS01357518_ent2',
             'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']
env = {**os.environ, 'AMBERHOME': AMBERHOME}

mmgbsa_results = {}

for cid in compounds:
    d = f'{WD}/mmgbsa_{cid}'

    # Remove stale prmtops so ante-MMPBSA.py will write fresh ones
    for f in ['cpx.prmtop', 'rec.prmtop', 'lig.prmtop']:
        try:
            os.remove(f'{d}/{f}')
        except FileNotFoundError:
            pass

    r = subprocess.run([
        'ante-MMPBSA.py',
        '-p', f'{d}/complex.prmtop',
        '-c', f'{d}/cpx.prmtop',
        '-r', f'{d}/rec.prmtop',
        '-l', f'{d}/lig.prmtop',
        '-n', ':LIG',
        '--radii', 'mbondi2'],
        capture_output=True, text=True, cwd=d, env=env)

    all_ok = all(os.path.exists(f'{d}/{f}') for f in ['cpx.prmtop','rec.prmtop','lig.prmtop'])
    if not all_ok:
        print(f"{cid}: ante-MMPBSA FAIL\n  {r.stderr[-200:]}"); continue

    # Rebuild single-frame trajectory from new complex.inpcrd
    cpptraj_in = f"parm {d}/cpx.prmtop\ntrajin {d}/complex.inpcrd\ntrajout {d}/single.nc netcdf\nrun\nquit\n"
    with open(f'{d}/cpptraj_single.in', 'w') as fh:
        fh.write(cpptraj_in)
    subprocess.run(['cpptraj', '-i', f'{d}/cpptraj_single.in'],
                   capture_output=True, text=True, env=env)

    # MMPBSA.py single-point
    mmpbsa_in = "&general\n  startframe=1, endframe=1, interval=1, verbose=2,\n/\n&gb\n  igb=5, saltcon=0.15,\n/\n"
    with open(f'{d}/mmpbsa_single.in', 'w') as fh:
        fh.write(mmpbsa_in)

    r2 = subprocess.run([
        'MMPBSA.py', '-O',
        '-i', f'{d}/mmpbsa_single.in',
        '-cp', f'{d}/cpx.prmtop',
        '-rp', f'{d}/rec.prmtop',
        '-lp', f'{d}/lig.prmtop',
        '-y',  f'{d}/single.nc',
        '-o',  f'{d}/mmgbsa_result.dat',
        '-prefix', f'{d}/tmp_'],
        capture_output=True, text=True, cwd=d, env=env)

    if os.path.exists(f'{d}/mmgbsa_result.dat'):
        content = open(f'{d}/mmgbsa_result.dat').read()
        dg = None
        for line in content.splitlines():
            if 'DELTA TOTAL' in line:
                try: dg = float(line.split()[2])
                except: pass
        mmgbsa_results[cid] = dg
        print(f"{cid}: ΔG = {dg} kcal/mol")
    else:
        print(f"{cid}: MMPBSA FAIL\n  {r2.stderr[-300:]}")

print("\nFinal:", mmgbsa_results)
