
# Spot-check: read first 80 and last 100 ATOM lines of ARV_001 model_0 to see chain letters,
# residue numbering scheme, and what's near K233.
pdb_path = f"{SESSION}/ARV_001/boltz_results_ARV_001_constrained/predictions/ARV_001_constrained/ARV_001_constrained_model_0.pdb"

atom_lines = []
with open(pdb_path) as f:
    for line in f:
        if line[:6] in ("ATOM  ", "HETATM"):
            atom_lines.append(line.rstrip())

print(f"Total ATOM/HETATM lines: {len(atom_lines)}")
print("\n=== First 10 ===")
for l in atom_lines[:10]:
    print(l)

print("\n=== Last 10 ===")
for l in atom_lines[-10:]:
    print(l)

# Find chain change boundaries
chains_seen = {}
for i, l in enumerate(atom_lines):
    ch = l[21]
    if ch not in chains_seen:
        chains_seen[ch] = (i, int(l[22:26].strip()), l[17:20].strip())
print(f"\nChain first appearances: {chains_seen}")

# What residues does each chain span?
chain_ranges = {}
for l in atom_lines:
    ch = l[21]
    resseq = int(l[22:26].strip())
    if ch not in chain_ranges:
        chain_ranges[ch] = [resseq, resseq]
    else:
        chain_ranges[ch][0] = min(chain_ranges[ch][0], resseq)
        chain_ranges[ch][1] = max(chain_ranges[ch][1], resseq)
print(f"Chain residue ranges: { {k: tuple(v) for k, v in chain_ranges.items()} }")

# Find K233 in chain A
k233_lines = [l for l in atom_lines if l[21]=='A' and l[22:26].strip()=='233']
print(f"\nK233 chain A atoms ({len(k233_lines)} atoms):")
for l in k233_lines:
    print(l)
