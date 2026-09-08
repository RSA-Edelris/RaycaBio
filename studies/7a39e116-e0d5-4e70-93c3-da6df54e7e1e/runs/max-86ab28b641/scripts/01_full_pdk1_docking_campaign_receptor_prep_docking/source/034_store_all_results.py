
import json, shutil

# Store all results
gbsa_results = {}

# Pose 1 already done
gbsa_results[1] = {
    "Van der Waals": -55.294,
    "Electrostatic": -5.501,
    "Polar Solvation": 9.290,
    "Non-Polar Solvation": -6.329,
    "Gas": -60.795,
    "TOTAL": -57.834,
    "Frames": 1,
    "mode": "em"
}
print("Pose 1 cached:", gbsa_results[1]["TOTAL"], "kcal/mol")

# Run poses 2-5 individually
receptor_path = f"{WS}/1Z5M_receptor_pH7.4.pdb"

for pose_idx in range(2, 6):
    pose_key = f"clean_pose_{pose_idx}.sdf"
    pose_path = f"{WS}/{pose_key}"
    
    print(f"\n--- Running gbsa for pose {pose_idx} ---")
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
    
    rc = res_i.get("rc", -1)
    out = res_i.get("output", {})
    print(f"  rc={rc}, best_dG={out.get('best_dG_kcal_per_mol')}")
    
    if rc == 0 and out.get("best_dG_kcal_per_mol"):
        # Try results list first
        results_list = out.get("results") or []
        if results_list and results_list[0].get("TOTAL"):
            r = results_list[0]
            gbsa_results[pose_idx] = {
                "Van der Waals":    float(r.get("Van der Waals", 0)),
                "Electrostatic":    float(r.get("Electrostatic", 0)),
                "Polar Solvation":  float(r.get("Polar Solvation", 0)),
                "Non-Polar Solvation": float(r.get("Non-Polar Solvation", 0)),
                "Gas":              float(r.get("Gas", 0)),
                "TOTAL":            float(r.get("TOTAL", 0)),
                "Frames": 1, "mode": "em"
            }
        else:
            # Fall back to best_dG and read CSV
            dg = out.get("best_dG_kcal_per_mol", 0.0)
            # Try to read the BindingEnergy.csv written to WS
            be_path = f"{WS}/BindingEnergy.csv"
            if os.path.exists(be_path):
                with open(be_path) as cf:
                    lines = cf.readlines()
                print(f"  BindingEnergy.csv lines: {lines}")
            gbsa_results[pose_idx] = {"TOTAL": dg, "mode": "em"}
    else:
        print(f"  FAILED for pose {pose_idx}")
        print(f"  summary: {res_i.get('summary','')}")

print("\n=== All GBSA results ===")
for p, r in sorted(gbsa_results.items()):
    print(f"Pose {p}: TOTAL={r.get('TOTAL','?'):.2f} kcal/mol  "
          f"VdW={r.get('Van der Waals','?')}  Elec={r.get('Electrostatic','?')}")
