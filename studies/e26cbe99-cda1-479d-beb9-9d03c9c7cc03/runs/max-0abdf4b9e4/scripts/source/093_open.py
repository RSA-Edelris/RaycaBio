
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

for cid in compounds:
    d = f'{WD}/mmgbsa_{cid}'

    # Single-frame netcdf trajectory from inpcrd
    cpptraj_in = f"""\
parm {d}/cpx.prmtop
trajin {d}/complex.inpcrd
trajout {d}/single.nc netcdf
run
quit
"""
    with open(f'{d}/cpptraj_single.in', 'w') as fh:
        fh.write(cpptraj_in)
    r = subprocess.run(['cpptraj', '-i', f'{d}/cpptraj_single.in'],
                       capture_output=True, text=True, env=env)
    nc_ok = os.path.exists(f'{d}/single.nc')
    if not nc_ok:
        print(f"{cid}: cpptraj FAIL"); print(r.stderr[-300:]); continue

    # Write MMPBSA.in
    with open(f'{d}/mmpbsa_single.in', 'w') as fh:
        fh.write(mmpbsa_in)

    print(f"{cid}: cpptraj OK → queuing MMPBSA.py")

print("All trajectories ready.")
