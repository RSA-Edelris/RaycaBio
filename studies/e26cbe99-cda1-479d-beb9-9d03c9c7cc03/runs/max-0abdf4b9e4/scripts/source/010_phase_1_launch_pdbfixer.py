
# ── Phase 1: launch pdbfixer ──────────────────────────────────────────────────
print("Dispatching pdbfixer (pH 7.4, missing atoms+H, loop rebuild) ...")
pdbfixer_result = dispatch('pdbfixer', {
    'pdbFile':                   pdb_path,          # PB-20260903-4CI2_raw.pdb
    'pH':                        7.4,
    'addMissingResidues':        True,
    'addMissingAtoms':           True,
    'addMissingHydrogens':       True,
    'removeHeterogens':          True,
    'replaceNonstandardResidues': True,
    'addWater':                  False,
    'addMembrane':               False,
}, gpu=True)

print("pdbfixer rc:", pdbfixer_result.get('rc'))
print("Summary:", pdbfixer_result.get('summary',''))
print("Missing residues added:", pdbfixer_result.get('missing_residues_added'))
print("Missing atoms added:",    pdbfixer_result.get('missing_atoms_added'))
print("n_atoms:", pdbfixer_result.get('n_atoms'))
print("Structure file:", pdbfixer_result.get('structure',''))
