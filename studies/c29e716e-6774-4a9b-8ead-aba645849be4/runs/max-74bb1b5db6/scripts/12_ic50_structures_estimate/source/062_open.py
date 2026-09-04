
with open(pdb_clean_path) as f:
    pdb_clean_content = f.read()
with open(sdf_path_anchor) as f:
    sdf_anchor_content = f.read()

result_anchor = dispatch('gnina', {
    'proteinFile': 'target_clean.pdb',
    'ligandFile': 'anchor.sdf',
    'wholeProtein': True,
    'exhaustiveness': 8,
    'numModes': 9,
    'seed': 42
}, files={
    'proteinFile': pdb_clean_content,
    'ligandFile': sdf_anchor_content
})

print(f"best_affinity: {result_anchor.get('best_affinity_kcal_mol')}")
print(f"cnn_affinity:  {result_anchor.get('best_cnn_affinity')}")
print(f"num_poses:     {result_anchor.get('num_poses')}")
print(f"gpu_used:      {result_anchor.get('gpu_used')}")
print(result_anchor.get('summary','')[:400])
poses = result_anchor.get('poses', [])
if poses:
    print(f"Top pose: {poses[0]}")
