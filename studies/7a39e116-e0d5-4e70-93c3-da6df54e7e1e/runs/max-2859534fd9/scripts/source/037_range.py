
import os

receptor_path = f"{WS}/1Z5M_receptor_pH7.4.pdb"
gbsa_results = {
    1: {
        "Van der Waals": -55.294, "Electrostatic": -5.501,
        "Polar Solvation": 9.290, "Non-Polar Solvation": -6.329,
        "Gas": -60.795, "TOTAL": -57.834
    }
}

for pose_idx in range(2, 6):
    pose_key = f"clean_pose_{pose_idx}.sdf"
    pose_path = f"{WS}/{pose_key}"
    print(f"\n--- Pose {pose_idx} (exists: {os.path.exists(pose_path)}, {os.path.getsize(pose_path)} bytes) ---")

    files_i = {
        "1Z5M_receptor_pH7.4.pdb": receptor_path,
        pose_key: pose_path,
    }

    res_i = dispatch("gbsa", {
        "task": "protein-ligand",
        "mode": "em",
        "method": "gb",
        "proteinFile": "1Z5M_receptor_pH7.4.pdb",
        "ligandFile": pose_key,
        "proteinForceField": "amber03",
        "ligandForceField": "gaff2",
        "ligandCharge": "gas",
        "threads": 8,
        "decompose": True
    }, files=files_i, gpu=True, timeout=600)

    rc  = res_i.get("rc", -1)
    out = res_i.get("output", {})
    print(f"  rc={rc}  best_dG={out.get('best_dG_kcal_per_mol')}")
    if rc != 0:
        # print truncated error for diagnosis
        err = res_i.get("summary","")
        print(f"  ERROR: {err[:400]}")
        continue

    # parse results
    results_list = out.get("results") or []
    if results_list and results_list[0].get("TOTAL"):
        r = results_list[0]
        gbsa_results[pose_idx] = {k: float(v) for k, v in r.items()
                                  if k in ("Van der Waals","Electrostatic",
                                           "Polar Solvation","Non-Polar Solvation",
                                           "Gas","TOTAL")}
    else:
        gbsa_results[pose_idx] = {"TOTAL": float(out.get("best_dG_kcal_per_mol", 0))}

    print(f"  TOTAL={gbsa_results[pose_idx]['TOTAL']:.2f} kcal/mol  "
          f"VdW={gbsa_results[pose_idx].get('Van der Waals','?')}  "
          f"Elec={gbsa_results[pose_idx].get('Electrostatic','?')}")

print("\n=== Summary ===")
for p, r in sorted(gbsa_results.items()):
    print(f"  Pose {p}: {r.get('TOTAL','?'):.2f} kcal/mol")
