
import os, shutil
from modulon.governance.toolkit import run_aidd_tool

poses_dir = f"{WORK}/poses"
RECEPTOR = f"{WORK}/4CI2_receptor_for_docking.pdb"
BOX = dict(boxX=84.800, boxY=154.937, boxZ=13.242,
           width=24, height=24, depth=24,
           numModes=5, cnnScoring="rescore", seed=0)

BATCH4 = [
    ("EDEL-CRBN-0013",     f"{WORK}/ligands/lig25.sdf"),
    ("EDEL-CRBN-0013_ent", f"{WORK}/ligands/lig26.sdf"),
    ("EDEL-CRBN-0014",     f"{WORK}/ligands/lig27.sdf"),
    ("EDEL-CRBN-0014_ent", f"{WORK}/ligands/lig28.sdf"),
    ("EDEL-CRBN-0015",     f"{WORK}/ligands/lig29.sdf"),
    ("EDEL-CRBN-0015_ent", f"{WORK}/ligands/lig30.sdf"),
    ("EDEL-CRBN-0016",     f"{WORK}/ligands/lig31.sdf"),
    ("EDEL-CRBN-0016_ent", f"{WORK}/ligands/lig32.sdf"),
]

for name, lig_file in BATCH4:
    out_path = f"{poses_dir}/{name}_poses.sdf.gz"
    if os.path.exists(out_path):
        print(f"  SKIP {name}")
        continue
    r = run_aidd_tool("gnina", {"proteinFile": RECEPTOR, "ligandFile": lig_file, **BOX})
    shutil.copy(f"{WORK}/gnina_docked.sdf.gz", out_path)
    aff = r.get('output', {}).get('best_affinity_kcal_mol', 'n/a')
    print(f"  OK  {name:27s}  {aff} kcal/mol")

total = len(os.listdir(poses_dir))
print(f"\nAll batches done. Total pose files: {total}/32")
