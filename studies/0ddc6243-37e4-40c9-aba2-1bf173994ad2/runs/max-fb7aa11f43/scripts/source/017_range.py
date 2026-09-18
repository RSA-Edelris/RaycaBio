
import numpy as np
import os

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

# ---------- 1. Confidence NPZ files ----------
for i in range(3):
    npz = np.load(f"{BASE}/gspt1_crbn_glue_{i}.npz")
    print(f"\n=== Model {i} confidence keys: {list(npz.files)} ===")
    for k in npz.files:
        arr = npz[k]
        print(f"  {k}: shape={arr.shape} dtype={arr.dtype}  "
              f"min={arr.min():.4f} mean={arr.mean():.4f} max={arr.max():.4f}")
