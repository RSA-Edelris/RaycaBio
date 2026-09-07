
import os, subprocess

WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
compounds = ['EDS01357518_ent1','EDS01357518_ent2',
             'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']
env = {**os.environ, 'AMBERHOME': AMBERHOME}

mmpbsa_in = """\
&general
  startframe = 1,
  endframe   = 1,
  interval   = 1,
  verbose    = 2,
/
&gb
  igb     = 5,
  saltcon = 0.15,
/
"""

mmgbsa_results = {}

for cid in compounds:
    d = f'{WD}/mmgbsa_{cid}'

    # Single-frame netcdf from inpcrd using complex.prmtop
    cpptraj_in = f"parm {d}/complex.prmtop\ntrajin {d}/complex.inpcrd\ntrajout {d}/single.nc netcdf\nrun\nquit\n"
    with open(f'{d}/cpptraj_single.in', 'w') as fh:
        fh.write(cpptraj_in)
    r = subprocess.run(['cpptraj', '-i', f'{d}/cpptraj_single.in'],
                       capture_output=True, text=True, env=env)
    if not os.path.exists(f'{d}/single.nc'):
        print(f"{cid}: cpptraj FAIL\n{r.stderr[-200:]}"); continue

    with open(f'{d}/mmpbsa_single.in', 'w') as fh:
        fh.write(mmpbsa_in)

    # Run MMPBSA.py
    r2 = subprocess.run([
        'MMPBSA.py',
        '-O',
        '-i', f'{d}/mmpbsa_single.in',
        '-cp', f'{d}/complex.prmtop',
        '-rp', f'{d}/rec.prmtop',
        '-lp', f'{d}/lig.prmtop',
        '-y', f'{d}/single.nc',
        '-o', f'{d}/mmgbsa_result.dat',
        '-prefix', f'{d}/mmgbsa_tmp'],
        capture_output=True, text=True, cwd=d, env=env)

    if os.path.exists(f'{d}/mmgbsa_result.dat'):
        with open(f'{d}/mmgbsa_result.dat') as fh:
            content = fh.read()
        # Parse DELTA TOTAL
        dg = None
        for line in content.splitlines():
            if 'DELTA TOTAL' in line:
                parts = line.split()
                try:
                    dg = float(parts[2])
                except:
                    pass
        mmgbsa_results[cid] = dg
        print(f"{cid}: ΔG_MM-GBSA = {dg} kcal/mol")
    else:
        print(f"{cid}: MMPBSA FAIL\n{r2.stderr[-300:]}")

print("\nDone:", mmgbsa_results)
