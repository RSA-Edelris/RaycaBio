
import numpy as np, pickle, requests, io
from Bio import PDB

# ── Fetch VHL-based PROTAC ternary complex: 6BOY ─────────────────────────────
# 6BOY = dBET1 PROTAC / BRD4-BD1 / VHL-ElonginB-ElonginC (Nowak 2018, Science)
# BRD4-BD1 is the *degradation target* here (Lys side), VHL is the E3 receptor.
# We can extract: target-Lys Nz distances to the VHL binding interface.

r = requests.get("https://files.rcsb.org/download/6BOY.pdb", timeout=30)
pdb_6boy = r.text
pp = PDB.PDBParser(QUIET=True)
s6 = pp.get_structure("6BOY", io.StringIO(pdb_6boy))

print("=== 6BOY chains (dBET1/BRD4-BD1/VHL ternary) ===")
for chain in s6[0]:
    prot = [res for res in chain if res.id[0]==' ']
    het  = [res for res in chain if res.id[0] not in (' ','W')]
    if prot:
        nums=[r.id[1] for r in prot]
        print(f"  Chain {chain.id}: {len(prot)} aa ({min(nums)}-{max(nums)})")
    for h in het:
        com = np.mean([a.coord for a in h.get_atoms()],axis=0)
        print(f"  Ligand {h.resname}: CoM {com.round(1)}")
