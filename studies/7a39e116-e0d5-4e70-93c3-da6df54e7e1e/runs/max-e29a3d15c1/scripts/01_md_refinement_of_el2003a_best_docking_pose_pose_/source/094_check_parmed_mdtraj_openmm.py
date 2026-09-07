
import subprocess, sys

# Check ParmEd, MDTraj, OpenMM
for mod in ["parmed", "mdtraj", "openmm"]:
    try:
        m = __import__(mod)
        print(f"{mod}: OK (version={getattr(m, '__version__', '?')})")
    except ImportError as e:
        print(f"{mod}: MISSING ({e})")

# Check if gmx_MMPBSA is installable (pip show)
r = subprocess.run([sys.executable, "-m", "pip", "show", "gmx_MMPBSA"],
                   capture_output=True, text=True)
print("pip show gmx_MMPBSA:", r.stdout[:200] or r.stderr[:100])

# sander version
r = subprocess.run(["sander", "--version"], capture_output=True, text=True)
print("sander:", (r.stdout + r.stderr)[:200])
