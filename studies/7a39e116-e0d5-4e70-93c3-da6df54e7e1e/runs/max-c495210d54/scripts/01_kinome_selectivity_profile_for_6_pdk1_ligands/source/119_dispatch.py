
result_cmgc = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "kinase_families":  ["CMGC"],
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_CMGC",
})
print("CMGC rc:", result_cmgc.get("returncode", result_cmgc.get("rc", "?")))
print(result_cmgc.get("stdout","")[-500:])
