
import os, json

print("Dispatching openfe complexMD — NAGL charges (fast GNN), 500 ps NPT...")

result = run_aidd_tool("openfe", {
    "simulationType":   "complexMD",
    "proteinPDB":       "receptor_pH74_noH.pdb",
    "ligandFile":       "all_poses/EL2003A_pose2.sdf",
    "chargeMethod":     "nagl",
    "nvtLength":        50,    # 50 ps NVT warm-up
    "equilLength":      100,   # 100 ps NPT equilibration
    "prodLength":       500,   # 500 ps production (25 frames at 20 ps)
    "protocolRepeats":  1,
}, gpu=True)

print("rc:", result.get("rc"))
# Print all keys and their values/types
for k, v in result.items():
    if k in ("dg_per_frame",):
        continue
    if isinstance(v, str) and len(v) > 300:
        print(f"  {k}: {v[:300]}...")
    else:
        print(f"  {k}: {v}")

# Save full result for inspection
with open("openfe_result.json", "w") as f:
    # Filter non-serializable
    safe = {}
    for k, v in result.items():
        try:
            json.dumps(v)
            safe[k] = v
        except:
            safe[k] = str(v)
    json.dump(safe, f, indent=2)
print("\nFull result saved to openfe_result.json")
