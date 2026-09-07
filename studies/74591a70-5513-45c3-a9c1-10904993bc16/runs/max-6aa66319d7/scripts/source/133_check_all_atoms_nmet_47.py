
# Check all atoms in NMET 47
from pathlib import Path
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
rec_amber = Path(f"{BASE}/mmgbsa2/receptor_amber.pdb")

met47 = []
for line in rec_amber.read_text().splitlines():
    if not line.startswith('ATOM'):
        continue
    chain = line[21]
    resseq = line[22:26].strip()
    resname = line[17:20].strip()
    if resseq == '47' and chain == 'B':
        atom_name = line[12:16]  # raw 4-char field
        element = line[76:78].strip() if len(line) >= 78 else ''
        met47.append((atom_name, element, resname))

print(f"Total atoms in NMET 47: {len(met47)}")
for an, el, rn in met47:
    print(f"  [{an}] element={el}")

# Also check: what does AMBER ff14SB NMET template have?
# (look at the library file)
import subprocess
r = subprocess.run(
    ["grep", "-A", "40", '"NMET"', 
     "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/dat/leap/lib/amino14.lib"],
    capture_output=True, text=True
)
print("\nNMET template atoms (from amino14.lib):")
in_atoms = False
for line in r.stdout.splitlines()[:60]:
    if '!entry.NMET.unit.atoms' in line:
        in_atoms = True
    if in_atoms and line.startswith('!'):
        if '!entry.NMET.unit.atoms' not in line:
            break
    if in_atoms:
        print(line)
