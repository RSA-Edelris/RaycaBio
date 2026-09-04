
# Check available tools for receptor/ligand prep
import subprocess
tools = ['obabel', 'reduce', 'pdb4amber']
for t in tools:
    r = subprocess.run(['which', t], capture_output=True, text=True)
    print(t, ':', r.stdout.strip() or 'NOT FOUND')

# Check python packages
for pkg in ['rdkit', 'pdbfixer', 'openbabel', 'meeko']:
    try:
        __import__(pkg)
        print(pkg, ': OK')
    except ImportError:
        print(pkg, ': MISSING')
