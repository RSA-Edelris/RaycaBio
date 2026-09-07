
import json

print("easy-md take 2 — 3D SDF, small box (2.5 nm buf), 500 ps NPT CUDA A100...")
result = run_aidd_tool("easy-md", {
    "protein_file":        "receptor_pH74_noH.pdb",
    "ligand_file":         "EL2003A_pose2_3D.sdf",
    "platform_name":       "CUDA",
    "platform_precision":  "mixed",
    "md_steps":            250000,     # 500 ps at 2 fs/step
    "md_npt":              True,
    "md_pressure":         1.0,
    "md_save_interval":    5000,       # frame every 10 ps  → 50 frames
    "emin_steps":          10,
    "emin_target_temp":    300.0,
    "integrator_temperature": 300.0,
    "integrator_friction": 1.0,
    "integrator_timestep": 0.002,
    "solv_pH":             7.4,
    "solv_ionic_strength": 0.15,
    "solv_box_buffer":     2.5,    # default nm buffer → 7.9 nm box
    "solv_model":          "tip3p",
    "run_analysis":        True,
}, gpu=True)

print("rc:", result.get("rc"))
for k, v in result.items():
    if k in ("path_rewrites", "staged_from_workspace", "autonomy", "image_cache"):
        continue
    if isinstance(v, str) and len(v) > 400:
        print(f"  {k}: {v[:400]}...")
    elif isinstance(v, dict) and len(str(v)) > 400:
        print(f"  {k}: (dict, keys={list(v.keys())})")
    else:
        print(f"  {k}: {v}")

with open("easymd_result2.json", "w") as g:
    safe = {}
    for k, v in result.items():
        try: json.dumps(v); safe[k] = v
        except: safe[k] = str(v)
    json.dump(safe, g, indent=2)
print("\nSaved easymd_result2.json")
