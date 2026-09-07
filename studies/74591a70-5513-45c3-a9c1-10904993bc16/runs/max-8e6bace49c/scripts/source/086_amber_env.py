
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
                           f"STDOUT: {r.stdout[-1500:]}\nSTDERR: {r.stderr[-1500:]}")
    return r

test_d = Path(MMDIR) / "EDEL-CRBN-0001_ent"

# Quick 400-step MD → 2 frames (save every 200 steps)
md_test_in = """\
NVT test MD 2 frames
 &cntrl
  imin=0, nstlim=400, dt=0.002,
  ntb=0, cut=12.0, rgbmax=12.0,
  igb=5, saltcon=0.10,
  tempi=300.0, temp0=300.0,
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntpr=200, ntwx=200,
  ioutfm=1,
 /
"""
(test_d / "md_test.in").write_text(md_test_in)
(test_d / "md_test.nc").unlink(missing_ok=True)

print("Running 400-step test MD on EDEL-CRBN-0001...")
t0 = time.time()
run([f"{AMBER}/sander",
     "-O", "-i", "md_test.in",
     "-o", "md_test.out",
     "-p", "complex.prmtop",
     "-c", "min.rst7",
     "-r", "md_test.rst7",
     "-x", "md_test.nc"],
    cwd=str(test_d))
elapsed = time.time() - t0
nc = test_d / "md_test.nc"
print(f"Done in {elapsed:.0f}s — md_test.nc: {nc.stat().st_size//1024} kB")
print(f"Speed: {elapsed/400*1000:.0f} ms/step (rgbmax=12 vs 585ms before)")
