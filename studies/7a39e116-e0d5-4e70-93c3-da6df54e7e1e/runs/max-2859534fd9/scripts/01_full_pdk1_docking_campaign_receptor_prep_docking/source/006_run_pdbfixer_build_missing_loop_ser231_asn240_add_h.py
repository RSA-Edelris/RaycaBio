
# Run pdbfixer: build missing loop (SER231-ASN240), add H at pH 7.4,
# remove all heterogens (LI8, GOL, SO4, CL, SEP, waters) → clean receptor

result_fix = dispatch("pdbfixer", {
    "pdbFile": "1Z5M.pdb",
    "pH": 7.4,
    "addMissingResidues": True,
    "addMissingAtoms": True,
    "addMissingHydrogens": True,
    "replaceNonstandardResidues": True,   # SEP → SER
    "removeHeterogens": True,             # strip LI8, GOL, SO4, CL, waters
    "addWater": False
}, gpu=True)

print("pdbfixer rc:", result_fix.get("rc"))
print("summary:", result_fix.get("summary",""))
print("missing_residues_added:", result_fix.get("missing_residues_added"))
print("missing_atoms_added:", result_fix.get("missing_atoms_added"))
print("nonstandard_replaced:", result_fix.get("nonstandard_residues_replaced"))
print("n_atoms:", result_fix.get("n_atoms"))
print("n_chains:", result_fix.get("n_chains"))
print("output file:", result_fix.get("structure",""))
