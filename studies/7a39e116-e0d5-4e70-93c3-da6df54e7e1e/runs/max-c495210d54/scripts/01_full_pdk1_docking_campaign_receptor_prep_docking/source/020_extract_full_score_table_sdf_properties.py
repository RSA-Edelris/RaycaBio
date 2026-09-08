
# Extract full score table from SDF properties
print("=" * 70)
print(f"{'Pose':>4} {'Vina(kcal/mol)':>14} {'CNNscore':>9} {'CNNaff':>8} {'CNN_VS':>7} {'CNNaff_var':>11}")
print("-" * 70)

pose_scores = []
for i, mol in enumerate(pose_mols[:5]):
    d = mol.GetPropsAsDict()
    vina  = float(d.get('minimizedAffinity', 0))
    cnn_s = float(d.get('CNNscore', 0))
    cnn_a = float(d.get('CNNaffinity', 0))
    cnn_v = d.get('CNN_VS', '')
    cnn_var = float(d.get('CNNaffinity_variance', 0))
    pose_scores.append(dict(pose=i+1, vina=vina, cnn_score=cnn_s,
                            cnn_aff=cnn_a, cnn_vs=cnn_v, cnn_var=cnn_var))
    print(f"{i+1:>4} {vina:>14.3f} {cnn_s:>9.4f} {cnn_a:>8.3f} {str(cnn_v):>7} {cnn_var:>11.4f}")

print("=" * 70)
print(f"\nBest pose by Vina: pose {min(pose_scores, key=lambda x: x['vina'])['pose']}")
print(f"Best pose by CNN score: pose {max(pose_scores, key=lambda x: x['cnn_score'])['pose']}")
