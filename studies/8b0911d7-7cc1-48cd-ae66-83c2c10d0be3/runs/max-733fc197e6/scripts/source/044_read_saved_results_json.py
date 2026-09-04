
import json, os

# Read the saved results JSON
results_path = os.path.join(WORKDIR, 'autodock-vina-results-4.json')
with open(results_path) as f:
    content = f.read()
print(f"File size: {len(content)} bytes")
print(content)
