
import subprocess, os

# Rebuild correct index files for all 4 compounds
# Groups: 1=Protein, 13=LIG, 14=Cl-, 15=Water
# Protein_LIG = 1|13 (gets group 18); Water_and_ions = 15|14 (gets group 19)

for cid in COMPOUNDS:
    d = f'{WD}/md_{cid}'
    r = subprocess.run(
        ['gmx', 'make_ndx', '-f', f'{d}/complex.gro', '-o', f'{d}/index.ndx'],
        input='1 | 13\nname 18 Protein_LIG\n15 | 14\nname 19 Water_and_ions\nq\n',
        capture_output=True, text=True, env=env
    )
    # Verify groups exist in index
    r2 = subprocess.run(['grep', '-c', 'Protein_LIG\|Water_and_ions', f'{d}/index.ndx'],
                        capture_output=True, text=True)
    hits = r2.stdout.strip()
    print(f"{cid}: index rebuilt, group matches={hits}")
    if int(hits) < 2:
        print("  WARNING:", r.stderr[-300:])

print("\nAll index files rebuilt.")
