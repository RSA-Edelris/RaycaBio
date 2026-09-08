
# Test: can we pass kinase_names instead of kinase_families?
# Try a small focused call: just CDK2 + GSK3B (most clinically relevant CMGC kinases)
result_cdk2 = dispatch("kinasedocker2", {
    "smiles":         smiles_list,
    "kinase_names":   ["CDK2", "GSK3B", "CDK4", "CDK1", "CDK6", "MAPK3", "MAPK1"],
    "docking_engine": "vina",
    "scoring_function": "DNN",
    "run_name":       "PDK1_CMGC_core",
})
print("rc:", result_cdk2.get("returncode", result_cdk2.get("rc", "?")))
print(result_cdk2.get("stdout","")[-800:])
