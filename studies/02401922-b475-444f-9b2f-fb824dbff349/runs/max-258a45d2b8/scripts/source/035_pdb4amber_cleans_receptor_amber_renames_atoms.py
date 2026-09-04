
# pdb4amber cleans receptor for Amber — renames atoms, removes problem H
r_p4a = subprocess.run([
    'pdb4amber',
    '-i', 'receptor_nowater.pdb',
    '-o', 'receptor_amber.pdb',
    '--nohyd',          # strip all H (tleap will re-add with correct names)
    '--no-conect'
], capture_output=True, text=True, cwd=WS)
print("pdb4amber rc:", r_p4a.returncode)
print(r_p4a.stdout[:500])
if r_p4a.returncode != 0:
    print("STDERR:", r_p4a.stderr[:500])

# Now re-run tleap with cleaned receptor
tleap4 = """
source leaprc.protein.ff14SB
source leaprc.gaff2

loadamberparams ligand_docked.frcmod
LIG = loadmol2 ligand_docked.mol2

REC = loadpdb receptor_amber.pdb

COM = combine {REC LIG}

saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG  ligand_amber.prmtop ligand_amber.inpcrd

quit
"""
with open('tleap4.in','w') as f:
    f.write(tleap4)

r_tl4 = subprocess.run(['tleap','-f','tleap4.in'], capture_output=True, text=True, cwd=WS)
print("\ntleap4 rc:", r_tl4.returncode)
for l in r_tl4.stdout.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','Fatal','error','Warning','saved','Saved','Exiting','Total']):
        print(l)
