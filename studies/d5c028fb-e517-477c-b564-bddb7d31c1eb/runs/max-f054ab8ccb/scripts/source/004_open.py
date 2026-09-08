
import numpy as np, re, collections

PDB_PATH = "/home/ubuntu/rayca-artifacts/396fce89620d1932c2d5eb11/files/CDK2-CCNE.pdb"

# ---- Parse all HETATM CTX atoms and all ATOM residues ----
ctx_atoms = []   # (name, x, y, z)
protein_atoms = []  # (chain, resname, resnum, atomname, x, y, z)

with open(PDB_PATH) as f:
    for line in f:
        rec = line[:6].strip()
        if rec == 'HETATM':
            resname = line[17:20].strip()
            if resname == 'CTX':
                aname = line[12:16].strip()
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                ctx_atoms.append((aname, x, y, z))
        elif rec == 'ATOM':
            chain  = line[21].strip()
            resname= line[17:20].strip()
            resnum = int(line[22:26].strip())
            aname  = line[12:16].strip()
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            protein_atoms.append((chain, resname, resnum, aname, x, y, z))

print(f"CTX atoms: {len(ctx_atoms)}")
print(f"Protein atoms: {len(protein_atoms)}")

# Centroid of CTX
ctx_xyz = np.array([[a[1], a[2], a[3]] for a in ctx_atoms])
ctx_centroid = ctx_xyz.mean(axis=0)
ctx_min = ctx_xyz.min(axis=0)
ctx_max = ctx_xyz.max(axis=0)
print(f"\nCTX centroid: {ctx_centroid.round(1)}")
print(f"CTX bbox: min={ctx_min.round(1)}  max={ctx_max.round(1)}")
print(f"CTX bbox size: {(ctx_max - ctx_min).round(1)}")

# Identify all protein residues within 4.5 Å of ANY CTX heavy atom (exclude H)
CUTOFF = 4.5
contacts = collections.defaultdict(set)  # (chain, resnum, resname) -> {atom_contacts}

for chain, resname, resnum, aname, x, y, z in protein_atoms:
    if aname.startswith('H'):
        continue
    pa = np.array([x, y, z])
    for ca_name, cx, cy, cz in ctx_atoms:
        if ca_name.startswith('H'):
            continue
        dist = np.linalg.norm(pa - np.array([cx, cy, cz]))
        if dist <= CUTOFF:
            contacts[(chain, resnum, resname)].add(aname)
            break

print(f"\n=== Binding-site residues within {CUTOFF} Å of CTX ({len(contacts)} residues) ===")
for (chain, resnum, resname), atoms in sorted(contacts.items()):
    atom_list = ', '.join(sorted(atoms))
    print(f"  Chain {chain}  {resname:3s} {resnum:4d}   contact atoms: {atom_list}")
