
# parmchk2: missing GAFF2 parameters
r_pk = subprocess.run([
    'parmchk2', '-i', 'ligand.mol2', '-f', 'mol2',
    '-o', 'ligand.frcmod', '-s', 'gaff2'
], capture_output=True, text=True, cwd=WS)
print("parmchk2 rc:", r_pk.returncode)

# Write tleap input for complex (receptor ff14SB + ligand GAFF2)
tleap_input = """
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p

loadamberparams ligand.frcmod
LIG = loadmol2 ligand.mol2

# Load receptor (already has H from PDBFixer)
REC = loadpdb receptor_prepared.pdb

# Load best docked pose
DOCKED = loadpdb best_pose.pdb

# Build complex
COM = combine {REC DOCKED}

# Single-point — no solvent for gas-phase MM/GBSA
saveamberparm COM complex.prmtop complex.inpcrd
saveamberparm REC receptor.prmtop receptor.inpcrd
saveamberparm DOCKED ligand_amber.prmtop ligand_amber.inpcrd

quit
"""
with open('tleap.in','w') as f:
    f.write(tleap_input)

r_tl = subprocess.run(['tleap', '-f', 'tleap.in'],
                      capture_output=True, text=True, cwd=WS)
print("tleap rc:", r_tl.returncode)
# Show last 30 lines
for l in r_tl.stdout.split('\n')[-30:]:
    print(l)
if r_tl.returncode != 0:
    print("STDERR:", r_tl.stderr[-300:])
