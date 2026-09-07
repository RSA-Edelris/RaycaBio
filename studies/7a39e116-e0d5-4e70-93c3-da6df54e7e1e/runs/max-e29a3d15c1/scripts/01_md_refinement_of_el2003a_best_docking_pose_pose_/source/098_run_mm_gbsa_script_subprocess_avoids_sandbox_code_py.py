
import subprocess, sys

# Run the MM-GBSA script as a subprocess (avoids sandbox code.py shadow)
py = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python3"
script = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/mmgbsa_calc.py"
cwd = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

print("Launching MM-GBSA subprocess...")
result = subprocess.run(
    [py, script],
    capture_output=True,
    text=True,
    cwd=cwd,
    timeout=600,
)
print("=== STDOUT ===")
print(result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout)
if result.returncode != 0:
    print("=== STDERR ===")
    print(result.stderr[-2000:])
print(f"\nReturn code: {result.returncode}")
