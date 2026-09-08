
import numpy as np

# Extract LI8 heavy atom coordinates → docking box center
li8_coords = []
missing_465 = []

for l in lines:
    if l.startswith("HETATM") and l[17:20].strip() == "LI8":
        x = float(l[30:38])
        y = float(l[38:46])
        z = float(l[46:54])
        aname = l[12:16].strip()
        li8_coords.append((aname, x, y, z))
    elif l.startswith("REMARK 465") and len(l) > 20:
        missing_465.append(l.strip())

li8_arr = np.array([[c[1], c[2], c[3]] for c in li8_coords])
cx, cy, cz = li8_arr.mean(axis=0)
print(f"LI8 atoms: {len(li8_coords)}")
print(f"LI8 heavy atom center: ({cx:.2f}, {cy:.2f}, {cz:.2f})")
print(f"LI8 extent: X={li8_arr[:,0].min():.1f}–{li8_arr[:,0].max():.1f}, "
      f"Y={li8_arr[:,1].min():.1f}–{li8_arr[:,1].max():.1f}, "
      f"Z={li8_arr[:,2].min():.1f}–{li8_arr[:,2].max():.1f}")

# Box size: 22 Å each side (generous for a drug-like molecule in a defined pocket)
box_size = 22.0

print(f"\nDocking box: center=({cx:.2f},{cy:.2f},{cz:.2f}), size={box_size}x{box_size}x{box_size} Å")
print(f"\nMissing residues (REMARK 465):")
for m in missing_465[:30]:
    print(" ", m)
if not missing_465:
    print("  None recorded")

# Also collect nearby waters (within 5 Å of LI8 center) → keep these
near_waters = []
for l in lines:
    if l.startswith("HETATM") and l[17:20].strip() in ("HOH","WAT"):
        x,y,z = float(l[30:38]), float(l[38:46]), float(l[46:54])
        d = np.sqrt((x-cx)**2+(y-cy)**2+(z-cz)**2)
        if d <= 5.0:
            near_waters.append((l[22:26].strip(), x, y, z, round(d,2)))

print(f"\nWaters within 5 Å of LI8 center: {len(near_waters)}")
for w in near_waters:
    print(f"  HOH {w[0]}: ({w[1]:.1f},{w[2]:.1f},{w[3]:.1f}) d={w[4]} Å")
