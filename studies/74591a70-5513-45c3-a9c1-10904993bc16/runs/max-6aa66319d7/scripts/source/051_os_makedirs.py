
import os, shutil
from modulon.governance.toolkit import run_aidd_tool

poses_dir = f"{WORK}/poses"
os.makedirs(poses_dir, exist_ok=True)

RECEPTOR = f"{WORK}/4CI2_receptor_for_docking.pdb"

LIGAND_FILES = [
    ("EDEL-CRBN-0001",     f"{WORK}/ligands/lig1.sdf"),
    ("EDEL-CRBN-0001_ent", f"{WORK}/ligands/lig2.sdf"),
    ("EDEL-CRBN-0002",     f"{WORK}/ligands/lig3.sdf"),
    ("EDEL-CRBN-0002_ent", f"{WORK}/ligands/lig4.sdf"),
    ("EDEL-CRBN-0003",     f"{WORK}/ligands/lig5.sdf"),
    ("EDEL-CRBN-0003_ent", f"{WORK}/ligands/lig6.sdf"),
    ("EDEL-CRBN-0004",     f"{WORK}/ligands/lig7.sdf"),
    ("EDEL-CRBN-0004_ent", f"{WORK}/ligands/lig8.sdf"),
]

BOX = dict(boxX=84.800, boxY=154.937, boxZ=13.242,
           width=24, height=24, depth=24,
           numModes=5, cnnScoring="rescore", seed=0)

pose_results = {}
for name, lig_file in LIGAND_FILES:
    out_path = f"{poses_dir}/{name}_poses.sdf.gz"
    if os.path.exists(out_path):
        print(f"  SKIP {name} (already exists)")
        pose_results[name] = out_path
        continue
    try:
        r = run_aidd_tool("gnina", {"proteinFile": RECEPTOR, "ligandFile": lig_file, **BOX})
        src = f"{WORK}/gnina_docked.sdf.gz"
        shutil.copy(src, out_path)
        pose_results[name] = out_path
        aff = r.get('output', {}).get('best_affinity_kcal_mol', 'n/a')
        print(f"  OK  {name:27s}  {aff} kcal/mol  -> {os.path.basename(out_path)}")
    except Exception as e:
        print(f"  ERR {name}: {e}")

print(f"\nBatch 1/4 done: {len(pose_results)} pose files")
