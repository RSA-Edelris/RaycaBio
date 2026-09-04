
import os, re

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
results_dir = os.path.join(wd, "docking_results")
ligands_dir = os.path.join(wd, "ligands_3d")
sdf_path = "/home/ubuntu/rayca-artifacts/fec3a540149a0d0fc51a148c/files/Sorted_Cedilla.sdf"

# Rebuild name -> lig index mapping from the protonated SDF order
from rdkit import Chem
suppl = Chem.SDMolSupplier(sdf_path, removeHs=True, sanitize=True)
names = []
for m in suppl:
    if m:
        names.append(m.GetProp('_Name') if m.HasProp('_Name') else 'unk')

# lig1 = names[0], lig2 = names[1], etc.
idx_to_name = {i+1: names[i] for i in range(len(names))}

def parse_scores(path):
    scores = []
    with open(path) as f:
        for line in f:
            m = re.match(r'REMARK VINA RESULT:\s+([-\d.]+)', line)
            if m:
                scores.append(float(m.group(1)))
    return scores

# Collect all available results
results = []
for n in range(1, 85):
    out_f = os.path.join(results_dir, f"lig{n}_out.pdbqt")
    if os.path.exists(out_f):
        scores = parse_scores(out_f)
        best = scores[0] if scores else None
        results.append({'lig': n, 'name': idx_to_name.get(n,'?'), 'best': best, 'all': scores})

# Sort by best score
results.sort(key=lambda x: x['best'] if x['best'] is not None else 0)
print(f"Results available: {len(results)}/84")
print(f"\n{'Rank':>4}  {'Compound':35}  {'Best (kcal/mol)':>16}  {'Pose2':>8}  {'Pose3':>8}")
print("-"*80)
for i, r in enumerate(results[:20]):
    p = r['all']
    print(f"  {i+1:2d}  {r['name']:35}  {r['best']:>16.3f}  {p[1] if len(p)>1 else '':>8}  {p[2] if len(p)>2 else '':>8}")

# CTX reference from prior session
print(f"\n  --  {'CTX crystal (reference)':35}  {-14.09:>16.3f}  (score_only, prior session)")
print(f"  --  {'CTX-1017233 (prior docked)':35}  {-12.614:>16.3f}  (prior session exhaustiveness 32)")
