
import subprocess
from pathlib import Path
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

# Quick check of receptor PDB
r = subprocess.run(['head', '-20', str(BASE / '4CI2_receptor_for_docking.pdb')], capture_output=True, text=True)
print(r.stdout)
r2 = subprocess.run(['grep', '-c', '^ATOM', str(BASE / '4CI2_receptor_for_docking.pdb')], capture_output=True, text=True)
r3 = subprocess.run(['grep', '-c', '^HETATM', str(BASE / '4CI2_receptor_for_docking.pdb')], capture_output=True, text=True)
r4 = subprocess.run(['grep', '^HETATM', str(BASE / '4CI2_receptor_for_docking.pdb')], capture_output=True, text=True)
print(f"ATOM records: {r2.stdout.strip()}")
print(f"HETATM records: {r3.stdout.strip()}")
print("HETATM lines (first 5):")
for line in r4.stdout.strip().split('\n')[:5]:
    print(f"  {line}")
