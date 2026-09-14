
import pickle, os

pkl_path = "/home/ubuntu/rayca-sessions/2d89c255-6bf5-4e5c-a4fb-99e4f253a979-1320c8c41b74/protacfold_out/boltz_pred/boltz_results_ARV471_ERalpha_CRBN_ternary/processed/mols/ARV471_ERalpha_CRBN_ternary.pkl"
print(f"pkl size: {os.path.getsize(pkl_path)/1e3:.1f} KB")

with open(pkl_path, 'rb') as f:
    mols = pickle.load(f)

print(f"type: {type(mols)}")
if isinstance(mols, dict):
    for k, v in mols.items():
        print(f"  {k}: {type(v)}")
elif isinstance(mols, (list, tuple)):
    print(f"  len={len(mols)}, first item type={type(mols[0]) if mols else 'empty'}")
else:
    print(f"  value: {mols}")
