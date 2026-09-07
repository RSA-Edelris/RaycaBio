
import os

# Dispatch easy-md: AMBER14sb protein + OpenFF ligand, 2 ns NPT, CUDA A100
print("Dispatching easy-md (2 ns NPT, A100 CUDA)...")

result = run_aidd_tool("easy-md", {
    "protein_file":        "receptor_pH74_noH.pdb",
    "ligand_file":         "all_poses/EL2003A_pose2.sdf",
    "platform_name":       "CUDA",
    "platform_precision":  "mixed",
    "md_steps":            1000000,    # 2 ns  (1e6 × 2 fs)
    "md_npt":              True,
    "md_pressure":         1.0,
    "md_save_interval":    20000,      # frame every 40 ps → 50 frames
    "emin_steps":          20,
    "emin_target_temp":    300.0,
    "integrator_temperature": 300.0,
    "integrator_friction": 1.0,
    "integrator_timestep": 0.002,
    "solv_pH":             7.4,
    "solv_ionic_strength": 0.15,
    "solv_box_buffer":     10.0,
    "solv_model":          "tip3p",
    "run_analysis":        True,
}, gpu=True)

print("rc:", result.get("rc"))
print("Keys:", list(result.keys()))
# Print text fields
for k in ("summary", "platform", "n_atoms", "md_steps", "gpu"):
    if k in result:
        print(f"  {k}: {result[k]}")

# Show analysis if present
if "analysis" in result:
    a = result["analysis"]
    if isinstance(a, dict):
        for k2, v2 in list(a.items())[:10]:
            print(f"  analysis.{k2}: {v2}")
    else:
        print("  analysis:", str(a)[:500])
