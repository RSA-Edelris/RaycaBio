
import json

# Save MCUF651 result from previous call (loaded from the auto-saved file)
with open("aizynthfinder-results.json") as f:
    mcuf651_res = json.load(f)

all_results = {"MCUF651": mcuf651_res}

remaining = {
    "B54":  "O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1",
    "A317": "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1",
    "8008": "CCOc1ccc(S(=O)(=O)Nc2ccc(Cl)cc2C#Cc2cnc(C(=O)O)cc2OC)c2ncccc12",
    "7977": "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21",
    "7877": "Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1",
}

for name, smi in remaining.items():
    print(f"Running {name} ...")
    res = dispatch("aizynthfinder", inputs={
        "smiles": smi,
        "iteration_limit": 150,
        "time_limit": 150,
        "max_routes": 5,
        "min_routes": 3,
        "max_transforms": 7,
        "expansion_policy": "uspto",
        "filter_policy": "uspto",
    }, gpu=True, timeout=300)
    all_results[name] = res
    solved = res.get("output", {}).get("is_solved", "?")
    n = res.get("output", {}).get("n_routes", "?")
    score = res.get("output", {}).get("top_score", "?")
    print(f"  rc={res['rc']}  solved={solved}  n_routes={n}  top_score={score}")

with open("all_aiz_results.json", "w") as f:
    json.dump(all_results, f)
print("\nAll done.")
