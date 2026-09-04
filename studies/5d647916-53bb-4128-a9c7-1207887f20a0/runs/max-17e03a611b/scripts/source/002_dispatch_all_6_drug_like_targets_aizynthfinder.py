
# Dispatch all 6 drug-like targets to AiZynthFinder in parallel
smiles_targets = {
    "MCUF651": "CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1",
    "B54":     "O=C(Nc1nc(/C=C/c2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1",
    "A317":    "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1",
    "8008":    "CCOc1ccc(S(=O)(=O)Nc2ccc(Cl)cc2C#Cc2cnc(C(=O)O)cc2OC)c2ncccc12",
    "7977":    "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21",
    "7877":    "Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1",
}

handles = {}
for name, smi in smiles_targets.items():
    h = dispatch(
        "aizynthfinder",
        smiles=smi,
        iteration_limit=200,
        time_limit=180,
        max_routes=5,
        min_routes=3,
        max_transforms=7,
        expansion_policy="uspto",
        filter_policy="uspto",
    )
    handles[name] = h
    print(f"Dispatched {name}: handle={h}")
