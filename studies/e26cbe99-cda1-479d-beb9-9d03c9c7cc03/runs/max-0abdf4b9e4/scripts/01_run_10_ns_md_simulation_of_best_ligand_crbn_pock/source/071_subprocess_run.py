
import subprocess, os
WD = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85'

# Check antechamber version
r = subprocess.run(['antechamber', '-h'], capture_output=True, text=True)
print("antechamber available:", r.returncode == 0 or 'usage' in r.stderr.lower() or 'ANTECHAMBER' in r.stderr)

# Check openmmforcefields version and GAFF availability
from openmmforcefields.generators import GAFFTemplateGenerator
print("GAFFTemplateGenerator imported OK")

# Check local gmx version (to decide cpu-only vs send to Isambard)
r2 = subprocess.run(['gmx', '--version'], capture_output=True, text=True)
for line in (r2.stdout + r2.stderr).splitlines():
    if 'GROMACS' in line or 'GPU' in line or 'CUDA' in line or 'version' in line.lower():
        print(line)

# List the complex PDB files to confirm they exist
import glob
cpx = sorted(glob.glob(f'{WD}/complex_*.pdb'))
for f in cpx:
    print(os.path.basename(f), os.path.getsize(f), 'bytes')
