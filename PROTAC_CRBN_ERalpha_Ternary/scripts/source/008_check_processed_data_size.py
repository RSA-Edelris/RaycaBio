
import numpy as np, os

# Check processed data size
npz_path = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/protacfold_out/boltz_pred/boltz_results_ARV471_ERalpha_CRBN_ternary/processed/structures/ARV471_ERalpha_CRBN_ternary.npz"
size_mb = os.path.getsize(npz_path) / 1e6
print(f"structures npz size: {size_mb:.2f} MB")
data = np.load(npz_path, allow_pickle=True)
for k in data.files:
    v = data[k]
    print(f"  {k}: shape={getattr(v,'shape','scalar')} dtype={getattr(v,'dtype','?')}")
