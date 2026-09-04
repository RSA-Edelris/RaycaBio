
# Remove long disordered C-term tail and N-term from missing residues
# Only model short loop 182-184 (3 residues)
del fixer.missingResidues[(0, 0)]    # GLY0/MET1 N-term: skip
del fixer.missingResidues[(0, 276)]  # 34-residue C-term tail: skip (too disordered)
# Keep (0, 180): ASP/PHE/GLY loop

fixer.findMissingAtoms()
print("Missing atoms:", {str(k): list(v.keys()) if hasattr(v, 'keys') else v for k,v in fixer.missingAtoms.items()})
print("Missing terminals:", fixer.missingTerminals)

# Add missing atoms (ASP240 sidechain CG/OD1/OD2) + model short loop
fixer.addMissingAtoms()
print("Missing atoms added.")

# Add hydrogens at pH 7.4
fixer.addMissingHydrogens(7.4)
print("Hydrogens added at pH 7.4.")

# Write prepared protein (without HETATM ligand FRJ - keep it for reference)
with open(PDB_FIXED, 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f, keepIds=True)
print(f"Written: {PDB_FIXED}")

import os
print(f"File size: {os.path.getsize(PDB_FIXED)} bytes")
