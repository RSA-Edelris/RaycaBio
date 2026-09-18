
import numpy as np, collections

# ---- Precise H-bond analysis: donor/acceptor pairs within 3.5 Å ----
# Identify polar atoms in CTX and protein pocket residues

HBOND_CUTOFF = 3.5
CLOSE_HYDROPHOBIC = 4.0

# CTX polar atoms (N and O)
ctx_polar = [(n, x, y, z) for (n, x, y, z) in ctx_atoms if n[0] in ('N','O')]
ctx_hydrophobic = [(n, x, y, z) for (n, x, y, z) in ctx_atoms if n[0] == 'C']

pocket_res = set(contacts.keys())

# Collect pocket atoms
pocket_residue_atoms = {}
for chain, resname, resnum, aname, x, y, z in protein_atoms:
    if (chain, resnum, resname) in pocket_res:
        pocket_residue_atoms.setdefault((chain, resnum, resname), []).append((aname, x, y, z))

print("=== Potential H-bond pairs (protein polar ↔ CTX polar, ≤3.5 Å) ===")
hbonds_found = []
for (chain, resnum, resname), atoms in sorted(pocket_residue_atoms.items()):
    for aname, ax, ay, az in atoms:
        if aname[0] not in ('N','O','S'):
            continue
        pa = np.array([ax, ay, az])
        for cn, cx, cy, cz in ctx_polar:
            dist = np.linalg.norm(pa - np.array([cx, cy, cz]))
            if dist <= HBOND_CUTOFF:
                hbonds_found.append((dist, chain, resnum, resname, aname, cn))
                print(f"  Chain {chain} {resname}{resnum} {aname:5s} ↔ CTX {cn:5s}  {dist:.2f} Å")

# ---- Closest hydrophobic contacts ----
print("\n=== Key hydrophobic contacts (protein C ↔ CTX C, ≤4.0 Å) ===")
hydro_contacts = []
for (chain, resnum, resname), atoms in sorted(pocket_residue_atoms.items()):
    for aname, ax, ay, az in atoms:
        if aname[0] != 'C':
            continue
        pa = np.array([ax, ay, az])
        min_dist = 999.
        min_ctx = ''
        for cn, cx, cy, cz in ctx_hydrophobic:
            dist = np.linalg.norm(pa - np.array([cx, cy, cz]))
            if dist < min_dist:
                min_dist = dist
                min_ctx = cn
        if min_dist <= CLOSE_HYDROPHOBIC:
            hydro_contacts.append((min_dist, chain, resnum, resname, aname, min_ctx))

# Deduplicate: one entry per residue (closest contact)
seen_res = {}
for dist, chain, resnum, resname, aname, cn in sorted(hydro_contacts):
    key = (chain, resnum)
    if key not in seen_res:
        seen_res[key] = (dist, resname, aname, cn)

for (chain, resnum), (dist, resname, aname, cn) in sorted(seen_res.items()):
    print(f"  Chain {chain} {resname}{resnum:4d} {aname:5s} ↔ CTX {cn:5s}  {dist:.2f} Å")
