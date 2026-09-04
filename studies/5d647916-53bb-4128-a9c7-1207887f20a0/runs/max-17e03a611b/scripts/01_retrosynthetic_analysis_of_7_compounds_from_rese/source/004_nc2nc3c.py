
import json

smiles_targets = {
    "MCUF651": "CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1",
    "B54":     "O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1",
    "A317":    "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1",
}

aiz_results = {}
for name, smi in smiles_targets.items():
    print(f"Running AiZynthFinder on {name} ...")
    res = dispatch("aizynthfinder", inputs={
        "smiles": smi,
        "iteration_limit": 200,
        "time_limit": 180,
        "max_routes": 5,
        "min_routes": 3,
        "max_transforms": 7,
        "expansion_policy": "uspto",
        "filter_policy": "uspto",
    }, gpu=False)
    aiz_results[name] = res
    solved = res.get("output", {}).get("is_solved", "?")
    n_routes = res.get("output", {}).get("n_routes", "?")
    print(f"  -> rc={res['rc']}  is_solved={solved}  n_routes={n_routes}")

with open("aiz_results_batch1.json", "w") as f:
    json.dump(aiz_results, f)
print("Batch 1 saved.")
