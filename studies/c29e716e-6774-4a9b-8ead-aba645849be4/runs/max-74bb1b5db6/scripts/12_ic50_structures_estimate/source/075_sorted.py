
import json, glob, re

ws = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02'

# Build SMILES→result map from existing files
smi_to_result = {}
for rf in sorted(glob.glob(f'{ws}/autodock-vina-results*.json')):
    with open(rf) as f:
        d = json.load(f)
    summ = d.get('summary', '')
    # Extract SMILES from summary: "docked SMILES <smi> into"
    m = re.search(r'docked SMILES (.+?) into', summ)
    smi = m.group(1) if m else None
    if smi:
        smi_to_result[smi] = {'affinity': d.get('best_affinity_kcal_mol'), 'affinities': d.get('affinities_kcal_mol')}

print(f"Mapped {len(smi_to_result)} results")

# Match to compound names
docking_results = {}
all_smi_dict = {s: n for n,s,*_ in all_compounds}
proposed_smi = [s for _,s in [(n,s) for n,s in [(p[0],p[1]) for p in [(n,s) for n,s in [(n,s,None) for n,s in [(t[0],t[1]) for t in [(n,s) for n,s in [(i,j) for i,j in proposed]]]]]]]]

# Flat: all compound (name, smiles)
name_smi_list = [(n, s) for n,s,*_ in all_compounds]

for name, smi in name_smi_list:
    if smi in smi_to_result:
        docking_results[name] = {'name': name, 'smiles': smi, **smi_to_result[smi]}
        print(f"  MATCHED {name}: {docking_results[name]['affinity']}")

print(f"\nMatched {len(docking_results)}/{len(name_smi_list)} compounds so far")
remaining = [(n, s) for n, s, *_ in all_compounds if n not in docking_results]
print(f"Remaining: {len(remaining)} compounds")
for n, s in remaining[:5]:
    print(f"  {n}")
