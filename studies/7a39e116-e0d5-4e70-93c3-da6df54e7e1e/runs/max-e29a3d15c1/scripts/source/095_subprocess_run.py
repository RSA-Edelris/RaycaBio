
import subprocess, os

work_dir = "gbsa_run/EL2003A_pose2"
gmx_dir  = f"{work_dir}/complex.GMX"

# Count frames in traj_com.xtc
r = subprocess.run(
    ["gmx", "check", "-f", f"{work_dir}/traj_com.xtc"],
    capture_output=True, text=True, cwd="."
)
print("traj_com.xtc info:")
for line in (r.stdout + r.stderr).splitlines():
    if any(k in line for k in ["frame", "time", "atoms", "Last"]):
        print(" ", line)

# Look at unique residue names in complex_reres.pdb
resnames = set()
with open(f"{work_dir}/complex_reres.pdb") as f:
    for line in f:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            resnames.add(line[17:20].strip())
print("\nResidue names in complex:", sorted(resnames))

# Count atoms per residue type
from collections import Counter
res_count = Counter()
with open(f"{work_dir}/complex_reres.pdb") as f:
    for line in f:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            rn = line[17:20].strip()
            res_count[rn] += 1
print("Atom count per residue type:", res_count)
