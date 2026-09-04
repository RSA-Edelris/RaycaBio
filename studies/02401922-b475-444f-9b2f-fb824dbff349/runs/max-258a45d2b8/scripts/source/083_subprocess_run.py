
import subprocess
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
r = subprocess.run([vina_bin, '--help'], capture_output=True, text=True)
print(r.stdout)
print(r.stderr)
