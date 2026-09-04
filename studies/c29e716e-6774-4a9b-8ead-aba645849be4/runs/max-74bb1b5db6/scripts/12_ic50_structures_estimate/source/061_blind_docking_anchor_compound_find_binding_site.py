
# Blind docking anchor compound to find binding site
with open(pdb_clean_path) as f:
    pdb_clean_content = f.read()
with open(sdf_path_anchor) as f:
    sdf_anchor_content = f.read()

result_anchor = dispatch('gnina', {
    'wholeProtein': True,
    'exhaustiveness': 8,
    'numModes': 9,
    'seed': 42
}, files={
    'proteinFile': pdb_clean_content,
    'ligandFile': sdf_anchor_content
})

print("gnina blind dock result:")
print(f"  best_affinity_kcal_mol: {result_anchor.get('best_affinity_kcal_mol')}")
print(f"  best_cnn_affinity:      {result_anchor.get('best_cnn_affinity')}")
print(f"  best_cnn_pose_score:    {result_anchor.get('best_cnn_pose_score')}")
print(f"  num_poses:              {result_anchor.get('num_poses')}")
print(f"  gpu_used:               {result_anchor.get('gpu_used')}")
print(result_anchor.get('summary','')[:400])
