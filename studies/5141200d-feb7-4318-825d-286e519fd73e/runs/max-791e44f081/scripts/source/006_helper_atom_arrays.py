
import numpy as np

# ── Helper: atom arrays ───────────────────────────────────────────────────────
lig_xyz  = np.array([[a["x"], a["y"], a["z"]] for a in lig_atoms])
prot_xyz = np.array([[a["x"], a["y"], a["z"]] for a in brd9_atoms])

lig_com  = lig_xyz.mean(axis=0)
prot_com = prot_xyz.mean(axis=0)

# ── 2. For each ligand atom: find nearest protein atom & count contacts <4 Å ─
print("BI-7273 atom burial analysis (contacts to BRD9 within 4 Å):")
print(f"{'Atom':<6} {'Contacts<4Å':>12} {'MinDist':>9}  Exposure")
buried_threshold = 3   # ≥3 protein contacts → buried
exposed_atoms = []
for a, xyz in zip(lig_atoms, lig_xyz):
    dists = np.linalg.norm(prot_xyz - xyz, axis=1)
    n_contacts = int((dists < 4.0).sum())
    min_d = float(dists.min())
    exposure = "EXPOSED" if n_contacts < buried_threshold else "buried"
    if n_contacts < buried_threshold:
        exposed_atoms.append(a["name"])
    print(f"{a['name']:<6} {n_contacts:>12d} {min_d:>9.2f} Å  {exposure}")

print(f"\nExposed atoms (< {buried_threshold} protein contacts within 4 Å):")
print(" ", ", ".join(exposed_atoms))

# ── 3. Solvent-exposure direction per exposed atom (vector away from prot CoM) ─
print("\nOutward vectors for exposed ligand atoms:")
for a in lig_atoms:
    if a["name"] not in exposed_atoms:
        continue
    xyz = np.array([a["x"], a["y"], a["z"]])
    vec = xyz - prot_com
    vec_n = vec / np.linalg.norm(vec)
    print(f"  {a['name']:<5}  pos=({xyz[0]:6.2f},{xyz[1]:6.2f},{xyz[2]:6.2f})  "
          f"outward=({vec_n[0]:+.3f},{vec_n[1]:+.3f},{vec_n[2]:+.3f})")
