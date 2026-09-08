
# AGC only first — PDK1's home family, fastest to interpret
result_agc = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "kinase_families":  ["AGC"],
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_ligands_AGC",
})
print("AGC  rc =", result_agc.get("rc"))
print("     n  =", result_agc.get("n_predictions"))
print("     csv=", result_agc.get("results_csv"))
print("     summary:", result_agc.get("summary","")[:400])
