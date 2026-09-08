
# Check available libraries for MM-GBSA post-processing
import importlib, subprocess, sys

libs = ["openmm", "mdtraj", "parmed", "numpy", "scipy", "rdkit", "openff.toolkit"]
for lib in libs:
    try:
        m = importlib.import_module(lib)
        ver = getattr(m, "__version__", "?")
        print(f"  {lib}: {ver}")
    except ImportError as e:
        print(f"  {lib}: MISSING ({e})")
