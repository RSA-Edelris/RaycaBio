
# Fix: 1) drop addHydrogens (not a valid cmd; tleap adds H automatically)
#       2) ensure TER between chains in receptor_noh.pdb

# Check chain break issue in receptor_noh.pdb
chains_seen = []
with open('receptor_noh.pdb') as f:
    for line in f:
        if line.startswith('ATOM'):
            chain = line[21]
            if not chains_seen or chains_seen[-1] != chain:
                chains_seen.append(chain)
print("Chains in receptor_noh.pdb:", chains_seen)

# Add TER between chains and at end
lines_out = []
prev_chain = None
with open('receptor_noh.pdb') as f:
    for line in f:
        if line.startswith('ATOM'):
            chain = line[21]
            if prev_chain and chain != prev_chain:
                lines_out.append('TER\n')
            prev_chain = chain
            lines_out.append(line)
        elif line.startswith('TER') or line.startswith('END'):
            if lines_out and not lines_out[-1].startswith('TER'):
                lines_out.append('TER\n')
        else:
            lines_out.append(line)
lines_out.append('END\n')

with open('receptor_noh2.pdb','w') as f:
    f.writelines(lines_out)
print(f"receptor_noh2.pdb: {len(lines_out)} lines")

# tleap without addHydrogens (tleap adds H implicitly)
tleap6 = """source leaprc.protein.ff14SB
source leaprc.gaff2
loadamberparams ligand_docked.frcmod
LIG = loadmol2 ligand_docked.mol2
REC = loadpdb receptor_noh2.pdb
COM = combine {REC LIG}
saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG  ligand_amber.prmtop ligand_amber.inpcrd
quit
"""
with open('tleap6.in','w') as f:
    f.write(tleap6)

r_tl6 = subprocess.run(['tleap','-f','tleap6.in'], capture_output=True, text=True, cwd=WS)
print("tleap6 rc:", r_tl6.returncode)
for l in r_tl6.stdout.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','Fatal','Warning','saved','Saved','Exiting','Total','prmtop']):
        print(l)
