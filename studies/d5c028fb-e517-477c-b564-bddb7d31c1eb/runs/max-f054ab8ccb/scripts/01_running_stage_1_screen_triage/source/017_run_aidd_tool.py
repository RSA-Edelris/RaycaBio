
from modulon.governance.toolkit import run_aidd_tool

result = run_aidd_tool(
    tool_id="gnina",
    inputs={
        "proteinFile": "receptor_stripped.pdb",
        "ligandFile":  "batch_actives.sdf",
        "boxX":  30.57, "boxY":  5.37, "boxZ": -25.80,
        "width":  24.0, "height": 20.0, "depth":  20.0,
        "exhaustiveness": 8, "numModes": 9,
        "cnnScoring": "rescore", "seed": 42
    }
)
print(result['output']['summary'])
print("rc:", result['rc'], "  gpu:", result['gpu'], "  duration:", result['duration_s'])
if 'poses' in result['output']:
    for p in result['output']['poses'][:5]:
        print(f"  rank {p['rank']}: affinity={p['affinity']} kcal/mol  cnn_pose={p['cnn_pose_score']:.4f}  cnn_aff={p['cnn_affinity']:.3f}")
