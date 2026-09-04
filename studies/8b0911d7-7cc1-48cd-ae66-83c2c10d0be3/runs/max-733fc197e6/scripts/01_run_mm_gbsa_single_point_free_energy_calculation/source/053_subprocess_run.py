
import subprocess

for tool in ['antechamber', 'parmchk2', 'tleap', 'sqm']:
    r = subprocess.run(['which', tool], capture_output=True, text=True)
    print(f"{tool}: {r.stdout.strip() or 'NOT FOUND'}")

# Also check parmed
r2 = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3', '-c', 'import parmed; print("parmed", parmed.__version__)'],
    capture_output=True, text=True
)
print(r2.stdout.strip(), r2.stderr.strip())
