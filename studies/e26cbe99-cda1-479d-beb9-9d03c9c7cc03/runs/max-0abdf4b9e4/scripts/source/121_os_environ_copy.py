
import subprocess, os

SESSION = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
md = f"{SESSION}/md_EDS01806218_ent1"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"

cmd = [
    f"{AMBERHOME}/bin/MMPBSA.py",
    "-O",
    "-i",  f"{md}/mmpbsa.in",
    "-o",  f"{md}/mmpbsa_results.dat",
    "-do", f"{md}/mmpbsa_decomp.dat",
    "-cp", f"{md}/complex_nowater.prmtop",
    "-rp", f"{md}/receptor.prmtop",
    "-lp", f"{md}/ligand.prmtop",
    "-y",  f"{md}/prod_nowater.nc",
]

env = os.environ.copy()
env["AMBERHOME"] = AMBERHOME

print("Running MMPBSA.py for EDS01806218_ent1 ...")
r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=md)
print("Return code:", r.returncode)

# Print last ~60 lines (summary)
out_lines = (r.stdout + r.stderr).splitlines()
for line in out_lines[-60:]:
    print(line)
