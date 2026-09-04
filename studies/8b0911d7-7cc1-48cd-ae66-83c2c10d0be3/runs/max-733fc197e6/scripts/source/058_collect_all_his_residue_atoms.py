
# Collect all HIS residue atoms
his_atoms = {}
with open(RECEPTOR_PDB) as f:
    for line in f:
        if (line.startswith('ATOM') or line.startswith('HETATM')):
            resname = line[17:20].strip()
            resnum  = int(line[22:26])
            aname   = line[12:16].strip()
            if resname == 'HIS':
                his_atoms.setdefault(resnum, []).append(aname)

for rn, atoms in sorted(his_atoms.items()):
    has_hd1 = 'HD1' in atoms
    has_he2 = 'HE2' in atoms
    correct = 'HIP' if (has_hd1 and has_he2) else ('HID' if has_hd1 else 'HIE')
    print(f"  HIS {rn:4d}: HD1={has_hd1}, HE2={has_he2} → rename to {correct}")
