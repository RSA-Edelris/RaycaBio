
# Find mdrun command line in the successful log
with open(f"{BASE}/slurm-6319835.log") as f:
    content = f.read()

# Show lines containing mdrun and GPU info
for i, line in enumerate(content.split('\n')):
    if any(k in line for k in ['mdrun', 'gpu', 'GPU', 'ntomp', 'ntmpi', 'nsteps', 'Hardware']):
        print(f"{i:4d}: {line}")
