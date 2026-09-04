
import os, subprocess, tempfile

RECEPTOR_PDB = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/9C56_receptor.pdb'
AMBER_HOME   = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
FIXED_PDB    = '/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc/9C56_receptor_amber.pdb'

# Build residue → correct name mapping
rename_map = {}  # resnum → new_resname
for rn, atoms in his_atoms.items():
    has_hd1 = 'HD1' in atoms
    has_he2 = 'HE2' in atoms
    rename_map[rn] = 'HIP' if (has_hd1 and has_he2) else ('HID' if has_hd1 else 'HIE')

# Rewrite PDB with corrected residue names
lines_out = []
with open(RECEPTOR_PDB) as f:
    for line in f:
        if (line.startswith('ATOM') or line.startswith('HETATM')):
            resname = line[17:20].strip()
            resnum  = int(line[22:26])
            if resname == 'HIS' and resnum in rename_map:
                new_name = rename_map[resnum]
                line = line[:17] + f"{new_name:<3s}" + line[20:]
        lines_out.append(line)

with open(FIXED_PDB, 'w') as f:
    f.writelines(lines_out)

print(f"Written: {FIXED_PDB}")

# Verify
r = subprocess.run(['grep', 'HIS', FIXED_PDB], capture_output=True, text=True)
his_remaining = r.stdout.count('\n')
print(f"HIS lines remaining: {his_remaining}")
r2 = subprocess.run(['grep', '-c', 'HID\|HIE\|HIP', FIXED_PDB], capture_output=True, text=True)
print(f"HID/HIE/HIP lines: {r2.stdout.strip()}")
