
# Inspect all property keys in first block to find correct score field names
print("=== Properties in pose 1 ===")
for k, v in pose_records[0]['props'].items():
    print(f"  {k!r}: {v!r}")

print("\n=== First 40 lines of block 1 ===")
for ln in pose_records[0]['block'].splitlines()[:40]:
    print(ln)
