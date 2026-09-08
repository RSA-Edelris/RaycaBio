
# Remove the three unknown accessions: P49840 (GSK3A), Q96GD4 (AURKB), P04049 (RAF1)
clinical_accessions_v2 = [a for a in clinical_accessions
                          if a not in ("P49840", "Q96GD4", "P04049")]
print("Accessions to dock:", len(clinical_accessions_v2), clinical_accessions_v2)

result_clin2 = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "accessions":       clinical_accessions_v2,
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_clinical_panel",
})
print("rc:", result_clin2.get("returncode", result_clin2.get("rc", "?")))
print(result_clin2.get("stdout","")[-800:])
