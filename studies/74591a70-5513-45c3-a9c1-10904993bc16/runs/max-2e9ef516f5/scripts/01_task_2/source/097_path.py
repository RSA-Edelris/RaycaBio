
import json
from pathlib import Path

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
MMDIR = Path(BASE) / "mmgbsa"

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

# Load docking scores to get the 32 compound names and their dirs
with open(f"{BASE}/docking_scores_all32.json") as fh:
    scores = json.load(fh)

names = list(scores.keys())
compound_dirs = [f"{name}_ent" for name in names]

results = {}
ok, missing = [], []
for name, cdir in zip(names, compound_dirs):
    d = MMDIR / cdir
    r = parse_mmpbsa(d)
    if r and "DELTA TOTAL" in r:
        results[name] = r
        ok.append(name)
    else:
        missing.append((name, str(d)))

print(f"Parsed OK: {len(ok)} / {len(names)}")
if missing:
    print(f"Missing/failed: {len(missing)}")
    for n, d in missing:
        dat = Path(d) / "FINAL_RESULTS_MMPBSA.dat"
        print(f"  {n}: {'exists' if dat.exists() else 'NO FILE'}")

# Write updated mmgbsa_results.json
out = f"{MMDIR}/mmgbsa_results.json"
with open(out, "w") as fh:
    json.dump(results, fh, indent=2)
print(f"\nSaved {len(results)} results to mmgbsa_results.json")
