
import os, shutil
from modulon.governance.toolkit import run_aidd_tool

poses_dir = f"{WORK}/poses"
RECEPTOR = f"{WORK}/4CI2_receptor_for_docking.pdb"
BOX = dict(boxX=84.800, boxY=154.937, boxZ=13.242,
           width=24, height=24, depth=24,
           numModes=5, cnnScoring="rescore", seed=0)

BATCH2 = [
    ("EDEL-CRBN-0005",     f"{WORK}/ligands/lig9.sdf"),
    ("EDEL-CRBN-0005_ent", f"{WORK}/ligands/lig10.sdf"),
    ("EDEL-CRBN-0006",     f"{WORK}/ligands/lig11.sdf"),
    ("EDEL-CRBN-0006_ent", f"{WORK}/ligands/lig12.sdf"),
    ("EDEL-CRBN-0007",     f"{WORK}/ligands/lig13.sdf"),
    ("EDEL-CRBN-0007_ent", f"{WORK}/ligands/lig14.sdf"),
    ("EDEL-CRBN-0008",     f"{WORK}/ligands/lig15.sdf"),
    ("EDEL-CRBN-0008_ent", f"{WORK}/ligands/lig16.sdf"),
]

for name, lig_file in BATCH2:
    out_path = f"{poses_dir}/{name}_poses.sdf.gz"
    if os.path.exists(out_path):
        print(f"  SKIP {name}")
        continue
    r = run_aidd_tool("gnina", {"proteinFile": RECEPTOR, "ligandFile": lig_file, **BOX})
    shutil.copy(f"{WORK}/gnina_docked.sdf.gz", out_path)
    aff = r.get('output', {}).get('best_affinity_kcal_mol', 'n/a')
    print(f"  OK  {name:27s}  {aff} kcal/mol")

print(f"\nBatch 2/4 done. Pose files so far: {len(os.listdir(poses_dir))}")
