
import numpy as np

# Re-extract LI8 centroid from original 1Z5M
pdb_path = os.path.join(ws, '1Z5M.pdb')
lines = open(pdb_path).readlines()

li8_coords = []
for l in lines:
    if l.startswith("HETATM") and l[17:20].strip() == "LI8":
        x, y, z = float(l[30:38]), float(l[38:46]), float(l[46:54])
        li8_coords.append([x, y, z])

li8_arr = np.array(li8_coords)
cx, cy, cz = li8_arr.mean(axis=0)
box_size = 22.0
print(f"LI8 atoms: {len(li8_coords)}")
print(f"Box center: ({cx:.3f}, {cy:.3f}, {cz:.3f})")
print(f"Box size:   {box_size} x {box_size} x {box_size} Å")
print(f"LI8 extent: X={li8_arr[:,0].min():.1f}–{li8_arr[:,0].max():.1f}  "
      f"Y={li8_arr[:,1].min():.1f}–{li8_arr[:,1].max():.1f}  "
      f"Z={li8_arr[:,2].min():.1f}–{li8_arr[:,2].max():.1f}")

# Waters within 5 Å of LI8 (kept in receptor)
near_w = []
for l in lines:
    if l.startswith("HETATM") and l[17:20].strip() in ("HOH","WAT"):
        x,y,z = float(l[30:38]),float(l[38:46]),float(l[46:54])
        d = np.linalg.norm([x-cx, y-cy, z-cz])
        if d <= 5.0:
            near_w.append((l[22:26].strip(), round(d,2)))
print(f"Active-site waters within 5 Å: {near_w}")
