
# Batch 2: CMGC core — CDK1/4/6, ERK1/2, p38, JNK1
batch2 = ["P06493","P11802","Q00534","P28482","P27361","Q16539","P45983"]
r2 = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "accessions":       batch2,
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_batch2",
})
print("Batch2 rc:", r2.get("returncode", r2.get("rc","?")))
print(r2.get("stdout","")[-300:])
