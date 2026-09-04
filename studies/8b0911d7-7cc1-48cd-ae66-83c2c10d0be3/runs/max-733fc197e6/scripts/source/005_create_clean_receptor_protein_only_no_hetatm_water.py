
# Create clean receptor (protein only, no HETATM/water) for fpocket and docking
RECEPTOR_PDB = os.path.join(WORKDIR, '9C56_receptor.pdb')

with open(PDB_FIXED) as fin, open(RECEPTOR_PDB, 'w') as fout:
    for line in fin:
        # Keep only ATOM records (protein), skip HOH/HETATM
        if line.startswith('ATOM'):
            fout.write(line)
        elif line.startswith('END') or line.startswith('TER'):
            fout.write(line)

# Verify
import subprocess
result = subprocess.run(['grep', '-c', '^ATOM', RECEPTOR_PDB], capture_output=True, text=True)
print(f"ATOM lines in receptor: {result.stdout.strip()}")
result2 = subprocess.run(['grep', '-c', '^HETATM', RECEPTOR_PDB], capture_output=True, text=True)
print(f"HETATM lines: {result2.stdout.strip()}")
print(f"Receptor written: {RECEPTOR_PDB}")
