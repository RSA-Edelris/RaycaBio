
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
from pathlib import Path

# Debug parse on the "bad" file
def parse_mmpbsa(d):
    dat = Path(d) / "FINAL_RESULTS_MMPBSA.dat"
    if not dat.exists():
        return None
    text = dat.read_text()
    result = {}
    in_diff = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("Differences"):
            in_diff = True
        if not in_diff:
            continue
        for key in ["VDWAALS", "EEL", "EGB", "ESURF", "DELTA G gas", "DELTA G solv", "DELTA TOTAL"]:
            if s.startswith(key):
                parts = s.split()
                try:
                    result[key] = float(parts[-3])
                    result[key + "_std"] = float(parts[-1])
                except (IndexError, ValueError):
                    pass
    return result if result else None

bad_dir = f"{BASE}/mmgbsa/EDEL-CRBN-0002_ent"
result = parse_mmpbsa(bad_dir)
print(f"Parse result: {result}")

# Debug each line in Differences section
dat = Path(bad_dir) / "FINAL_RESULTS_MMPBSA.dat"
text = dat.read_text()
in_diff = False
print("\nDiff section lines:")
for line in text.split("\n"):
    s = line.strip()
    if s.startswith("Differences"):
        in_diff = True
        print(f"  FOUND DIFF HEADER: {repr(s[:40])}")
    if in_diff:
        for key in ["VDWAALS", "EEL", "EGB", "ESURF", "DELTA G gas", "DELTA G solv", "DELTA TOTAL"]:
            if s.startswith(key):
                parts = s.split()
                print(f"  key={key}  len={len(parts)}  last3={parts[-3]}  last1={parts[-1]}")
