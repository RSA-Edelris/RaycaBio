
import os, gzip, re
from rdkit.Chem import MolFromMolBlock, SDWriter, AddHs, AllChem

# ── Re-read the gnina docked SDF from ART ──────────────────────────────────
gz_path = f"{ART}/gnina_docked.sdf.gz"
print("gnina gz exists:", os.path.exists(gz_path))

with gzip.open(gz_path, "rt") as fh:
    raw = fh.read()

# Split on $$$$ boundaries
blocks = [b + "\n$$$$\n" for b in raw.split("$$$$\n") if b.strip()]
print(f"Total blocks read: {len(blocks)}")

# ── Parse gnina scores via regex (RDKit reads them as 0) ──────────────────
def parse_props(block):
    props = {}
    for m in re.finditer(r'> <(\S+)>\n(.*?)\n', block):
        try:    props[m.group(1)] = float(m.group(2).strip())
        except: props[m.group(1)] = m.group(2).strip()
    return props

pose_data = [parse_props(b) for b in blocks[:5]]
print("\nGnina scores:")
for i, d in enumerate(pose_data, 1):
    print(f"  Pose {i}: Vina={d.get('minimizedAffinity','?'):.3f}  "
          f"CNN={d.get('CNNaffinity','?'):.3f}  CNNscore={d.get('CNNscore','?'):.3f}")

# ── Write clean SDFs (minimal, RDKit-canonicalised, with Hs) ──────────────
def write_clean_pose(block, path, name):
    mol = MolFromMolBlock(block.split("$$$$")[0], removeHs=True, sanitize=True)
    if mol is None:
        raise ValueError(f"RDKit could not parse block for {name}")
    mol.SetProp("_Name", name)
    mol_h = AddHs(mol, addCoords=True)
    # Assign stereochemistry if needed
    AllChem.AssignStereochemistry(mol_h, cleanIt=True, force=True)
    # Write
    w = SDWriter(path)
    w.write(mol_h)
    w.close()
    print(f"  Written {path}  ({os.path.getsize(path)} bytes)")

for i, blk in enumerate(blocks[:5], 1):
    pname = f"clean_pose_{i}"
    fpath = f"{WS}/{pname}.sdf"
    write_clean_pose(blk, fpath, pname)

print("\nAll clean poses written.")
