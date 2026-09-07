
import subprocess, os
from pathlib import Path

# Locate AMBERHOME: should be the conda env root
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
spc = Path(AMBERHOME) / "dat/mmpbsa/spc.xvv"
print(f"spc.xvv exists: {spc.exists()}  ({spc})")

# Update amber_env to set AMBERHOME
def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["AMBERHOME"] = AMBERHOME
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd],
                       cwd=cwd, capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n"
                           f"STDOUT: {r.stdout[-2000:]}\nSTDERR: {r.stderr[-2000:]}")
    return r

test_d = Path(MMDIR) / "EDEL-CRBN-0001_ent"

print("\nRetrying MMPBSA.py with AMBERHOME set...")
run([f"{AMBER}/MMPBSA.py",
     "-O",
     "-i", "mmgbsa_test.in",
     "-o", "FINAL_RESULTS_MMPBSA.dat",
     "-sp", "complex.prmtop",
     "-rp", "rec.prmtop",
     "-lp", "lig.prmtop",
     "-y", "md_test.nc"],
    cwd=str(test_d))
print("Done")

dat = (test_d / "FINAL_RESULTS_MMPBSA.dat").read_text()
for line in dat.split("\n"):
    if any(k in line for k in ["DELTA G", "VDWAALS", "EEL", "EGB", "ESURF"]):
        print(" ", line)
