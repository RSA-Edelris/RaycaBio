
import subprocess

py     = "/home/ubuntu/rayca-runtime/.venv/bin/python3"
script = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/mmgbsa_calc.py"
cwd    = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

print("Running MM-GBSA (ParmEd direct path, timeout=600s)...")
r = subprocess.run([py, script], capture_output=True, text=True, cwd=cwd, timeout=600)

print("=== STDOUT ===")
print(r.stdout[-5000:] if len(r.stdout) > 5000 else r.stdout)
if r.returncode != 0:
    print("=== STDERR ===")
    print(r.stderr[-2000:])
print(f"Return code: {r.returncode}")
