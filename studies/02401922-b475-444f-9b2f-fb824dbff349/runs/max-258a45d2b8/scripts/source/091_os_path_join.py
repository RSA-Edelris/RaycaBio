
import os, re, json
from rdkit import Chem
from rdkit.Chem import Descriptors

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
results_dir = os.path.join(wd, "docking_results")
ligands_dir = os.path.join(wd, "ligands_3d")
sdf_path = "/home/ubuntu/rayca-artifacts/fec3a540149a0d0fc51a148c/files/Sorted_Cedilla.sdf"

# Name mapping: lig index -> compound name + MW + SMILES
suppl = Chem.SDMolSupplier(sdf_path, removeHs=True, sanitize=True)
raw = [(m.GetProp('_Name'), Descriptors.MolWt(m), Chem.MolToSmiles(m), Chem.GetFormalCharge(m))
       for m in suppl if m]
idx_to_info = {i+1: raw[i] for i in range(len(raw))}

def parse_scores(path):
    scores = []
    with open(path) as f:
        for line in f:
            m = re.match(r'REMARK VINA RESULT:\s+([-\d.]+)', line)
            if m:
                scores.append(float(m.group(1)))
    return scores

results = []
for n in range(1, 85):
    out_f = os.path.join(results_dir, f"lig{n}_out.pdbqt")
    name, mw, smi, q = idx_to_info.get(n, ('?', 0, '', 0))
    scores = parse_scores(out_f) if os.path.exists(out_f) else []
    best = scores[0] if scores else None
    results.append({'lig': n, 'name': name, 'mw': round(mw,1), 'q_neutral': q,
                    'best': best, 'all_scores': scores})

# Sort by best score (most negative = best)
results.sort(key=lambda x: x['best'] if x['best'] else 0)

# Save
with open(os.path.join(wd, "docking_scores.json"), 'w') as f:
    json.dump(results, f, indent=2)

# Print full ranking
print(f"{'Rank':>4}  {'Compound':35}  {'MW':>7}  {'q':>3}  {'Pose1':>8}  {'Pose2':>8}  {'Pose3':>8}  {'Pose4':>8}  {'Pose5':>8}")
print("-"*105)
for i, r in enumerate(results):
    p = r['all_scores']
    def ps(j): return f"{p[j]:.3f}" if len(p)>j else ''
    print(f"  {i+1:2d}  {r['name']:35}  {r['mw']:>7.1f}  {r['q_neutral']:>3}  {ps(0):>8}  {ps(1):>8}  {ps(2):>8}  {ps(3):>8}  {ps(4):>8}")

# CTX reference
print("-"*105)
print(f"  --  {'CTX crystal (score_only, ref)':35}  {'523.3':>7}  {'+1':>3}  {-14.090:>8.3f}")
print(f"  --  {'CTX-1017233 (exh=32, prior)':35}  {'523.3':>7}  {'+1':>3}  {-12.614:>8.3f}")
