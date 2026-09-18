
# ── Grid-based cavity detection (Fpocket-lite approach) ─────────────────────
# Strategy: probe grid points that are (a) at least 1.4 Å from any protein atom
# (no steric clash) and (b) within 5.5 Å of at least one protein atom (buried).
# Cluster surviving probe points and score by count; exclude already-known pockets.

from scipy.spatial import cKDTree
from scipy.ndimage import label as ndlabel

# Build coordinate arrays
prot_coords = np.array([[a['x'],a['y'],a['z']] for a in protein])
tree = cKDTree(prot_coords)

# Bounding box + 5 Å padding, 1.5 Å grid spacing
pad  = 5.0
step = 1.5
xmin,ymin,zmin = prot_coords.min(axis=0) - pad
xmax,ymax,zmax = prot_coords.max(axis=0) + pad

xs = np.arange(xmin, xmax, step)
ys = np.arange(ymin, ymax, step)
zs = np.arange(zmin, zmax, step)
print(f"Grid size: {len(xs)}×{len(ys)}×{len(zs)} = {len(xs)*len(ys)*len(zs):,} points")

# For each grid point: find nearest atom distance and count atoms within 5.5 Å
# Use cKDTree for speed
XX, YY, ZZ = np.meshgrid(xs, ys, zs, indexing='ij')
grid_pts = np.stack([XX.ravel(), YY.ravel(), ZZ.ravel()], axis=1)

# Nearest-atom distance
near_dist, _ = tree.query(grid_pts, k=1)
# Count atoms within 5.5 Å (buried criterion)
buried_counts = tree.query_ball_point(grid_pts, r=5.5, return_length=True)

# Pocket criteria: not inside protein (>1.4 Å), but enclosed (≥8 atoms within 5.5 Å)
probe_mask = (near_dist > 1.4) & (buried_counts >= 8)
print(f"Probe points passing filter: {probe_mask.sum():,}")

# Store surviving grid indices for clustering
probe_idx = np.where(probe_mask)[0]
probe_coords = grid_pts[probe_idx]
print("Done finding probe points.")
