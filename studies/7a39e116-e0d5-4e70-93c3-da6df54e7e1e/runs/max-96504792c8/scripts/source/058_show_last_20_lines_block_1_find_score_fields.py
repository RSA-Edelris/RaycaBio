
# Show last 20 lines of block 1 to find score fields
print("=== Last 25 lines of block 1 ===")
b1_lines = pose_records[0]['block'].splitlines()
print(f"Total lines: {len(b1_lines)}")
for ln in b1_lines[-25:]:
    print(repr(ln))
