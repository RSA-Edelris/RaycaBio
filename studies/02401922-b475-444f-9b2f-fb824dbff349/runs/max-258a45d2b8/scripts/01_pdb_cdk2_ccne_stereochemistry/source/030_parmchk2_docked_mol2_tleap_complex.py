
# parmchk2 for docked mol2, then tleap for complex
r_pk2 = subprocess.run([
    'parmchk2', '-i', 'ligand_docked.mol2', '-f', 'mol2',
    '-o', 'ligand_docked.frcmod', '-s', 'gaff2'
], capture_output=True, text=True, cwd=WS)
print("parmchk2 rc:", r_pk2.returncode)

# Build complex PDB: receptor_prepared.pdb + best_pose_lig.pdb
with open('receptor_prepared.pdb') as f:
    rec_lines = [l for l in f if l.startswith(('ATOM','HETATM'))]
with open('best_pose_lig.pdb') as f:
    lig_lines = [l for l in f if l.startswith(('ATOM','HETATM'))]

with open('complex.pdb','w') as f:
    f.writelines(rec_lines)
    f.write('TER\n')
    f.writelines(lig_lines)
    f.write('END\n')
print(f"complex.pdb: {len(rec_lines)} rec + {len(lig_lines)} lig atoms")

# tleap input — load mol2 to define LIG, then loadpdb for coordinates
tleap2 = f"""
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p

loadamberparams ligand_docked.frcmod
LIG = loadmol2 ligand_docked.mol2

COM = loadpdb complex.pdb
REC = loadpdb receptor_prepared.pdb
LIG_UNIT = loadpdb best_pose_lig.pdb

saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG_UNIT ligand_amber.prmtop ligand_amber.inpcrd

quit
"""
with open('tleap2.in','w') as f:
    f.write(tleap2)

r_tl2 = subprocess.run(['tleap','-f','tleap2.in'], capture_output=True, text=True, cwd=WS)
print("tleap rc:", r_tl2.returncode)
# Show key lines
for l in r_tl2.stdout.split('\n'):
    if any(k in l for k in ['ERROR','Warning','FATAL','saved','Saved','wrote','Wrote','Total']):
        print(l)
