
from modulon.governance.toolkit import run_aidd_tool
import json

result = run_aidd_tool("rdkit", {
    "smiles": ["O=C1N(CC2CC2)Cc(cc2OCOc2c2)c2NCC1"],
    "descriptors": ["MolWt", "MolLogP", "NumHDonors", "NumHAcceptors", "NumRotatableBonds", "RingCount", "TPSA"]
})
print(json.dumps(result, indent=2))
