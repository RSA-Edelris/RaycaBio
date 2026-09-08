
import re, numpy as np
from rdkit.Chem import MolFromMolBlock, SDWriter

# Parse scores from raw SDF blocks
def parse_sdf_props(block):
    props = {}
    for m in re.finditer(r'> <(\S+)>\n(.*?)\n', block):
        try: props[m.group(1)] = float(m.group(2).strip())
        except ValueError: props[m.group(1)] = m.group(2).strip()
    return props

pose_data = [parse_sdf_props(b) for b in blocks[:5]]

print("=" * 72)
print(f"{'Pose':>4} {'Vina(kcal/mol)':>14} {'CNNscore':>9} {'CNNaffinity':>11} {'CNN_VS':>8}")
print("-" * 72)
for i, d in enumerate(pose_data):
    print(f"  {i+1:>2}  {d.get('minimizedAffinity',0):>14.4f}  "
          f"{d.get('CNNscore',0):>9.4f}  {d.get('CNNaffinity',0):>11.4f}  "
          f"{d.get('CNN_VS',0):>8.4f}")
print("=" * 72)

# Re-parse pose mols and write corrected SDFs with gnina scores attached
for i, (block, props) in enumerate(zip(blocks[:5], pose_data)):
    mol = MolFromMolBlock(block, removeHs=False, sanitize=True)
    if mol:
        mol.SetProp("_Name", f"EL2003A-A2U1_pose{i+1}")
        for k, v in props.items():
            mol.SetProp(k, str(v))
        pose_mols[i] = mol
        w = SDWriter(f"{WS}/pose_{i+1}.sdf")
        w.write(mol); w.close()

print("\nPose SDFs updated with gnina scores.")

# Pose 1 coordinates → verify ligand placement
p1_coords = np.array(pose_mols[0].GetConformer().GetPositions())
centroid  = p1_coords.mean(axis=0)
print(f"Pose 1 ligand centroid: {centroid.round(2)}")
print(f"LI8 box center:        [{cx:.2f} {cy:.2f} {cz:.2f}]")
print(f"Offset from box:       {(centroid - np.array([cx,cy,cz])).round(2)}")
