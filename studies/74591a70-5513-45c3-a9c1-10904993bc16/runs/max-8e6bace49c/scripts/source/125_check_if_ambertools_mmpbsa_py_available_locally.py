
import subprocess
# Check if AmberTools / MMPBSA.py is available locally
for tool in ['tleap', 'antechamber', 'MMPBSA.py', 'sander', 'pmemd']:
    r = subprocess.run(['which', tool], capture_output=True, text=True)
    print(f"{tool}: {r.stdout.strip() or 'NOT FOUND'}")
