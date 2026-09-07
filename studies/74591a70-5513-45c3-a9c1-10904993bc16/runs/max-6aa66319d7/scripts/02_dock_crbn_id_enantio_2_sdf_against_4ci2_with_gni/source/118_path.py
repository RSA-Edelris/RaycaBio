
import os
from pathlib import Path
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# Check key files
for fname in ["4CI2_receptor_for_docking.pdb", "ligs2/Compound_1_ent1.sdf", "CRBN_ID_enantio_2.sdf"]:
    p = BASE / fname
    exists = p.exists()
    size = p.stat().st_size if exists else 0
    print(f"{fname}: exists={exists}, size={size}")

# Check workspace
print(f"\nCWD: {os.getcwd()}")

# List ligs2 files
ligs2 = BASE / "ligs2"
if ligs2.exists():
    files = sorted(ligs2.iterdir())
    print(f"\nligs2/ contains {len(files)} files")
    for f in files[:3]:
        print(f"  {f.name}: {f.stat().st_size} bytes")
