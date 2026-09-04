
result2 = run_aidd_tool("aizynthfinder", {
    "smiles": "O=C1CCNc2cc3c(cc2CN1CC1CC1)OCO3",
    "expansion_policy": "uspto",
    "stock": "zinc",
    "iteration_limit": 200
})
import json
print(json.dumps(result2, indent=2)[:8000])
