
# Load ligand mol2 directly — skip loadpdb for ligand, use combine
# Also strip water from receptor to reduce complexity

# Write clean receptor PDB (protein only, no HOH for gas-phase MMGBSA)
prot_only_lines = []
with open('receptor_prepared.pdb') as f:
    for line in f:
        if line.startswith('ATOM'):
            prot_only_lines.append(line)
        elif line.startswith('HETATM') and 'HOH' in line:
            pass  # skip waters for GB solvation model
        elif line.startswith('TER') or line.startswith('END'):
            prot_only_lines.append(line)

with open('receptor_nowater.pdb','w') as f:
    f.writelines(prot_only_lines)
print(f"receptor_nowater.pdb: {len(prot_only_lines)} lines")

# tleap: load receptor from PDB, ligand from mol2, combine
tleap3 = """
source leaprc.protein.ff14SB
source leaprc.gaff2

loadamberparams ligand_docked.frcmod
LIG = loadmol2 ligand_docked.mol2

REC = loadpdb receptor_nowater.pdb

COM = combine {REC LIG}

saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG  ligand_amber.prmtop ligand_amber.inpcrd

quit
"""
with open('tleap3.in','w') as f:
    f.write(tleap3)

r_tl3 = subprocess.run(['tleap','-f','tleap3.in'], capture_output=True, text=True, cwd=WS)
print("tleap rc:", r_tl3.returncode)
for l in r_tl3.stdout.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','Fatal','error','Warning','saved','Saved','Exiting']):
        print(l)
