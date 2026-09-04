
# Check actual unique residue names in the receptor PDB
with open(RECEPTOR_PDB) as f:
    resnames = set()
    for line in f:
        if line.startswith('ATOM') or line.startswith('HETATM'):
            resnames.add(line[17:20].strip())
print("Residue names:", sorted(resnames))

# Also grep for HIE directly
import subprocess
r = subprocess.run(['grep', '-c', 'HIE', RECEPTOR_PDB], capture_output=True, text=True)
print("Lines with HIE:", r.stdout.strip())

# Check first few lines to see file format
with open(RECEPTOR_PDB) as f:
    for i, line in enumerate(f):
        if i < 5 or 'HIE' in line or 'HIS' in line:
            print(repr(line[:80]))
        if i > 10 and 'HIE' not in line and 'HIS' not in line:
            continue
        if i > 200:
            break
