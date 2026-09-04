
# Build SAR insight from top vs bottom analysis
import json, os, math
from rdkit import Chem
from rdkit.Chem import Descriptors

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
sdf_path = "/home/ubuntu/rayca-artifacts/fec3a540149a0d0fc51a148c/files/Sorted_Cedilla.sdf"

with open(os.path.join(wd, "docking_scores.json")) as f:
    scores = json.load(f)
scores.sort(key=lambda x: x['best'] if x['best'] else 0)

suppl = Chem.SDMolSupplier(sdf_path, removeHs=True, sanitize=True)
smi_map = {}
for m in suppl:
    if m:
        smi_map[m.GetProp('_Name')] = Chem.MolToSmiles(m)

# Check top 10 and bottom 10 for piperazine (N-methylpiperazine)
def has_piperazine(smi):
    return 'N1CCN(C)CC1' in smi or 'N5CCN(C)CC5' in smi

def has_free_piperazine(smi):
    return 'N5CCNCC5' in smi or 'N1CCNCC1' in smi

print("=== TOP 10 structural features ===")
for r in scores[:10]:
    smi = smi_map.get(r['name'],'')
    pip = has_piperazine(smi)
    print(f"  {r['name']:25s}  MW={r['mw']:6.1f}  pip={pip}  SMILES={smi[:70]}")

print("\n=== BOTTOM 10 ===")
for r in scores[-10:]:
    smi = smi_map.get(r['name'],'')
    pip = has_piperazine(smi)
    print(f"  {r['name']:25s}  MW={r['mw']:6.1f}  pip={pip}  SMILES={smi[:70]}")
