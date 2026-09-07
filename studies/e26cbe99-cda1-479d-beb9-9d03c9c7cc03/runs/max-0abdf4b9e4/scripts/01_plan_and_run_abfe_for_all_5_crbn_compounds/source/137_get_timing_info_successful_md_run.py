
# Get timing info from successful MD run
with open(f"{BASE}/slurm-6319835.log") as f:
    content = f.read()

# Find performance lines
lines = content.split('\n')
for i, line in enumerate(lines):
    if any(k in line for k in ['Performance:', 'ns/day', 'hours/ns', 'Elapsed', 'Wall time', 'Time:']):
        print(f"{i:5d}: {line}")
