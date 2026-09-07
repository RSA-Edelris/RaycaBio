
# Fix: pass absolute path to pdbfixer
result_fix = dispatch("pdbfixer", {
    "pdbFile": "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/1Z5M.pdb",
    "pH": 7.4,
    "addMissingResidues": True,
    "addMissingAtoms": True,
    "addMissingHydrogens": True,
    "replaceNonstandardResidues": True,
    "removeHeterogens": True,
    "addWater": False
}, gpu=True)

print("pdbfixer rc:", result_fix.get("rc"))
print("summary:", result_fix.get("summary",""))
print("missing_residues_added:", result_fix.get("missing_residues_added"))
print("missing_atoms_added:", result_fix.get("missing_atoms_added"))
print("nonstandard_replaced:", result_fix.get("nonstandard_residues_replaced"))
print("n_atoms:", result_fix.get("n_atoms"))
print("structure:", result_fix.get("structure",""))
