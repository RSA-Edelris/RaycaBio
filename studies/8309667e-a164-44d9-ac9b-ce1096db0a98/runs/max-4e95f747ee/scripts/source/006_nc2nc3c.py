
import json

smiles_map = {
    "MCUF651": "CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1",
    "A317":    "O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1",
    "7977":    "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21",
}

# Also probe key intermediates where AiZynthFinder only found one family
extra_smiles = {
    # MCUF651: probe the piperidine-3-carboxamide before N-alkylation, and the benzothiazolamine
    "MCUF651_int1": "O=C(Nc1nc2c(F)cc(F)cc2s1)[C@H]1CCCNC1",   # nipecotamide before N-alkylation
    "MCUF651_int2": "Nc1nc2c(F)cc(F)cc2s1",                      # 2-amino-5,6-difluorobenzothiazole
    # A317: probe 2-aminothiazole intermediate
    "A317_int1":    "Nc1nc([C@H]2CCCN2c2ccccn2)cs1",              # 2-aminothiazole with pyridyl-pyrrolidine
    # 7977: probe the uracil-azaindole intermediate before Suzuki/N-alkylation
    "7977_int1":    "Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)[nH]c2cnccc21",
}

rsgpt_results = {}
all_queries = {**smiles_map, **extra_smiles}

for name, smi in all_queries.items():
    print(f"\nRSGPT: {name}")
    r = dispatch("rsgpt", {"smiles": smi, "beam_size": 15, "max_length": 100})
    rsgpt_results[name] = r
    preds = r.get("predicted_reactions", r.get("reactants", []))
    print(f"  {len(preds)} predictions")
    for i, p in enumerate(preds[:5], 1):
        if isinstance(p, dict):
            print(f"  [{i}] {p}")
        else:
            print(f"  [{i}] {p}")

with open("rsgpt_results.json", "w") as f:
    json.dump(rsgpt_results, f, indent=2)
print("\nSaved rsgpt_results.json")
