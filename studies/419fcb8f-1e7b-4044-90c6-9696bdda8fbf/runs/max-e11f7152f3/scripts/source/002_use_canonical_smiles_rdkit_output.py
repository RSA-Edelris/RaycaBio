
from modulon.governance.toolkit import run_aidd_tool
import json

# Use canonical SMILES from RDKit output
result = run_aidd_tool("aizynthfinder", {
    "smiles": "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
    "expansion_policy": "uspto",
    "stock": "zinc",
    "iteration_limit": 200,
    "return_all_routes": True
})
print(json.dumps(result, indent=2)[:6000])
