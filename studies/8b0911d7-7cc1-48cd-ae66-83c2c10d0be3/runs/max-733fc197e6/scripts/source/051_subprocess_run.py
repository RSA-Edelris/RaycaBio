
import subprocess
r = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3', '-c', '''
import inspect
from openmmforcefields.generators import GAFFTemplateGenerator, SMIRNOFFTemplateGenerator
# Check what generators are available
from openmmforcefields import generators
print("Available generators:", [x for x in dir(generators) if "Generator" in x or "generator" in x.lower()])

# Check if GAFFTemplateGenerator init accepts smiles
src = inspect.getsource(GAFFTemplateGenerator.__init__)
print("\\n--- __init__ source ---\\n", src[:3000])
'''],
    capture_output=True, text=True
)
print(r.stdout[:4000])
print(r.stderr[:1000])
