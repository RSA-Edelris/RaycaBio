
# Try MCUF651 with gpu=True to get a properly-matched GPU node
res = dispatch("aizynthfinder", inputs={
    "smiles": "CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1",
    "iteration_limit": 150,
    "time_limit": 150,
    "max_routes": 5,
    "min_routes": 3,
    "max_transforms": 6,
    "expansion_policy": "uspto",
    "filter_policy": "uspto",
}, gpu=True, timeout=300)

print(f"rc={res['rc']}  duration={res.get('duration_s','?')}s")
if res['rc'] == 0:
    out = res['output']
    print(f"is_solved={out.get('is_solved')}  n_routes={out.get('n_routes')}  top_score={out.get('top_score')}")
    print("Summary:", out.get('summary',''))
else:
    print("ERROR:", res.get('error',''), res.get('output_raw','')[:300])
