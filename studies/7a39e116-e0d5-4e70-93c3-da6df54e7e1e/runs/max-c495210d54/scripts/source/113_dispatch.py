
result = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "kinase_families":  ["AGC","CAMK","CK1","CMGC","Other","STE","TK","TKL"],
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_ligands_kinome_screen",
})

print("rc =", result.get("rc"))
print("n_predictions:", result.get("n_predictions"))
print("summary:", result.get("summary","")[:800])
print("results_csv:", result.get("results_csv"))
