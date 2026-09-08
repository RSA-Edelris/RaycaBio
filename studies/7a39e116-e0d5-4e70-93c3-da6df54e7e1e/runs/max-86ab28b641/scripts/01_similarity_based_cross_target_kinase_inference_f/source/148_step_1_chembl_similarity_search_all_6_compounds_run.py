
# Step 1: ChEMBL similarity search for all 6 compounds
# Run sequentially (tool dispatches to GPU, each call ~5-10s)
import json
WS = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

compounds = {
    "BX912":         "O=C(Nc1cccc(Nc2ncc(Br)c(NCCc3cnc[nH]3)n2)c1)N1CCCC1",
    "EL2003A":       "O=C(Nc1cccc(Nc2nc(NCCc3cnc[nH]3)c3nc[nH]c3n2)c1)N1CCCC1",
    "EL2003A-A2U1":  "Cc1ccc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)cc1NC(=O)N1CCCC1",
    "EL2003A-A4U1":  "O=C(Nc1cc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)ccc1C(F)(F)F)N1CCCC1",
    "EL5001A":       "O=C(NCCNc1ncc(Br)c(NCCc2c[nH]cn2)n1)N1CCCC1",
    "EL5003A":       "O=C(N[C@@H]1CC[C@@H](Nc2ncc(Br)c(NCCc3c[nH]cn3)n2)C1)N1CCCC1",
}

similarity_results = {}
for cname, smi in compounds.items():
    print(f"Searching ChEMBL for {cname} ...")
    r = run_aidd_tool("chembl", {
        "name": "",
        "smiles": smi,
        "chemblId": "",
        "searchBy": "SMILES",
        "maxResults": 50,
        "similarityThreshold": 0.4
    })
    n = r.get("num_results", 0)
    hits = r.get("results", [])
    similarity_results[cname] = hits
    print(f"  → {n} hits")
    if hits:
        print(f"     top hit: {hits[0].get('chembl_id','?')} Tc={hits[0].get('similarity',hits[0].get('tanimoto','?')):.3f}")

import pickle
with open(f"{WS}/chembl_similarity_hits.pkl","wb") as f:
    pickle.dump(similarity_results, f)
print("Saved similarity hits.")
