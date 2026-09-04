
import subprocess, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"

# Check what docking tools are available locally
for tool in ['vina', 'gnina', 'obabel', 'qvina2']:
    r = subprocess.run(['which', tool], capture_output=True, text=True)
    print(f"{tool:10s}: {r.stdout.strip() or 'NOT FOUND'}")

# Also check conda envs
r = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
print("\nConda envs:")
print(r.stdout)
