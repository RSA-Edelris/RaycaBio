
import subprocess

# Check AmberTools executables available
amber_tools = ['antechamber', 'parmchk2', 'tleap', 'cpptraj', 'pmemd', 'sander', 'ambpdb']
for t in amber_tools:
    r = subprocess.run(['which', t], capture_output=True, text=True)
    status = r.stdout.strip() if r.returncode == 0 else 'not found'
    print(f"  {t:15s}: {status}")

# Check parmed version
import parmed
print(f"\nparmed version: {parmed.__version__}")

# Check mdtraj version
import mdtraj
print(f"mdtraj version: {mdtraj.__version__}")

# Confirm best ligand SDF exists
import os
sdf = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/poses_EDS01806218_ent2.sdf'
print(f"\nBest ligand SDF exists: {os.path.exists(sdf)}, size: {os.path.getsize(sdf)} bytes")
