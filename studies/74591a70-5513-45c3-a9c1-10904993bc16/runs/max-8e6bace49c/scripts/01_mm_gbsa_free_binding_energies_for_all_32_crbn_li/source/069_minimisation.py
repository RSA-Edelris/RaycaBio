
import subprocess
from pathlib import Path

# ── Minimisation ──────────────────────────────────────────────────────────────
min_in = """\
Energy minimization in GB implicit solvent
 &cntrl
  imin=1, maxcyc=2000, ncyc=500,
  ntb=0, cut=999.0,
  igb=5, saltcon=0.10,
  ntpr=200, ntwx=0,
 /
"""
Path(f"{lig_dir}/min.in").write_text(min_in)

r = subprocess.run(
    [f"{AMBER}/sander",
     "-O", "-i", "min.in", "-o", "min.out",
     "-p", "complex.prmtop", "-c", "complex.inpcrd", "-r", "min.rst7"],
    cwd=lig_dir, capture_output=True, text=True, timeout=300
)
print("sander min rc:", r.returncode)
if r.returncode != 0:
    print("STDERR:", r.stderr[-600:])

# Read last lines of output to confirm convergence
out = Path(f"{lig_dir}/min.out").read_text()
# Find last NSTEP block
last_block = [l for l in out.split("\n") if "NSTEP" in l or "ENERGY" in l]
print("\n".join(last_block[-6:]))
print("min.rst7:", Path(f"{lig_dir}/min.rst7").stat().st_size, "B")
