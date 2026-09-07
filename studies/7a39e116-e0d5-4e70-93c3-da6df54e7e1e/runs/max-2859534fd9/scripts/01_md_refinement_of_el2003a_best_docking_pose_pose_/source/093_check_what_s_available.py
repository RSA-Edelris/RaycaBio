
import subprocess

# Check what's available
for cmd in ["gmx_MMPBSA", "gmx_MMPBSA_ana", "gmx", "sander", "python3"]:
    r = subprocess.run(["which", cmd], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"{cmd}: {r.stdout.strip()}")
    else:
        print(f"{cmd}: NOT FOUND")

# Check gmx_MMPBSA version if available
r = subprocess.run(["gmx_MMPBSA", "--version"], capture_output=True, text=True)
if r.returncode == 0:
    print("gmx_MMPBSA version:", r.stdout[:200])
else:
    print("gmx_MMPBSA stderr:", r.stderr[:100])

# Check ParmEd, MDTraj, OpenMM
for mod in ["parmed", "mdtraj", "openmm"]:
    try:
        m = __import__(mod)
        print(f"{mod}: OK (version={getattr(m, '__version__', '?')})")
    except ImportError as e:
        print(f"{mod}: MISSING ({e})")
