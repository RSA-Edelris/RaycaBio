
import os, shutil
from modulon.governance.toolkit import run_aidd_tool

poses_dir = f"{WORK}/poses"
RECEPTOR = f"{WORK}/4CI2_receptor_for_docking.pdb"
BOX = dict(boxX=84.800, boxY=154.937, boxZ=13.242,
           width=24, height=24, depth=24,
           numModes=5, cnnScoring="rescore", seed=0)

BATCH3 = [
    ("EDEL-CRBN-0009",     f"{WORK}/ligands/lig17.sdf"),
    ("EDEL-CRBN-0009_ent", f"{WORK}/ligands/lig18.sdf"),
    ("EDEL-CRBN-0010",     f"{WORK}/ligands/lig19.sdf"),
    ("EDEL-CRBN-0010_ent", f"{WORK}/ligands/lig20.sdf"),
    ("EDEL-CRBN-0011",     f"{WORK}/ligands/lig21.sdf"),
    ("EDEL-CRBN-0011_ent", f"{WORK}/ligands/lig22.sdf"),
    ("EDEL-CRBN-0012",     f"{WORK}/ligands/lig23.sdf"),
    ("EDEL-CRBN-0012_ent", f"{WORK}/ligands/lig24.sdf"),
]

for name, lig_file in BATCH3:
    out_path = f"{poses_dir}/{name}_poses.sdf.gz"
    if os.path.exists(out_path):
        print(f"  SKIP {name}")
        continue
    r = run_aidd_tool("gnina", {"proteinFile": RECEPTOR, "ligandFile": lig_file, **BOX})
    shutil.copy(f"{WORK}/gnina_docked.sdf.gz", out_path)
    aff = r.get('output', {}).get('best_affinity_kcal_mol', 'n/a')
    print(f"  OK  {name:27s}  {aff} kcal/mol")

print(f"Batch 3/4 done. Files: {len(os.listdir(poses_dir))}")
