
import numpy as np

# Estimate receptor 3D extent to predict simulation box size
coords = []
with open("receptor_pH74_noH.pdb") as f:
    for line in f:
        if line.startswith("ATOM"):
            try:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                coords.append((x, y, z))
            except ValueError:
                pass

coords = np.array(coords)
mins = coords.min(axis=0)
maxs = coords.max(axis=0)
extents = maxs - mins
print(f"Receptor bounding box (Å):")
print(f"  X: {mins[0]:.1f} to {maxs[0]:.1f}  extent {extents[0]:.1f} Å")
print(f"  Y: {mins[1]:.1f} to {maxs[1]:.1f}  extent {extents[1]:.1f} Å")
print(f"  Z: {mins[2]:.1f} to {maxs[2]:.1f}  extent {extents[2]:.1f} Å")
print(f"  Max extent: {extents.max():.1f} Å")

# Estimate box with 12 Å padding (cubic, max extent governs)
pad = 12.0
box_side = extents.max() + 2 * pad
vol = box_side**3  # Å³
n_water = int(vol / 30.0)   # ~30 Å³/TIP3P
n_protein = len(coords)
n_total = n_water * 3 + n_protein  # approximate total atoms
print(f"\nWith 12 Å padding:")
print(f"  Box side: {box_side:.1f} Å = {box_side/10:.2f} nm")
print(f"  ~TIP3P waters: {n_water:,}")
print(f"  ~Total atoms:  {n_total:,}")
print(f"\nExpected throughput on A100 (PME, OpenMM):")
for ns_per_day in [100, 200]:
    for prod_ns in [0.5, 1.0]:
        equil_ns = 0.3
        total_ns = prod_ns + equil_ns
        mins_needed = total_ns / ns_per_day * 24 * 60
        print(f"  {ns_per_day} ns/day, {prod_ns:.1f} ns prod → {mins_needed:.0f} min total")
