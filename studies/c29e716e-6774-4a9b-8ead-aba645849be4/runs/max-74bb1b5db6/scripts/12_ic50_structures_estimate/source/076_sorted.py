
import json, glob, re

ws = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02'

# Build SMILES→affinity from existing result files
smi_to_aff = {}
for rf in sorted(glob.glob(f'{ws}/autodock-vina-results*.json')):
    with open(rf) as f:
        d = json.load(f)
    summ = d.get('summary', '')
    m = re.search(r'docked SMILES (.+?) into', summ)
    if m:
        smi_to_aff[m.group(1)] = d.get('best_affinity_kcal_mol')

# All compounds as flat (name, smiles) list
name_smi_all = []
for item in all_compounds:
    name_smi_all.append((item[0], item[1]))

# Match
docking_results = {}
for name, smi in name_smi_all:
    if smi in smi_to_aff:
        docking_results[name] = smi_to_aff[smi]

print(f"Matched {len(docking_results)}/{len(name_smi_all)}")
for n,v in sorted(docking_results.items()):
    print(f"  {n}: {v}")

remaining = [(n, s) for n, s in name_smi_all if n not in docking_results]
print(f"\nRemaining: {len(remaining)}")
for n, _ in remaining[:5]:
    print(f"  {n}")
