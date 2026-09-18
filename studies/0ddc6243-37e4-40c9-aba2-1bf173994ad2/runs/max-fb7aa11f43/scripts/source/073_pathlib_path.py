
import subprocess, pathlib

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")

# Find gaff2.dat
r = subprocess.run(["find", "/home/ubuntu/rayca-runtime/.mamba/envs/rayca", "-name", "gaff2.dat"],
                   capture_output=True, text=True)
gaff2_dat = r.stdout.strip().splitlines()[0]
print("gaff2.dat:", gaff2_dat)

# Pull DIHE section entries that involve c1, ce-n, or c-ns
lines = pathlib.Path(gaff2_dat).read_text().splitlines()
in_dihe = False
hits = []
for l in lines:
    if l.startswith("DIHE"): in_dihe = True; continue
    if in_dihe and l.strip() == "": in_dihe = False; continue
    if not in_dihe: continue
    # Look for relevant analogues
    types = l[:11].replace(" ", "")
    for key in ["c1-", "-c1", "ce-n", "c-ns", "ns-c", "ns-h"]:
        if key in types.lower():
            hits.append(l)
            break

print(f"\nRelevant GAFF2 DIHE entries ({len(hits)}):")
for l in hits[:30]:
    print(l)
