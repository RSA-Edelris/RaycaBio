
# Test autodock-vina with one compound, ligandSmiles input
# Receptor as PDB file (tool likely converts internally since it outputs receptor_pdbqt)
test_result = dispatch('autodock-vina', {
    'receptorFile': 'protein.pdb',
    'ligandSmiles': 'Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C(C)C)CC3)cn1',  # EDS00444974
    'boxX': cx, 'boxY': cy, 'boxZ': cz,
    'width': 25, 'height': 25, 'depth': 25,
    'exhaustiveness': 8,
    'num_modes': 3,
    'seed': 42
}, files={'protein.pdb': pdb_clean_content})

print(f"best_affinity: {test_result.get('best_affinity_kcal_mol')}")
print(f"num_poses:     {test_result.get('num_poses')}")
print(f"affinities:    {test_result.get('affinities_kcal_mol')}")
print(test_result.get('summary','')[:400])
