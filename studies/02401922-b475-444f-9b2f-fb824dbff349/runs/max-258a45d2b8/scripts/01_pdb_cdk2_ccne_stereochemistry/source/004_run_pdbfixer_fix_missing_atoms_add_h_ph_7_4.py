
# Run PDBFixer: fix missing atoms, add H at pH 7.4
fixer = PDBFixer(filename='receptor_raw.pdb')

# Find and add missing residues/atoms (do NOT add missing terminal segments)
fixer.findMissingResidues()
# Only fill gaps in the middle, not termini
chains_info = list(fixer.topology.chains())
fixer.missingResidues = {k: v for k,v in fixer.missingResidues.items()
                         if k[1] not in (0, len(list(fixer.topology.chains()))-1)}

fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()
fixer.removeHeterogens(keepWater=True)   # keep the 9 waters we already filtered in

fixer.findMissingAtoms()
fixer.addMissingAtoms()

# Add H at pH 7.4 — this sets protonation states (HIS, ASP, GLU, LYS, etc.)
fixer.addMissingHydrogens(7.4)

with open('receptor_prepared.pdb','w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

print("Receptor prepared: receptor_prepared.pdb")

# Count atoms
atom_count = sum(1 for l in open('receptor_prepared.pdb') if l.startswith(('ATOM','HETATM')))
print(f"Atoms in prepared receptor: {atom_count}")
