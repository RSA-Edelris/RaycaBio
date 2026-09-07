
import subprocess

# Find all Python executables and check which has mdtraj
for py in [
    "/home/ubuntu/rayca-runtime/.venv/bin/python3",
    "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python3",
    "/usr/bin/python3",
    "/home/ubuntu/rayca-runtime/.mamba/bin/python3",
]:
    r = subprocess.run([py, "-c", "import mdtraj; import parmed; import openmm; print('OK', mdtraj.__version__, parmed.__version__, openmm.__version__)"],
                       capture_output=True, text=True, timeout=15)
    if r.returncode == 0:
        print(f"{py}: {r.stdout.strip()}")
    else:
        print(f"{py}: FAIL - {r.stderr.strip()[:80]}")
