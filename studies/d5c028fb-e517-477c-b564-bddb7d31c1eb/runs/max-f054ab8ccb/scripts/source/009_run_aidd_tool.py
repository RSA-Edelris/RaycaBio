
from modulon.governance.toolkit import run_aidd_tool

result = run_aidd_tool(
    tool_id="gnina",
    inputs={
        "proteinFile": "receptor_stripped.pdb",
        "ligandFile":  "ligands_3d.sdf",
        "boxX":  30.57,
        "boxY":   5.37,
        "boxZ": -25.80,
        "width":  24.0,
        "height": 20.0,
        "depth":  20.0,
        "exhaustiveness": 8,
        "numModes": 9,
        "cnnScoring": "rescore",
        "seed": 42
    }
)

print("mode:         ", result.get("mode"))
print("gpu_used:     ", result.get("gpu_used"))
print("num_poses:    ", result.get("num_poses"))
print("best_affinity:", result.get("best_affinity_kcal_mol"))
print("best_cnn_aff: ", result.get("best_cnn_affinity"))
print("output_file:  ", result.get("output_file"))
print()

# Show per-compound best scores
poses = result.get("poses", [])
print(f"Total pose records: {len(poses)}")

# Group by compound name, keep best (lowest Vina affinity)
best = {}
for p in poses:
    name = p.get("name","?")
    aff  = p.get("affinity", 0)
    cnn  = p.get("cnn_affinity", 0)
    pose = p.get("cnn_pose_score", 0)
    if name not in best or aff < best[name][0]:
        best[name] = (aff, cnn, pose)

print(f"\nUnique compounds docked: {len(best)}")
for nm, (aff, cnn, ps) in sorted(best.items(), key=lambda x: x[1][0]):
    print(f"  {nm:12s}  Vina={aff:6.2f}  CNN_aff={cnn:5.2f}  CNN_pose={ps:.3f}")
