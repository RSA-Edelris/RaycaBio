
# Strategy: read ligand.mol2 (correct GAFF2 from SDF) as template
# Read ligand_docked.mol2 (correct coords from docked PDB) 
# Map atom positions from docked mol2 → template mol2 by element+index order

# First, read both mol2 atom sections
def parse_mol2_atoms(path):
    atoms = []
    in_atoms = False
    with open(path) as f:
        for line in f:
            if '@<TRIPOS>ATOM' in line:
                in_atoms = True
                continue
            if '@<TRIPOS>' in line and in_atoms:
                break
            if in_atoms:
                parts = line.split()
                if len(parts) >= 6:
                    atoms.append({
                        'idx': parts[0], 'name': parts[1],
                        'x': float(parts[2]), 'y': float(parts[3]), 'z': float(parts[4]),
                        'type': parts[5], 'rest': parts
                    })
    return atoms

template_atoms = parse_mol2_atoms('ligand.mol2')
docked_atoms   = parse_mol2_atoms('ligand_docked.mol2')

print(f"Template atoms: {len(template_atoms)}, Docked atoms: {len(docked_atoms)}")

# Both should have 73 atoms (same molecule)
# Match by position index (same atom ordering if both from same SMILES)
if len(template_atoms) == len(docked_atoms):
    # Write updated mol2: template topology + docked coordinates
    with open('ligand.mol2') as f:
        mol2_content = f.read()
    
    # Replace atom block
    lines = mol2_content.split('\n')
    out_lines = []
    in_atoms = False
    atom_idx = 0
    for line in lines:
        if '@<TRIPOS>ATOM' in line:
            in_atoms = True
            out_lines.append(line)
            continue
        if '@<TRIPOS>' in line and in_atoms:
            in_atoms = False
        if in_atoms and line.strip():
            # Replace x,y,z with docked coordinates
            parts = line.split()
            if len(parts) >= 6 and atom_idx < len(docked_atoms):
                da = docked_atoms[atom_idx]
                # Keep template types/charges, use docked coords
                new_line = f"{parts[0]:>7s} {parts[1]:<8s} {da['x']:>10.4f} {da['y']:>10.4f} {da['z']:>10.4f} {'  '.join(parts[5:])}"
                out_lines.append(new_line)
                atom_idx += 1
                continue
        out_lines.append(line)
    
    with open('ligand_corrected.mol2','w') as f:
        f.write('\n'.join(out_lines))
    print(f"Written ligand_corrected.mol2 with docked coords + template topology, {atom_idx} atoms updated")
else:
    print("Atom count mismatch! Cannot directly map")
    print("Template elements:", [a['type'].split('.')[0] for a in template_atoms[:10]])
    print("Docked elements:", [a['type'].split('.')[0] for a in docked_atoms[:10]])
