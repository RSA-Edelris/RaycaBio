
import gzip
from rdkit import Chem

# ── Inspect r_gnina result dict ───────────────────────────────────────────────
print("r_gnina keys:", list(r_gnina.keys()))
for k, v in r_gnina.items():
    if k not in ('poses', 'raw'):
        print(f"  {k}: {v}")

# ── Parse gnina_docked.sdf.gz ─────────────────────────────────────────────────
gz_path = 'gnina_docked.sdf.gz'
with gzip.open(gz_path, 'rt') as fh:
    sdf_text = fh.read()

print(f"\nDocked SDF length: {len(sdf_text):,} chars")

# Parse with RDKit
from rdkit.Chem import SDMolSupplier
import io
suppl = SDMolSupplier()
suppl.SetData(sdf_text, removeHs=False)
poses = []
for mol in suppl:
    if mol is None:
        continue
    props = {k: mol.GetProp(k) for k in mol.GetPropNames()}
    poses.append({'mol': mol, 'props': props})

print(f"Poses found: {len(poses)}")
if poses:
    print(f"  Properties on first pose: {list(poses[0]['props'].keys())}")
    for i, p in enumerate(poses):
        aff   = p['props'].get('minimizedAffinity', p['props'].get('affinity', '?'))
        cnn_a = p['props'].get('CNNaffinity', '?')
        cnn_p = p['props'].get('CNNscore', p['props'].get('CNNpose', '?'))
        print(f"  Pose {i+1}: vina={aff}  cnn_aff={cnn_a}  cnn_pose={cnn_p}")
