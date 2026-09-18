
# Inspect mol_type distribution and check token counts
import numpy as np

BASE = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/job-6567207/ternary_out"

npz = np.load(f"{BASE}/gspt1_crbn_glue_0.npz")
mol_type = npz['mol_type']

print("mol_type value counts:")
for v, c in zip(*np.unique(mol_type, return_counts=True)):
    labels = {0: 'protein', 1: 'DNA', 2: 'RNA', 3: 'ligand'}
    print(f"  {v} ({labels.get(int(v),'?')}): {c} tokens")

print(f"\nTotal tokens: {len(mol_type)}")
print(f"Protein tokens: {(mol_type==0).sum()}  (expected 199+406=605)")
print(f"Ligand tokens:  {(mol_type==3).sum()}")
