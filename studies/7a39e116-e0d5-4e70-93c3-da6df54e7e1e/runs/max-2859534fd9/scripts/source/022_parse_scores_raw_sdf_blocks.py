
import re
from rdkit.Chem import MolFromMolBlock, SDWriter, Chem
import numpy as np

# Parse scores from raw SDF blocks
def parse_sdf_props(block):
    props = {}
    for m in re.finditer(r'> <(\S+)>\n(.*?)\n', block):
        key, val = m.group(1), m.group(2).strip()
        try:
            props[key] = float(val)
        except ValueError:
            props[key] = val
    return props

pose_data = []
for i, block in enumerate(blocks[:5]):
    props = parse_sdf_props(block)
    pose_data.append(props)

print("=" * 72)
print(f"{'Pose':>4} {'Vina(kcal/mol)':>14} {'CNNscore':>9} {'CNNaffinity':>11} {'CNN_VS':>8} {'Var':>7}")
print("-" * 72)
for i, d in enumerate(pose_data):
    print(f"  {i+1:>2}  {d.get('minimizedAffinity',0):>14.4f}  "
          f"{d.get('CNNscore',0):>9.4f}  {d.get('CNNaffinity',0):>11.4f}  "
          f"{d.get('CNN_VS',0):>8.4f}  {d.get('CNNaffinity_variance',0):>7.4f}")
print("=" * 72)

# Re-write pose SDFs with correct properties from raw parse
for i, (block, props) in enumerate(zip(blocks[:5], pose_data)):
    mol = MolFromMolBlock(block, removeHs=False, sanitize=True)
    if mol:
        mol.SetProp("_Name", f"EL2003A-A2U1_pose{i+1}")
        for k, v in props.items():
            mol.SetProp(k, str(v))
        pose_mols[i] = mol

# Rewrite individual SDFs with correct properties
for i, mol in enumerate(pose_mols[:5]):
    path = f"{WS}/pose_{i+1}.sdf"
    w = SDWriter(path)
    w.write(mol)
    w.close()
print("\nPose SDF files updated with correct scores.")

# Get pose 1 coordinates for interaction analysis
conf = pose_mols[0].GetConformer()
lig_coords = np.array(conf.GetPositions())
print(f"\nPose 1 ligand centroid: {lig_coords.mean(axis=0).round(2)}")
print(f"Box center was: ({cx:.2f}, {cy:.2f}, {cz:.2f}) — offset: {(lig_coords.mean(axis=0) - np.array([cx,cy,cz])).round(2)}")
