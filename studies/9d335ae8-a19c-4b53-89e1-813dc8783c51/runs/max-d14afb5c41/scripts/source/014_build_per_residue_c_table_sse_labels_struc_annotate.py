
import numpy as np

# ── Build per-residue Cα table with SSE labels ────────────────────────────────
# struc.annotate_sse returns one label per residue in the protein structure
# Get unique residues (in order)
ca_mask = (protein.atom_name == "CA")
ca_atoms = protein[ca_mask]

res_ids   = ca_atoms.res_id       # residue numbers
res_names = ca_atoms.res_name     # 3-letter codes
coords    = ca_atoms.coord        # (N,3) float array

print(f"Cα residues: {len(res_ids)}  SSE len: {len(sse)}")
print(f"First 5 res_ids: {res_ids[:5]}, SSE: {sse[:5]}")
print(f"Last 5 res_ids:  {res_ids[-5:]}, SSE: {sse[-5:]}")

# Confirm 1-to-1 mapping
assert len(res_ids) == len(sse), f"Mismatch: {len(res_ids)} vs {len(sse)}"
print("1-to-1 mapping confirmed")

# SSE per residue number dict
sse_dict = {int(res_ids[i]): sse[i] for i in range(len(res_ids))}
print(f"\nHelix residues: {sum(1 for v in sse_dict.values() if v=='a')}")
print(f"Strand residues: {sum(1 for v in sse_dict.values() if v=='b')}")
print(f"Coil residues: {sum(1 for v in sse_dict.values() if v=='c')}")
