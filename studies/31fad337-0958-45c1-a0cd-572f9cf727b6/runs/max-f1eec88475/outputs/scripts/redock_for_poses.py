#!/usr/bin/env python3
"""
Re-dock 63 compounds that are missing pose SDF files.
Saves the best (rank-1) pose to poses_all/{name}_best_pose.sdf.
Also copies existing top-20 SDF best poses into poses_all/.
"""
import json, gzip, sys, shutil, time
from pathlib import Path
from modulon.governance.toolkit import run_aidd_tool
from rdkit import Chem

WDIR    = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC     = str(WDIR / "receptor_raw.pdb")
LIG_DIR = str(WDIR / "ligands_prepared")
SDF_GZ  = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/gnina_docked.sdf.gz")

POSES_ALL = WDIR / "poses_all"
POSES_ALL.mkdir(exist_ok=True)

BOX = dict(boxX=30.57, boxY=5.37, boxZ=-25.80,
           width=35, height=30, depth=31,
           numModes=5, cnnScoring="rescore", exhaustiveness=8, seed=42)

# ── 1. Copy existing top-20 best poses into poses_all/ ───────────────────────
top20_dir = WDIR / "poses_top20"
copied = 0
for sdf in sorted(top20_dir.glob("*.sdf")):
    # Keep only best (first) pose
    suppl = Chem.SDMolSupplier(str(sdf), removeHs=False)
    best = next((m for m in suppl if m is not None), None)
    if best is None:
        continue
    name = sdf.stem.replace("_poses", "")
    out = POSES_ALL / f"{name}_best_pose.sdf"
    w = Chem.SDWriter(str(out))
    w.write(best)
    w.close()
    copied += 1
print(f"Copied {copied} top-20 best poses to poses_all/")

# ── 2. Re-dock the 63 missing compounds ──────────────────────────────────────
need = json.loads((WDIR / "redock_list.json").read_text())
print(f"Re-docking {len(need)} compounds sequentially...")

done = 0
failed = 0
for i, name in enumerate(need):
    out = POSES_ALL / f"{name}_best_pose.sdf"
    if out.exists():
        print(f"  [{i+1}/{len(need)}] {name}: already done, skip")
        done += 1
        continue

    lig = f"{LIG_DIR}/{name}.sdf"
    t0 = time.time()
    try:
        r = run_aidd_tool("gnina", {"proteinFile": REC, "ligandFile": lig, **BOX})
        o = r.get("output", {})

        # Copy the SDF.gz while it's still there
        if SDF_GZ.exists():
            with gzip.open(str(SDF_GZ), "rb") as gz:
                sdf_bytes = gz.read()
            # Write temporary full SDF, then keep only best pose
            tmp = POSES_ALL / f"_tmp_{name}.sdf"
            tmp.write_bytes(sdf_bytes)
            suppl = Chem.SDMolSupplier(str(tmp), removeHs=False)
            best = next((m for m in suppl if m is not None), None)
            tmp.unlink()
            if best is not None:
                w = Chem.SDWriter(str(out))
                w.write(best)
                w.close()
                dt = time.time() - t0
                print(f"  [{i+1}/{len(need)}] {name}: Vina={o.get('best_affinity_kcal_mol','?')} CNN={o.get('best_cnn_affinity','?')} [{dt:.1f}s]")
                done += 1
            else:
                print(f"  [{i+1}/{len(need)}] {name}: SDF unreadable")
                failed += 1
        else:
            print(f"  [{i+1}/{len(need)}] {name}: SDF.gz not found")
            failed += 1
    except Exception as e:
        print(f"  [{i+1}/{len(need)}] {name}: ERROR {e}")
        failed += 1

print(f"\nDone: {done} succeeded, {failed} failed")
sdf_files = list(POSES_ALL.glob("*_best_pose.sdf"))
print(f"Total SDF files in poses_all/: {len(sdf_files)}")
