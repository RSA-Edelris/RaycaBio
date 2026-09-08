
# Protonate ligand at pH 7.4 using dimorphite-DL
# SMILES from earlier: Cc1ccc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)cc1NC(=O)N1CCCC1

lig_smiles = "Cc1ccc(Nc2nc(NCCc3c[nH]cn3)c3nc[nH]c3n2)cc1NC(=O)N1CCCC1"

result_prot = dispatch("protonation-state", {
    "inputType": "smiles",
    "smiles": lig_smiles,
    "pH": 7.4,
    "ph_range": 1.0,
    "precision": 1.0,
    "label_states": True
})

print("protonation-state rc:", result_prot.get("rc"))
print("summary:", result_prot.get("summary",""))
print("num_variants:", result_prot.get("num_variants"))
print("pH window:", result_prot.get("ph_min"), "–", result_prot.get("ph_max"))
for s in result_prot.get("protonated_smiles", []):
    print(" ", s)
