
import numpy as np

# Parse all poses from gnina output SDF
suppl = Chem.SDMolSupplier()
suppl.SetData(sdf_out, removeHs=False)

poses_data = []
for mol in suppl:
    if mol is None:
        continue
    conf = mol.GetConformer()
    coords = conf.GetPositions()
    centroid = coords.mean(axis=0)
    affinity = float(mol.GetProp('minimizedAffinity')) if mol.HasProp('minimizedAffinity') else None
    cnn_aff = float(mol.GetProp('CNNaffinity')) if mol.HasProp('CNNaffinity') else None
    cnn_score = float(mol.GetProp('CNNscore')) if mol.HasProp('CNNscore') else None
    poses_data.append({'centroid': centroid, 'affinity': affinity, 'cnn_affinity': cnn_aff, 'cnn_score': cnn_score})

print(f"Parsed {len(poses_data)} poses")
for i, p in enumerate(poses_data):
    print(f"  Pose {i+1}: affinity={p['affinity']:.3f}, CNN={p['cnn_affinity']:.3f}, score={p['cnn_score']:.3f}, centroid=({p['centroid'][0]:.1f},{p['centroid'][1]:.1f},{p['centroid'][2]:.1f})")

# Use top CNN-scoring pose centroid as box center
top_pose = sorted(poses_data, key=lambda x: x['cnn_score'] or 0, reverse=True)[0]
cx, cy, cz = top_pose['centroid']
print(f"\nBox center: boxX={cx:.2f}, boxY={cy:.2f}, boxZ={cz:.2f}")
print(f"Box size: 25 Å (covers full ligand + ~8 Å padding)")
