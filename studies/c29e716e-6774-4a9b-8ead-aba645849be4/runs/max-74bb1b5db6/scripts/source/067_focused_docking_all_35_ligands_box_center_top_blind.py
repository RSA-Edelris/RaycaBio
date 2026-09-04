
# Focused docking: all 35 ligands, box center from top blind-dock pose
with open(pdb_clean_path) as f:
    pdb_clean_content = f.read()
with open(combined_sdf_path) as f:
    combined_sdf_content = f.read()

result_all = dispatch('gnina', {
    'proteinFile': 'protein.pdb',
    'ligandFile': 'all_35.sdf',
    'boxX': cx,
    'boxY': cy,
    'boxZ': cz,
    'width': 25,
    'height': 25,
    'depth': 25,
    'exhaustiveness': 16,
    'numModes': 5,
    'seed': 42
}, files={
    'protein.pdb': pdb_clean_content,
    'all_35.sdf': combined_sdf_content
})

print(f"rc: {result_all.get('_rc', 'n/a')}")
print(f"best_affinity: {result_all.get('best_affinity_kcal_mol')}")
print(f"num_poses: {result_all.get('num_poses')}")
print(result_all.get('summary','')[:300])
