
from modulon.governance.toolkit import run_aidd_tool

result = run_aidd_tool(
    tool_id="gnina",
    inputs={
        "proteinFile": "batch_actives.sdf",   # NOTE: should be receptor pdb
        "ligandFile":  "batch_actives.sdf",
        "boxX":  30.57, "boxY":  5.37, "boxZ": -25.80,
        "width":  24.0, "height": 20.0, "depth":  20.0,
        "exhaustiveness": 8, "numModes": 9,
        "cnnScoring": "rescore", "seed": 42
    }
)
print(result)
