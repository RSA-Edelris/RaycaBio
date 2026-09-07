
import subprocess
from pathlib import Path

# Check what the timed-out minimisation produced
min_rst = Path(f"{lig_dir}/min.rst7")
min_out = Path(f"{lig_dir}/min.out")
print(f"min.rst7: {min_rst.stat().st_size} B")

# Read the last 30 lines of min.out to see how far it got
out_text = min_out.read_text()
tail = out_text.split("\n")
# Find last NSTEP line
nstep_lines = [l for l in tail if "NSTEP" in l and "=" in l]
energy_lines = [l for l in tail if "ENERGY" in l and "=" in l]
print("Last NSTEP lines:", nstep_lines[-3:])
print("Last ENERGY lines:", energy_lines[-3:])
print("Last 10 lines:\n", "\n".join(tail[-10:]))
