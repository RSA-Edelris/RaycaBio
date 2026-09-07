
from pathlib import Path
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# Count $$$$ separators and look for embedded ones in properties
sdf_text = (BASE / "final_calculation.sdf").read_text()
terminators = [i for i, line in enumerate(sdf_text.splitlines()) if line.strip() == "$$$$"]
print(f"$$$$ count: {len(terminators)} (expected 22)")
print(f"First 3 at lines: {terminators[:3]}")

# Look at lines around the first None record (after first $$$$)
lines = sdf_text.splitlines()
t0 = terminators[0]
print(f"\nLines {t0-2} to {t0+8}:")
for i in range(max(0, t0-2), min(len(lines), t0+9)):
    print(f"  {i:4d}: {repr(lines[i])}")
