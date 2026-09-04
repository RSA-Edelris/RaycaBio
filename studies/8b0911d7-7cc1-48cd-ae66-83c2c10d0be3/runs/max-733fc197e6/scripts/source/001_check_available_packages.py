
import subprocess, sys

# Check available packages
for pkg in ['pdbfixer', 'propka', 'rdkit', 'dimorphite_dl', 'openmm']:
    try:
        __import__(pkg.replace('-','_'))
        print(f"OK: {pkg}")
    except ImportError:
        print(f"MISSING: {pkg}")
