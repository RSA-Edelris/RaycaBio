
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

# Remove ALL _MMPBSA_* temp files left by prior failed runs
removed = []
for p in list(test_d.glob("_MMPBSA_*")) + list(test_d.glob("reference.frc")):
    p.unlink()
    removed.append(p.name)
print(f"Cleaned: {removed}")

# Use absolute paths for everything
run([f"{AMBER}/MMPBSA.py",
     "-O",
     "-i",  str(test_d / "mmgbsa_test.in"),
     "-o",  str(test_d / "FINAL_RESULTS_MMPBSA.dat"),
     "-cp", str(test_d / "complex.prmtop"),    # -cp not -sp (complex prmtop)
     "-rp", str(test_d / "rec.prmtop"),
     "-lp", str(test_d / "lig.prmtop"),
     "-y",  str(test_d / "md_test.nc")],
    cwd=str(test_d))
print("MMPBSA.py succeeded!")

dat = (test_d / "FINAL_RESULTS_MMPBSA.dat").read_text()
for line in dat.split("\n"):
    if any(k in line for k in ["DELTA G", "VDWAALS", "EEL", "EGB", "ESURF"]):
        print(" ", line)
