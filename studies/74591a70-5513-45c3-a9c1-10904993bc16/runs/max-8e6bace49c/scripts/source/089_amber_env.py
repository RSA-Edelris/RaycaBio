
import subprocess, os
from pathlib import Path

AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"

def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None); env.pop("PYTHONHOME", None)
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

# Corrected input — intdiel/extdiel not valid in &gb for Amber24 MMPBSA.py
mmgbsa_in = """\
MM-GBSA
 &general
  startframe=1, endframe=2, interval=1,
 /
 &gb
  igb=5, saltcon=0.10,
 /
"""
(test_d / "mmgbsa_test.in").write_text(mmgbsa_in)

run([f"{AMBER}/MMPBSA.py",
     "-O",
     "-i", "mmgbsa_test.in",
     "-o", "FINAL_RESULTS_MMPBSA.dat",
     "-sp", "complex.prmtop",
     "-rp", "rec.prmtop",
     "-lp", "lig.prmtop",
     "-y", "md_test.nc"],
    cwd=str(test_d))
print("MMPBSA.py succeeded!")

dat = (test_d / "FINAL_RESULTS_MMPBSA.dat").read_text()
for line in dat.split("\n"):
    if any(k in line for k in ["DELTA G", "VDWAALS", "EEL", "EGB", "ESURF", "Total"]):
        print(" ", line)
