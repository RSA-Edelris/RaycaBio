
import json

# Retry B54
print("Retrying B54...")
res_b54 = dispatch("aizynthfinder", inputs={
    "smiles": "O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1",
    "iteration_limit": 150,
    "time_limit": 150,
    "max_routes": 5,
    "min_routes": 3,
    "max_transforms": 7,
    "expansion_policy": "uspto",
    "filter_policy": "uspto",
}, gpu=True, timeout=300)
print(f"rc={res_b54['rc']}  solved={res_b54.get('output',{}).get('is_solved')}  n_routes={res_b54.get('output',{}).get('n_routes')}")
all_results["B54"] = res_b54
with open("all_aiz_results.json", "w") as f:
    json.dump(all_results, f)
print("Saved.")
