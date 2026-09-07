
import subprocess, os, time
from pathlib import Path

def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None); env.pop("PYTHONHOME", None)
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd],
                       cwd=cwd, capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n"
                           f"STDOUT: {r.stdout[-2000:]}\nSTDERR: {r.stderr[-2000:]}")
    return r

test_d = Path(MMDIR) / "EDEL-CRBN-0001_ent"

# Remove old MMPBSA result if any
for f in ["FINAL_RESULTS_MMPBSA.dat", "_MMPBSA_*", "reference.frc"]:
    for p in test_d.glob(f):
        p.unlink()

mmgbsa_test_in = """\
MM-GBSA test (2 frames)
 &general
  startframe=1, endframe=2, interval=1,
 /
 &gb
  igb=5, saltcon=0.10, intdiel=1.0, extdiel=78.5,
 /
"""
(test_d / "mmgbsa_test.in").write_text(mmgbsa_test_in)

print("Running MMPBSA.py test on 2-frame trajectory...")
t0 = time.time()
run([f"{AMBER}/MMPBSA.py",
     "-O",
     "-i", "mmgbsa_test.in",
     "-o", "FINAL_RESULTS_MMPBSA.dat",
     "-sp", "complex.prmtop",
     "-rp", "rec.prmtop",
     "-lp", "lig.prmtop",
     "-y", "md_test.nc"],
    cwd=str(test_d))
elapsed = time.time() - t0
print(f"Done in {elapsed:.1f}s")

# Parse and show result
dat = (test_d / "FINAL_RESULTS_MMPBSA.dat").read_text()
# Print the DELTA G section
for line in dat.split("\n"):
    if "DELTA" in line or "VDWAALS" in line or "EEL" in line or "EGB" in line or "ESURF" in line:
        print(" ", line)
