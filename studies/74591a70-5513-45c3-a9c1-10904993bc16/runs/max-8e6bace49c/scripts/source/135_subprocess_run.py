
import subprocess

AMBER_BIN = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"

# Find and read NMET template atom names from aminont12.lib
r = subprocess.run(
    ["grep", "-n", "NMET", f"{AMBERHOME}/dat/leap/lib/aminont12.lib"],
    capture_output=True, text=True
)
print("NMET occurrences in aminont12.lib:")
print(r.stdout[:500])

# Get the atom section
r2 = subprocess.run(
    ["grep", "-A", "60", '"NMET"', f"{AMBERHOME}/dat/leap/lib/aminont12.lib"],
    capture_output=True, text=True
)
# Print just atom entries (lines with atom names)
lines = r2.stdout.splitlines()
in_atoms = False
for line in lines[:100]:
    if 'unit.atoms table' in line.lower() or 'unit.atoms ' in line.lower():
        in_atoms = True
    if in_atoms:
        print(line)
        if in_atoms and line.startswith('!') and 'unit.atoms' not in line:
            break
