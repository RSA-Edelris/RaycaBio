
import subprocess
r = subprocess.run(
    ['/home/ubuntu/rayca-runtime/.venv/bin/python3', '-c', '''
import inspect
from openmmforcefields.generators import GAFFTemplateGenerator

# Check the actual template generation method - does it call antechamber with SDF/mol2?
src = inspect.getsource(GAFFTemplateGenerator.generate_residue_template)
print("--- generate_residue_template ---")
print(src[:4000])
'''],
    capture_output=True, text=True
)
print(r.stdout[:5000])
print(r.stderr[:500])
