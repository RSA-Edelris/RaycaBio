
# Save interaction data to JSON for reference
import json as json_mod

interactions_serial = {}
for lig, idata in interactions.items():
    interactions_serial[lig] = {
        'hbonds': {k: [[d, an] for d, an in v] for k, v in idata['hbonds'].items()},
        'hydrophobic': idata['hydrophobic'],
    }

with open(f"{ART}/interactions_best_poses.json", 'w') as fh:
    json_mod.dump(interactions_serial, fh, indent=2)

# Save full table to CSV
import csv
with open(f"{ART}/full_docking_gbsa_table.csv", 'w', newline='') as fh:
    writer = csv.DictWriter(fh, fieldnames=['mol_name','rank','pic50','affinity',
                                             'cnn_score','cnn_aff','vdw','elec',
                                             'polar','nonpolar','mmgbsa'])
    writer.writeheader()
    for r in full_table:
        writer.writerow({k: round(v,3) if isinstance(v, float) else v for k,v in r.items()})

print("Saved interactions_best_poses.json and full_docking_gbsa_table.csv")
print(f"full_table rows: {len(full_table)}")
