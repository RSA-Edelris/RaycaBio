
# Check available Python packages for structure analysis
import subprocess, sys

for mod in ['scipy', 'numpy', 'openbabel', 'pdbfixer', 'openmm']:
    try:
        __import__(mod)
        print(f"  OK: {mod}")
    except ImportError:
        print(f"  MISSING: {mod}")

# Try installing MDAnalysis
result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'MDAnalysis', '-q', '--no-deps'], 
                       capture_output=True, text=True)
print("MDAnalysis install:", result.returncode, result.stderr[:100] if result.stderr else "ok")
