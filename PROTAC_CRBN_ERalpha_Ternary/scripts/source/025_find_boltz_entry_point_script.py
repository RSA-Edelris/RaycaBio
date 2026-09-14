
import subprocess, sys

# Find the boltz entry point script
r = subprocess.run(['which', 'boltz'], capture_output=True, text=True)
print("boltz binary:", r.stdout.strip())

r2 = subprocess.run([sys.executable, '-c',
    'import boltz; import os; print(os.path.dirname(boltz.__file__))'],
    capture_output=True, text=True)
boltz_dir = r2.stdout.strip()
print("boltz dir:", boltz_dir)

# list top-level contents
r3 = subprocess.run(['ls', boltz_dir], capture_output=True, text=True)
print("contents:", r3.stdout.strip())
