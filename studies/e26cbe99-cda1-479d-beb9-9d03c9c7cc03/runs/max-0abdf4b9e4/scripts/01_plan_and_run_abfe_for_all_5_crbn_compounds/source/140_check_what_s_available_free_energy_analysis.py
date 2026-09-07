
import subprocess

# Check what's available for free energy analysis
for pkg in ["alchemlyb", "pymbar", "scipy", "numpy"]:
    r = subprocess.run([PYTHON, "-c", f"import {pkg}; print({pkg}.__version__)"],
                       capture_output=True, text=True)
    status = r.stdout.strip() or r.stderr.strip()[:80]
    print(f"{pkg}: {status}")
