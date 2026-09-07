
import csv

with open(f"{ART}/full_docking_gbsa_table.csv", 'w', newline='') as fh:
    fieldnames = ['mol_name','rank','pic50','affinity','cnn_score','cnn_aff',
                  'vdw','elec','polar','nonpolar','gas','mmgbsa']
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    for r in full_table:
        writer.writerow({k: round(v,3) if isinstance(v, float) else v for k,v in r.items()})

print("Saved full_docking_gbsa_table.csv")
print("First 3 rows:")
for r in full_table[:3]:
    print(f"  {r}")
