
# Strip ALL H from receptor_amber.pdb (including polar H PDBFixer added with wrong names)
# tleap will re-add H with correct ff14SB names
stripped = []
with open('receptor_amber.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            elem = line[76:78].strip() if len(line) >= 78 else ''
            aname = line[12:16].strip()
            # Skip if element is H or atom name starts with H
            if elem == 'H' or (not elem and aname.startswith('H')):
                continue
        stripped.append(line)

with open('receptor_noh.pdb','w') as f:
    f.writelines(stripped)
print(f"receptor_noh.pdb: {len(stripped)} lines (H stripped)")

# Final tleap with H-stripped receptor + addHydrogens
tleap5 = """
source leaprc.protein.ff14SB
source leaprc.gaff2

loadamberparams ligand_docked.frcmod
LIG = loadmol2 ligand_docked.mol2

REC = loadpdb receptor_noh.pdb
addHydrogens REC

COM = combine {REC LIG}

saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG  ligand_amber.prmtop ligand_amber.inpcrd

quit
"""
with open('tleap5.in','w') as f:
    f.write(tleap5)

r_tl5 = subprocess.run(['tleap','-f','tleap5.in'], capture_output=True, text=True, cwd=WS)
print("tleap5 rc:", r_tl5.returncode)
for l in r_tl5.stdout.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','Fatal','error','Warning','saved','Saved','Exiting','Total charge']):
        print(l)
