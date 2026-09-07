
import subprocess
from pathlib import Path

# Check if prolif/MDAnalysis are available
for pkg in ['prolif', 'MDAnalysis', 'plip']:
    r = subprocess.run(
        ['/home/ubuntu/rayca-runtime/.venv/bin/python3', '-c', f'import {pkg}; print({pkg}.__version__)'],
        capture_output=True, text=True
    )
    print(f"{pkg}: {r.stdout.strip() or ('NOT FOUND: ' + r.stderr.strip()[:80])}")
