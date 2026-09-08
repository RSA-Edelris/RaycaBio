
import os

# Confirm all files exist
files_to_stage = {
    "1Z5M_receptor_pH7.4.pdb": f"{ART}/1Z5M_receptor_pH7.4.pdb",
    "pose_1.sdf": f"{ART}/pose_1.sdf",
    "pose_2.sdf": f"{ART}/pose_2.sdf",
    "pose_3.sdf": f"{ART}/pose_3.sdf",
    "pose_4.sdf": f"{ART}/pose_4.sdf",
    "pose_5.sdf": f"{ART}/pose_5.sdf",
}
for name, path in files_to_stage.items():
    print(f"  {name}: exists={os.path.exists(path)}  size={os.path.getsize(path) if os.path.exists(path) else 'MISSING'}")

# Dispatch Uni-GBSA: MM/GBSA with GROMACS MD (1 ns) for all 5 poses
print("\nDispatching Uni-GBSA (MD 1 ns + MM/GBSA for 5 poses)...")
result_gbsa = dispatch("gbsa", {
    "task": "protein-ligand",
    "mode": "md",
    "method": "gb",
    "proteinFile": "1Z5M_receptor_pH7.4.pdb",
    "ligandFiles": ["pose_1.sdf","pose_2.sdf","pose_3.sdf","pose_4.sdf","pose_5.sdf"],
    "proteinForceField": "amber03",
    "ligandForceField": "gaff2",
    "ligandCharge": "bcc",
    "nsteps": 500000,
    "nframe": 100,
    "decompose": True,
    "threads": 8,
    "boxSize": 0.9,
    "conc": 0.15
}, files=files_to_stage, gpu=True, timeout=3600)

print("rc:", result_gbsa.get("rc"))
print("summary:", result_gbsa.get("summary",""))
out_g = result_gbsa.get("output", {})
print("best_dG_kcal_per_mol:", out_g.get("best_dG_kcal_per_mol"))
print("gpu_used:", out_g.get("gpu"))
print("results:", out_g.get("results"))
# Save the CSV if present
csv_data = out_g.get("binding_energy_csv","")
if csv_data:
    with open(f"{WS}/gbsa_results.csv","w") as f:
        f.write(csv_data)
    print("CSV saved:", len(csv_data), "chars")
