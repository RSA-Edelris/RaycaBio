
import subprocess, os

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Write tleap script for explicit-solvent solvation
tleap_solv = """\
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p
loadamberparams ligand_mapped.frcmod
LIG = loadmol2 ligand_mapped.mol2
REC = loadpdb receptor_noh2.pdb
COM = combine {REC LIG}
solvateOct COM TIP3PBOX 10.0
addIons COM Na+ 0
addIonsRand COM Na+ 27 Cl- 27
saveamberparm COM  complex_solv.prmtop  complex_solv.inpcrd
savepdb COM complex_solv.pdb
quit
"""
with open(f'{wd}/tleap_solv.in', 'w') as f:
    f.write(tleap_solv)

# Run tleap
env = os.environ.copy()
env['AMBERHOME'] = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
tleap = f"{env['AMBERHOME']}/bin/tleap"
r = subprocess.run([tleap, '-f', f'{wd}/tleap_solv.in'], capture_output=True, text=True,
                   cwd=wd, env=env, timeout=300)
print("RC:", r.returncode)
# Show last 50 lines of output
lines = (r.stdout + r.stderr).splitlines()
for l in lines[-50:]:
    print(l)
