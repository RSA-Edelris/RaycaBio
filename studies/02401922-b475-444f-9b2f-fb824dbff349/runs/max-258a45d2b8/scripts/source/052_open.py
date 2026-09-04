
import os, subprocess

wd = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'

# Count atoms in solvated complex
n_atoms = 0
with open(f'{wd}/complex_solv.pdb') as f:
    for line in f:
        if line.startswith(('ATOM','HETATM')):
            n_atoms += 1
print(f"Total atoms in solvated complex: {n_atoms}")

# Check pmemd.cuda
amber_home = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
for binary in ['pmemd.cuda', 'pmemd.cuda.MPI', 'pmemd']:
    path = f'{amber_home}/bin/{binary}'
    exists = os.path.exists(path)
    print(f"{binary}: {'FOUND' if exists else 'not found'}")

# Also check GROMACS gmx
for binary in ['gmx', 'gmx_gpu', 'gmx_mpi']:
    r = subprocess.run(['which', binary], capture_output=True, text=True)
    print(f"{binary}: {r.stdout.strip() or 'not found'}")
