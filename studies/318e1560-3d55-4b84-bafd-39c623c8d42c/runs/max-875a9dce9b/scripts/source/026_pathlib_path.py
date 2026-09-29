
import pathlib
from collections import Counter

work_dir = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb/brd4_vhl_protac")
out_pdb = work_dir / "BRD4BD1_VHL_ternary_model.pdb"

# Count atoms per chain and collect REMARK lines
chain_counts = Counter()
remark_lines = []
sample_lines = {}  # first ATOM line per chain
with open(out_pdb) as f:
    for line in f:
        if line.startswith("REMARK"):
            remark_lines.append(line.rstrip())
        if line[:4] in ("ATOM","HETA"):
            ch = line[21]
            chain_counts[ch] += 1
            if ch not in sample_lines:
                sample_lines[ch] = line.rstrip()

print("=== REMARK lines ===")
for r in remark_lines:
    print(r)
print()
print("=== Atom counts per chain ===")
for ch in sorted(chain_counts):
    print(f"  chain {ch}: {chain_counts[ch]} records  first={sample_lines[ch][:40]}")
