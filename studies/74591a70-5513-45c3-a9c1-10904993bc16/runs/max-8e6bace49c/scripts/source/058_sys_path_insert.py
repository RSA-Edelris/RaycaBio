
import sys, json
sys.path.insert(0, WORK)
from interaction_utils import parse_pdb_atoms, parse_sdf_atoms, get_contacts, summarise

# Load receptor once
rec = parse_pdb_atoms(RECEPTOR)
print(f"Receptor heavy atoms: {len(rec['coords'])}")

best_dir = f"{WORK}/best_poses"
names    = sorted([f.replace("_pose1.sdf","") for f in os.listdir(best_dir) if f.endswith("_pose1.sdf")])

all_contacts = {}
for name in names:
    sdf = f"{best_dir}/{name}_pose1.sdf"
    lig = parse_sdf_atoms(sdf)
    if len(lig['coords']) == 0:
        print(f"  WARN: {name} — no ligand atoms parsed")
        all_contacts[name] = []
        continue
    contacts = get_contacts(rec, lig['coords'], lig['elements'])
    # filter to unique (type,res) summary
    all_contacts[name] = contacts

# Save
with open(f"{WORK}/all_contacts.json", 'w') as f:
    json.dump(all_contacts, f, indent=2)

# Quick check on best ligand
best = "EDEL-CRBN-0005_ent"
s = summarise(all_contacts[best])
print(f"\n{best} interactions:")
for t, res in s.items():
    print(f"  {t:15s}: {', '.join(res[:10])}")
print(f"\nTotal ligands analysed: {len(all_contacts)}")
