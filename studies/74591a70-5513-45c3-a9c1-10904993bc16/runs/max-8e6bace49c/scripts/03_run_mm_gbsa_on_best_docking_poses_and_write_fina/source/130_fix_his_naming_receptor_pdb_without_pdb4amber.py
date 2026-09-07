
# Fix HIS naming in receptor PDB without pdb4amber
# Strategy: for each HIS residue, check if HD1 present → HID, HE2 present → HIE, both → HIP

from pathlib import Path
from collections import defaultdict

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
rec_in  = Path(f"{BASE}/mmgbsa2/receptor_protein.pdb")
rec_out = Path(f"{BASE}/mmgbsa2/receptor_amber.pdb")

lines = rec_in.read_text().splitlines()

# First pass: collect atoms per HIS residue
# Parse ATOM lines: cols 12-15=atom_name, 17-19=res_name, 21=chain, 22-25=res_seq
his_protons = defaultdict(set)  # key: (chain, resseq) → set of atom names

for line in lines:
    if not line.startswith(('ATOM', 'HETATM')):
        continue
    res_name = line[17:20].strip()
    if res_name != 'HIS':
        continue
    atom_name = line[12:16].strip()
    chain = line[21]
    resseq = line[22:26].strip()
    his_protons[(chain, resseq)].add(atom_name)

# Determine new name for each HIS residue
his_rename = {}
for key, atoms in his_protons.items():
    has_hd1 = 'HD1' in atoms
    has_he2 = 'HE2' in atoms
    if has_hd1 and has_he2:
        his_rename[key] = 'HIP'
    elif has_hd1:
        his_rename[key] = 'HID'
    else:
        his_rename[key] = 'HIE'

print(f"HIS residues found: {len(his_rename)}")
for (chain, resseq), name in sorted(his_rename.items(), key=lambda x: int(x[0][1])):
    atoms = his_protons[(chain, resseq)]
    hd1 = 'HD1' in atoms
    he2 = 'HE2' in atoms
    print(f"  Chain {chain} Res {resseq}: {'HD1' if hd1 else '   '} {'HE2' if he2 else '   '} → {name}")
