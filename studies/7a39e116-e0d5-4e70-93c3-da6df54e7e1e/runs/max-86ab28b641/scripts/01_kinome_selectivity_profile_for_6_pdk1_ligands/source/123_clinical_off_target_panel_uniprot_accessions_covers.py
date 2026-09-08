
# Clinical off-target panel — UniProt accessions
# Covers CMGC (CDK, GSK3, MAPK), TK, CAMK, Other, STE, TKL, CK1
clinical_accessions = [
    # CMGC — CDK/GSK3/MAPK
    "P24941",  # CDK2
    "P06493",  # CDK1
    "P11802",  # CDK4
    "Q00534",  # CDK6
    "P49841",  # GSK3B
    "P49840",  # GSK3A
    "P28482",  # MAPK1  (ERK2)
    "P27361",  # MAPK3  (ERK1)
    "Q16539",  # MAPK14 (p38α)
    "P45983",  # MAPK8  (JNK1)
    # TK — receptor & non-receptor
    "P00533",  # EGFR
    "P00519",  # ABL1
    "P35968",  # KDR (VEGFR2)
    "P11362",  # FGFR1
    "P08581",  # MET
    "P12931",  # SRC
    "Q06187",  # BTK
    "O60674",  # JAK2
    "P36888",  # FLT3
    # CAMK — checkpoint & cardiac
    "O14757",  # CHEK1
    "O96017",  # CHEK2
    # Other — mitotic
    "O14965",  # AURKA
    "Q96GD4",  # AURKB
    "P53350",  # PLK1
    # STE — MEK
    "Q02750",  # MAP2K1 (MEK1)
    # TKL — RAF
    "P15056",  # BRAF
    "P04049",  # RAF1
    # CK1
    "P48730",  # CSNK1D
]

result_clin = dispatch("kinasedocker2", {
    "smiles":           smiles_list,
    "accessions":       clinical_accessions,
    "docking_engine":   "vina",
    "scoring_function": "DNN",
    "run_name":         "PDK1_clinical_panel",
})
print("rc:", result_clin.get("returncode", result_clin.get("rc", "?")))
print(result_clin.get("stdout","")[-1000:])
