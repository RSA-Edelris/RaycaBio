"""
Build a merged SDF for all 84 CDK2-CyclinE1 docked compounds with docking
scores and MM-GBSA binding free energy terms as SD properties.
"""
import json
from pathlib import Path
from rdkit import Chem

WDIR   = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
POSES  = WDIR / "poses_all"
OUT    = WDIR / "CDK2_CyclinE1_84compounds_docking_mmgbsa.sdf"

# --- load source tables --------------------------------------------------
dock_rows = {r["name"]: r
             for r in json.loads((WDIR / "docking_results.json").read_text())}

# Patch CTX-1020667 with re-docked values (original batch had null CNN pose;
# re-dock on 2026-09-06 with correct proteinFile field gave the values below)
redock = json.loads((WDIR / "CTX-1020667_docking_result.json").read_text())
if "CTX-1020667" in dock_rows:
    dock_rows["CTX-1020667"]["best_affinity"]     = redock.get("best_affinity_kcal_mol")
    dock_rows["CTX-1020667"]["best_cnn_affinity"] = redock.get("best_cnn_affinity")
    dock_rows["CTX-1020667"]["best_cnn_pose"]     = redock.get("best_cnn_pose_score")
    dock_rows["CTX-1020667"]["num_poses"]         = redock.get("num_poses", 9)

gbsa_list = json.loads((WDIR / "mmgbsa_results.json").read_text())
gbsa_rank = {r["ligandName"]: i + 1 for i, r in enumerate(gbsa_list)}

# Docking rank: sort by CNN pKi descending (uses patched CTX-1020667 value)
dock_list = sorted(dock_rows.values(),
                   key=lambda x: x.get("best_cnn_affinity") or 0,
                   reverse=True)
dock_rank = {r["name"]: i + 1 for i, r in enumerate(dock_list)}

# --- write SDF -----------------------------------------------------------
writer = Chem.SDWriter(str(OUT))
n_written = 0
n_missing = []

# Iterate in MM-GBSA rank order (rank 1 = best binder first)
for gbsa_row in gbsa_list:
    name = gbsa_row["ligandName"]
    sdf_path = POSES / f"{name}_best_pose.sdf"

    if not sdf_path.exists():
        n_missing.append(name)
        continue

    suppl = Chem.SDMolSupplier(str(sdf_path), removeHs=False)
    mol = next((m for m in suppl if m is not None), None)
    if mol is None:
        n_missing.append(name)
        continue

    mol.SetProp("_Name", name)

    # --- docking properties ---
    d = dock_rows.get(name, {})
    mol.SetProp("Docking_Rank",          str(dock_rank.get(name, "")))
    mol.SetProp("Vina_Affinity_kcal_mol", f"{d.get('best_affinity', ''):.3f}"
                if d.get("best_affinity") is not None else "")
    mol.SetProp("CNN_pKi",               f"{d.get('best_cnn_affinity', ''):.3f}"
                if d.get("best_cnn_affinity") is not None else "")
    mol.SetProp("CNN_Pose_Score",        f"{d.get('best_cnn_pose', ''):.4f}"
                if d.get("best_cnn_pose") is not None else "")
    mol.SetProp("Num_Docked_Poses",      str(d.get("num_poses", "")))

    # --- MM-GBSA properties ---
    g = gbsa_row
    mol.SetProp("MMGBSA_Rank",              str(gbsa_rank.get(name, "")))
    mol.SetProp("MMGBSA_dG_kcal_mol",       f"{g['dG_kcal_mol']:.3f}")
    mol.SetProp("MMGBSA_VdW_kcal_mol",      f"{g['Van_der_Waals']:.3f}"
                if g.get("Van_der_Waals") is not None else "")
    mol.SetProp("MMGBSA_Elec_kcal_mol",     f"{g['Electrostatic']:.3f}"
                if g.get("Electrostatic") is not None else "")
    mol.SetProp("MMGBSA_PolarSolv_kcal_mol",f"{g['Polar_Solvation']:.3f}"
                if g.get("Polar_Solvation") is not None else "")
    mol.SetProp("MMGBSA_NonPolarSolv_kcal_mol", f"{g['NonPolar_Solvation']:.3f}"
                if g.get("NonPolar_Solvation") is not None else "")
    mol.SetProp("MMGBSA_Status",            str(g.get("status", "")))

    writer.write(mol)
    n_written += 1

writer.close()
print(f"Written: {n_written} compounds → {OUT}")
if n_missing:
    print(f"Missing SDF ({len(n_missing)}): {n_missing}")
else:
    print("All 84 compounds written successfully.")
