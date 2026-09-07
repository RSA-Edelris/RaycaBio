
import json
from pathlib import Path

BASE    = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
SDF_IN  = BASE / "CRBN_ID_enantio_2.sdf"
LIG_DIR = BASE / "ligs2"
LIG_DIR.mkdir(exist_ok=True)

# Split multi-compound SDF into individual files
text   = SDF_IN.read_text()
blocks = [b for b in text.split("$$$$") if b.strip()]
names  = []
for block in blocks:
    name = block.strip().split('\n')[0].strip()
    if not name:
        name = f"cpd_{len(names)+1}"
    out_path = LIG_DIR / f"{name}.sdf"
    out_path.write_text(block.strip() + "\n$$$$\n")
    names.append(name)

print(f"Wrote {len(names)} individual SDF files to {LIG_DIR.name}/")
print("Names:", names)
