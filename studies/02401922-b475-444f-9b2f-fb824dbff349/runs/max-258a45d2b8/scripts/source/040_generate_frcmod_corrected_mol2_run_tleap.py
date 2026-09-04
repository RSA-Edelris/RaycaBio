
# Generate frcmod from corrected mol2 and run tleap
r_pk3 = subprocess.run([
    'parmchk2', '-i', 'ligand_corrected.mol2', '-f', 'mol2',
    '-o', 'ligand_corrected.frcmod', '-s', 'gaff2'
], capture_output=True, text=True, cwd=WS)
print("parmchk2 rc:", r_pk3.returncode)

tleap7 = """source leaprc.protein.ff14SB
source leaprc.gaff2
loadamberparams ligand_corrected.frcmod
LIG = loadmol2 ligand_corrected.mol2
REC = loadpdb receptor_noh2.pdb
COM = combine {REC LIG}
saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG  ligand_amber.prmtop ligand_amber.inpcrd
quit
"""
with open('tleap7.in','w') as f:
    f.write(tleap7)

r_tl7 = subprocess.run(['tleap','-f','tleap7.in'], capture_output=True, text=True, cwd=WS)
print("tleap7 rc:", r_tl7.returncode)
for l in r_tl7.stdout.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','Fatal','Warning','saved','Saved','Exiting','prmtop']):
        print(l)

import os
for fn in ['complex.prmtop','complex.inpcrd','receptor.prmtop','receptor.inpcrd',
           'ligand_amber.prmtop','ligand_amber.inpcrd']:
    sz = os.path.getsize(f'{WS}/{fn}') if os.path.exists(f'{WS}/{fn}') else 0
    print(f"  {fn}: {sz:,} bytes")
