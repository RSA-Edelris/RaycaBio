
pdb_path = "/home/ubuntu/rayca-artifacts/11507a0e2f5e69d5dfa40a62/files/Target.pdb"

hetatm = []
atom_coords = []
with open(pdb_path) as f:
    for line in f:
        if line.startswith("HETATM"):
            hetatm.append(line.strip())
        if line.startswith("ATOM") or line.startswith("HETATM"):
            try:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                atom_coords.append((x, y, z))
            except:
                pass

print(f"HETATM: {len(hetatm)}, total coords: {len(atom_coords)}")
for l in hetatm[:20]:
    print(l)
