
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyArrow, Polygon
from scipy.interpolate import CubicSpline
from scipy.spatial.transform import Rotation

# ── Pocket residue sets (from earlier analysis) ───────────────────────────────
MAIN_RES  = {351,352,353,354,355,356,357,358,359,379,380,381,382,388,402,404}
ALLO_RES  = {384,385,386,387,405,406,407,408,409,410,411,412,413,414,415}
ZINC_RES  = {325,328,368,369,370,371,393,394,395,396}
LVY_XYZ   = np.array([[ 84.230,156.371,13.871],[ 85.153,156.878,15.009],
                       [ 84.846,158.363,15.282],[ 85.010,159.150,14.003],
                       [ 84.782,158.539,12.808],[ 84.432,157.230,12.643],
                       [ 84.106,152.712,13.165],[ 85.417,153.010,12.790],
                       [ 85.721,154.487,12.998],[ 84.453,154.974,13.532],
                       [ 83.502,154.007,13.641],[ 84.453,150.404,12.599],
                       [ 85.790,150.710,12.234],[ 86.300,152.026,12.319],
                       [ 83.580,151.414,13.063],[ 82.330,154.090,14.040],
                       [ 87.576,152.361,11.975],[ 84.217,156.737,11.543],
                       [ 85.305,160.331,14.074]])
ZN_XYZ    = np.array([[75.756,152.112,31.429]])

# ── Find best viewing plane via PCA on Cα coords ──────────────────────────────
mu = coords.mean(axis=0)
_, _, Vt = np.linalg.svd(coords - mu)
# Use PC1 (x-axis) and PC3 (y-axis) — gives best pocket separation
V1, V3 = Vt[0], Vt[2]

def proj(xyz):
    c = xyz - mu
    return c @ V1, c @ V3

px, py = proj(coords)

# Project ligand and Zn
lvy_px, lvy_py = proj(LVY_XYZ)
zn_px, zn_py   = proj(ZN_XYZ)

# Depth for z-ordering (PC2)
V2 = Vt[1]
depth = (coords - mu) @ V2

print("PCA projection done")
print(f"PC1 range: {px.min():.1f} – {px.max():.1f}")
print(f"PC3 range: {py.min():.1f} – {py.max():.1f}")

# Pocket centroids in projection
main_idx = [i for i,r in enumerate(res_ids) if int(r) in MAIN_RES]
allo_idx = [i for i,r in enumerate(res_ids) if int(r) in ALLO_RES]
zinc_idx = [i for i,r in enumerate(res_ids) if int(r) in ZINC_RES]

print(f"\nMain pocket Cα count: {len(main_idx)}")
print(f"Allo pocket Cα count: {len(allo_idx)}")
print(f"Zinc site  Cα count: {len(zinc_idx)}")
