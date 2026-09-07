
from pathlib import Path
import json

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

lvy_ref = (BASE / "4CI2_LVY_ref.pdb").read_text()
print("=== 4CI2_LVY_ref.pdb (first 10 lines) ===")
for l in lvy_ref.splitlines()[:10]:
    print(repr(l))

rec = (BASE / "4CI2_receptor_for_docking.pdb").read_text()
chains = set()
atom_n = hetatm_n = 0
for l in rec.splitlines():
    if l.startswith("ATOM"):
        chains.add(l[21]); atom_n += 1
    elif l.startswith("HETATM"):
        chains.add(l[21]); hetatm_n += 1
print(f"\nChains in receptor: {sorted(chains)}")
print(f"ATOM: {atom_n}, HETATM: {hetatm_n}")
