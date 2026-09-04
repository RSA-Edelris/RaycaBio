
# Write correctly mapped mol2: template topology + correctly ordered docked coords
with open('ligand.mol2') as f:
    mol2_lines = f.readlines()

out_lines = []
in_atoms = False
atom_idx = 0   # 0-based index into template atoms

for line in mol2_lines:
    if '@<TRIPOS>ATOM' in line:
        in_atoms = True
        out_lines.append(line)
        continue
    if '@<TRIPOS>' in line and in_atoms:
        in_atoms = False

    if in_atoms and line.strip():
        parts = line.split()
        if len(parts) >= 6:
            x, y, z = new_coords[atom_idx]
            # Rebuild line preserving original atom type/charge fields
            rest = parts[5:]  # type, subst_id, subst_name, charge
            new_line = f"{parts[0]:>7s} {parts[1]:<8s} {x:>10.4f} {y:>10.4f} {z:>10.4f}  {'  '.join(rest)}\n"
            out_lines.append(new_line)
            atom_idx += 1
            continue

    out_lines.append(line)

with open('ligand_mapped.mol2','w') as f:
    f.writelines(out_lines)
print(f"ligand_mapped.mol2 written, {atom_idx} atoms updated")

# Rebuild frcmod and topology
r_pk4 = subprocess.run(['parmchk2','-i','ligand_mapped.mol2','-f','mol2',
                        '-o','ligand_mapped.frcmod','-s','gaff2'],
                       capture_output=True, text=True, cwd=WS)
print("parmchk2 rc:", r_pk4.returncode)

tleap8 = """source leaprc.protein.ff14SB
source leaprc.gaff2
loadamberparams ligand_mapped.frcmod
LIG = loadmol2 ligand_mapped.mol2
REC = loadpdb receptor_noh2.pdb
COM = combine {REC LIG}
saveamberparm COM  complex.prmtop  complex.inpcrd
saveamberparm REC  receptor.prmtop receptor.inpcrd
saveamberparm LIG  ligand_amber.prmtop ligand_amber.inpcrd
quit
"""
with open('tleap8.in','w') as f:
    f.write(tleap8)

r_tl8 = subprocess.run(['tleap','-f','tleap8.in'], capture_output=True, text=True, cwd=WS)
print("tleap8 rc:", r_tl8.returncode)
for l in r_tl8.stdout.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','Fatal','Exiting']):
        print(l)
