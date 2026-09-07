
# Full missing-residue list for chain B
b_missing = sorted([(seq, res) for ch, seq, res in missing_res if ch == 'B'])
print(f"Chain B — all {len(b_missing)} missing biological residues:")
print(b_missing)

a_missing = sorted([(seq, res) for ch, seq, res in missing_res if ch == 'A' and seq > 0])
print(f"\nChain A — all {len(a_missing)} missing biological residues:")
print(a_missing)
