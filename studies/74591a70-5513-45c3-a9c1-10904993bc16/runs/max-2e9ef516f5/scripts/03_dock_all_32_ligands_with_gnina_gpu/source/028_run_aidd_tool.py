
from modulon.governance.toolkit import run_aidd_tool

result = run_aidd_tool(
    tool_id="gnina",
    inputs={
        "proteinFile": "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e/4CI2_receptor_for_docking.pdb",
        "ligandFile": "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e/ligands/lig16.sdf",
        "boxX": 84.800,
        "boxY": 154.937,
        "boxZ": 13.242,
        "width": 24,
        "height": 24,
        "depth": 24,
        "numModes": 5,
        "cnnScoring": "rescore",
        "seed": 0
    }
)

print(result)
