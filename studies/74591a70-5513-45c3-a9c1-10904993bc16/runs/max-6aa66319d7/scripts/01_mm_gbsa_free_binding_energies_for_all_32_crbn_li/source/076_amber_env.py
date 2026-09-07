
import subprocess, os, json

def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(
            f"FAILED: {' '.join(str(c) for c in cmd)}\n"
            f"STDOUT: {r.stdout[-1500:]}\nSTDERR: {r.stderr[-1500:]}")
    return r

MMDIR = f"{WORK}/mmgbsa"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"

# Load the 32 compound names
with open(f"{WORK}/docking_scores_all32.json") as fh:
    scores = json.load(fh)
names = list(scores.keys())
print(f"Total ligands: {len(names)}")
print(names[:5])
