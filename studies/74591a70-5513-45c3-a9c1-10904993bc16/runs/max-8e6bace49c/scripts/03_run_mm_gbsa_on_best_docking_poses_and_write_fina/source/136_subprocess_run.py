
import subprocess

AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
# Read lines around the NMET atom section
r = subprocess.run(
    ["sed", "-n", "2133,2175p", f"{AMBERHOME}/dat/leap/lib/aminont12.lib"],
    capture_output=True, text=True
)
print(r.stdout)
