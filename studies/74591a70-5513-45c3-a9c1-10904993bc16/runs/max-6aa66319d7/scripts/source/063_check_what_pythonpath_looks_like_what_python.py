
import subprocess, os

# Check what PYTHONPATH looks like and what Python pdb4amber uses
r = subprocess.run(
    [f"{AMBER}/pdb4amber", "--version"],
    capture_output=True, text=True,
    env={**os.environ}
)
print("STDERR:", r.stderr[:500])

# Check shebang of pdb4amber
with open(f"{AMBER}/pdb4amber") as f:
    print("Shebang:", f.readline().strip())

# Check PYTHONPATH
print("PYTHONPATH:", os.environ.get("PYTHONPATH", "(not set)"))
print("PATH[:200]:", os.environ.get("PATH","")[:200])

# Check Python in conda env
r2 = subprocess.run(
    ["/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python", "--version"],
    capture_output=True, text=True,
    env={"PATH": "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin:/usr/bin:/bin",
         "HOME": os.environ.get("HOME", "/root")}
)
print("Conda python:", r2.stdout.strip() or r2.stderr.strip())
