
from modulon.governance.toolkit import run_aidd_tool
import json

b54_canon = "O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1"

res_b54 = run_aidd_tool(
    tool_id="aizynthfinder",
    inputs={
        "smiles": b54_canon,
        "iteration_limit": 150,
        "time_limit": 150,
        "max_routes": 5,
        "min_routes": 3,
        "max_transforms": 7,
        "expansion_policy": "uspto",
        "filter_policy": "uspto",
    },
    gpu=True,
    timeout=300
)

print(f"rc={res_b54.get('rc')}")
print(f"error={res_b54.get('error')}")
print(f"duration_s={res_b54.get('duration_s')}")
if res_b54.get('output_files'):
    print(f"output_files={list(res_b54['output_files'].keys())}")
