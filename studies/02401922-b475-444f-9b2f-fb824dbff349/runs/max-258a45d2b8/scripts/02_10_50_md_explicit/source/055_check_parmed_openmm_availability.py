
import subprocess, sys

# Check ParmEd and OpenMM availability
for mod in ['parmed', 'openmm', 'openmm.app']:
    try:
        __import__(mod)
        import importlib
        m = importlib.import_module(mod)
        ver = getattr(m, '__version__', 'installed')
        print(f"{mod}: OK ({ver})")
    except ImportError as e:
        print(f"{mod}: MISSING — {e}")
