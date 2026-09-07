
import subprocess, importlib

tools = ['openmm', 'openmmforcefields', 'openff.toolkit', 'openff.interchange',
         'parmed', 'mdtraj', 'MDAnalysis', 'pdbfixer']

for t in tools:
    try:
        importlib.import_module(t.replace('-','_'))
        print(f"  AVAILABLE: {t}")
    except ImportError:
        print(f"  missing:   {t}")

for cmd in ['antechamber', 'acpype', 'gmx', 'obabel', 'python3']:
    r = subprocess.run(['which', cmd], capture_output=True, text=True)
    status = r.stdout.strip() if r.returncode == 0 else "not found"
    print(f"  CLI: {cmd} -> {status}")
