
import subprocess
# Check what's installed that could provide molecule objects for GAFF
r = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/pip', 'list'],
    capture_output=True, text=True
)
lines = [l for l in r.stdout.splitlines() if any(x in l.lower() for x in ['openff', 'openmm', 'rdkit', 'gaff', 'espaloma', 'openfe', 'interchange', 'mdtraj'])]
print('\n'.join(lines))

# Also check the GAFFTemplateGenerator source for accepted types
r2 = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3', '-c',
     'import inspect; from openmmforcefields.generators import GAFFTemplateGenerator; src = inspect.getsource(GAFFTemplateGenerator.add_molecules); print(src[:3000])'],
    capture_output=True, text=True
)
print("\n--- add_molecules source ---\n", r2.stdout[:3000])
print(r2.stderr[:500])
