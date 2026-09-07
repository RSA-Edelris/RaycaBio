
# Print full dispatch result for diagnosis
name = "Compound_1_ent1"
print(f"Test docking {name} with relative paths...")
r = dispatch('gnina', {
    'proteinFile': '4CI2_receptor_for_docking.pdb',
    'ligandFile':  f'ligs2/{name}.sdf',
    'boxX': 85.06, 'boxY': 154.79, 'boxZ': 13.38,
    'width': 22.0, 'height': 22.0, 'depth': 22.0,
    'numModes': 5, 'cnnScoring': 'rescore', 'seed': 42
})
print(f"Full result: {r}")
