
# Short energy minimization: 500 SD + 1000 CG, no periodic boundary, implicit GB
min_in = """Minimization of docked complex
 &cntrl
  imin=1, maxcyc=1500, ncyc=500,
  ntb=0,               ! no periodic box (gas phase / implicit solvent)
  igb=5, saltcon=0.15,
  cut=999.0,           ! no cutoff for implicit solvent
  ntr=1, restraintmask=':1-566', restraint_wt=5.0,  ! restrain receptor
  ntpr=100,
 /
"""
with open('min.in','w') as f:
    f.write(min_in)

# Check if sander is available
import subprocess
r_s = subprocess.run(['which','sander'], capture_output=True, text=True)
print("sander:", r_s.stdout.strip() or 'not found')

r_sander = subprocess.run([
    'sander',
    '-O',
    '-i', 'min.in',
    '-o', 'min.out',
    '-p', 'complex.prmtop',
    '-c', 'complex.inpcrd',
    '-r', 'complex_min.rst7',
    '-ref', 'complex.inpcrd'
], capture_output=True, text=True, cwd=WS,
   env={**os.environ, 'AMBERHOME': amber_home})

print("sander rc:", r_sander.returncode)
if r_sander.returncode != 0:
    print("STDERR:", r_sander.stderr[-500:])
    # Show last lines of min.out
    try:
        with open('min.out') as f:
            print(f.read()[-1000:])
    except: pass
else:
    print("Minimization complete")
    # Show final energy
    import os
    with open('min.out') as f:
        lines = f.readlines()
    for l in lines[-30:]:
        if 'NSTEP' in l or 'ENERGY' in l or 'BOND' in l or 'VDWAALS' in l:
            print(l, end='')
