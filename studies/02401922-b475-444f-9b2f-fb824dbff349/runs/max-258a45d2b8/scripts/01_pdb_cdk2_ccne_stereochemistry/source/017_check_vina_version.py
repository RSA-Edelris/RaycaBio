
import subprocess

# Check vina version
r = subprocess.run(['vina', '--version'], capture_output=True, text=True)
print("Vina:", r.stdout.strip() or r.stderr.strip())

# Check meeko
import meeko
print("Meeko:", meeko.__version__)

# Prepare receptor PDBQT with obabel (strip H, add Gasteiger charges)
r2 = subprocess.run(
    ['obabel', 'receptor_prepared.pdb', '-O', 'receptor.pdbqt',
     '-xr',          # remove non-polar H
     '--partialcharge', 'gasteiger'],
    capture_output=True, text=True, cwd=WS
)
print("Receptor PDBQT:", r2.stderr.strip())

import os
sz = os.path.getsize(f'{WS}/receptor.pdbqt')
print(f"receptor.pdbqt: {sz:,} bytes")
