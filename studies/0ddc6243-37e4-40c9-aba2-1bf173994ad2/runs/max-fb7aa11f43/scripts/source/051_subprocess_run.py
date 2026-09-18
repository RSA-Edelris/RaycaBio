
import subprocess

for tool in ['parmchk2', 'tleap', 'cpptraj']:
    r = subprocess.run(['which', tool], capture_output=True, text=True)
    status = r.stdout.strip() if r.returncode == 0 else "NOT FOUND"
    print(f"{tool:12s}: {status}")
