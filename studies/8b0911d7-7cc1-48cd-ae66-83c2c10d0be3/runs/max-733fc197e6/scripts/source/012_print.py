
import sys, subprocess

python_exe = sys.executable
print(f"session Python: {python_exe}")

# Run script with correct interpreter
r = subprocess.run([python_exe, script], capture_output=True, text=True, cwd=WORKDIR)
print(r.stdout[-4000:])
if r.returncode != 0:
    print("STDERR:", r.stderr[-500:])
