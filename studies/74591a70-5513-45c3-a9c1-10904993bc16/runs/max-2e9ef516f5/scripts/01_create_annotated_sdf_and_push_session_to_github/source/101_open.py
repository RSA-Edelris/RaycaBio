
import json
from pathlib import Path

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"

with open(f"{BASE}/mmgbsa/combined_results.json") as f:
    data = json.load(f)

rows = {r["name"]: r for r in data["ranked"]}

# Build one SDF with all 32 best poses, annotated with scores
# SDF property block: > <PROP_NAME>\nvalue\n\n
out_lines = []
missing = []

for row in data["ranked"]:
    name = row["name"]
    # Find the pose SDF
    pose_file = Path(f"{BASE}/best_poses/{name}_pose1.sdf")
    if not pose_file.exists():
        missing.append(name)
        continue
    text = pose_file.read_text()
    # Strip trailing $$$$ and whitespace
    mol_block = text.strip()
    if mol_block.endswith("$$$$"):
        mol_block = mol_block[:-4].rstrip()
    # Add properties
    props = [
        ("Compound_ID",        name),
        ("Vina_dG_kcal_mol",   f"{row['vina_dg']:.3f}"),
        ("CNN_pKd",            f"{row['cnn_pkd']:.3f}"),
        ("GBSA_dG_kcal_mol",   f"{row['gbsa_dg']:.3f}"),
        ("GBSA_dG_std",        f"{row['gbsa_std']:.3f}"),
        ("GBSA_VDWAALS",       f"{row['vdwaals']:.3f}"),
        ("GBSA_EEL",           f"{row['eel']:.3f}"),
        ("GBSA_EGB",           f"{row['egb']:.3f}"),
        ("GBSA_ESURF",         f"{row['esurf']:.3f}"),
        ("GBSA_rank",          str(data["ranked"].index(row) + 1)),
    ]
    prop_block = ""
    for k, v in props:
        prop_block += f"> <{k}>\n{v}\n\n"
    out_lines.append(mol_block + "\n" + prop_block + "$$$$\n")

out_path = Path(f"{BASE}/CRBN_32_ligands_docking_GBSA.sdf")
out_path.write_text("".join(out_lines))

print(f"Written: {out_path}")
print(f"Compounds: {len(out_lines)} / 32")
if missing:
    print(f"Missing pose files: {missing}")
print(f"File size: {out_path.stat().st_size/1024:.1f} KB")
