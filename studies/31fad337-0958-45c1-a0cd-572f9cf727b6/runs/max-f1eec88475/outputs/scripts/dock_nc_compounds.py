#!/usr/bin/env python3
"""
Dock NC-001 to NC-010 with gnina, extract best poses, save SDF files.
Identical box/params as the 84-compound campaign.
Reads gnina_docked.sdf.gz from the session workspace immediately after each call.
"""
import sys, json, gzip, time, shutil
sys.path.insert(0, "/home/ubuntu/rayca-modulon/src")

from pathlib import Path
from modulon.governance.toolkit import run_aidd_tool
from rdkit import Chem

SESS    = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f")
WDIR    = SESS / "cdk2_campaign"
SDF_GZ  = SESS / "gnina_docked.sdf.gz"
REC     = str(WDIR / "receptor_raw.pdb")
LIG_DIR = WDIR / "ligands_prepared"
POSES   = WDIR / "poses_all"
POSES.mkdir(exist_ok=True)
RESULTS = WDIR / "nc_docking_results.json"

BOX = dict(
    boxX=30.57, boxY=5.37, boxZ=-25.80,
    width=35, height=30, depth=31,
    numModes=9, cnnScoring="rescore", exhaustiveness=8, seed=42,
)

NC_NAMES = [f"NC-{i:03d}" for i in range(1, 11)]

# Load any existing results
if RESULTS.exists():
    existing = {r["name"]: r for r in json.loads(RESULTS.read_text())}
else:
    existing = {}

all_results = []
for name in NC_NAMES:
    out_sdf = POSES / f"{name}_best_pose.sdf"
    # Skip if already has both score and SDF
    if name in existing and out_sdf.exists() and existing[name].get("best_affinity") is not None:
        print(f"SKIP {name}: already done")
        all_results.append(existing[name])
        continue

    lig_path = str(LIG_DIR / f"{name}.sdf")
    t0 = time.time()
    try:
        r  = run_aidd_tool("gnina", {"proteinFile": REC, "ligandFile": lig_path, **BOX})
        o  = r.get("output", {})
        row = {
            "name":              name,
            "best_affinity":     o.get("best_affinity_kcal_mol"),
            "best_cnn_affinity": o.get("best_cnn_affinity"),
            "best_cnn_pose":     o.get("best_cnn_pose_score"),
            "num_poses":         o.get("num_poses", 0),
            "gpu_used":          o.get("gpu_used", False),
            "error":             "",
        }

        # Extract best pose from gnina_docked.sdf.gz
        if SDF_GZ.exists():
            with gzip.open(str(SDF_GZ), "rb") as gz:
                sdf_bytes = gz.read()
            tmp = POSES / f"_tmp_{name}.sdf"
            tmp.write_bytes(sdf_bytes)
            suppl = Chem.SDMolSupplier(str(tmp), removeHs=False)
            best_mol = next((m for m in suppl if m is not None), None)
            tmp.unlink(missing_ok=True)
            if best_mol is not None:
                best_mol.SetProp("_Name", name)
                w = Chem.SDWriter(str(out_sdf))
                w.write(best_mol)
                w.close()
                row["best_pose_sdf"] = str(out_sdf)
                print(f"  pose saved: {out_sdf.name} ({best_mol.GetNumAtoms()} atoms)")
            else:
                row["best_pose_sdf"] = ""
                print(f"  WARN: SDF.gz unreadable for {name}")
        else:
            row["best_pose_sdf"] = ""
            print(f"  WARN: gnina_docked.sdf.gz not found for {name}")

    except Exception as e:
        row = {"name": name, "best_affinity": None, "best_cnn_affinity": None,
               "best_cnn_pose": None, "num_poses": 0, "gpu_used": False,
               "error": str(e), "best_pose_sdf": ""}

    dt  = time.time() - t0
    aff = row.get("best_affinity")
    cnn = row.get("best_cnn_affinity")
    if aff is not None and cnn is not None:
        tag = f"Vina={aff:.2f}  CNN_pKi={cnn:.3f}"
    else:
        tag = f"ERROR: {row['error'][:80]}"
    print(f"{name}: {tag}  ({dt:.0f}s)", flush=True)

    all_results.append(row)
    RESULTS.write_text(json.dumps(all_results, indent=2))

ok   = sum(1 for r in all_results if r.get("best_affinity") is not None)
sdfs = sum(1 for r in all_results if r.get("best_pose_sdf"))
print(f"\nDone: {ok}/{len(NC_NAMES)} docked, {sdfs}/{len(NC_NAMES)} SDF files saved")
print(f"Results: {RESULTS}")
