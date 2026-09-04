
import json, time

smiles_map = {
    "MCUF651": "CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1",
    "A317":    "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1",
    "7977":    "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21",
}

aizyn_results = {}
for name, smi in smiles_map.items():
    print(f"\n=== AiZynthFinder: {name} ===")
    t0 = time.time()
    r = dispatch("aizynthfinder", {
        "smiles": smi,
        "iteration_limit": 200,
        "time_limit": 180,
        "max_routes": 10,
        "min_routes": 5,
        "max_transforms": 7,
        "expansion_policy": "uspto",
        "filter_policy": "uspto",
    })
    elapsed = round(time.time() - t0, 1)
    aizyn_results[name] = r
    print(f"  solved={r.get('is_solved')}, n_routes={r.get('n_routes')}, "
          f"n_solved={r.get('n_solved_routes')}, time={elapsed}s")
    print(f"  top_score={r.get('top_score')}")

# Save to disk
with open("aizyn_results.json", "w") as f:
    json.dump(aizyn_results, f, indent=2)
print("\nSaved aizyn_results.json")
