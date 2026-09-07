
import subprocess

env = {"AMBERHOME": AMBERHOME, "PATH": f"{AMBERHOME}/bin:/usr/bin:/bin"}

print("=== Step 2: MMPBSA.py ===")
r = subprocess.run(
    [f"{AMBERHOME}/bin/MMPBSA.py", "-O",
     "-i",  f"{MD}/mmpbsa.in",
     "-o",  f"{MD}/mmpbsa_results.dat",
     "-do", f"{MD}/mmpbsa_decomp.dat",
     "-sp", f"{MD}/complex.prmtop",
     "-cp", f"{MD}/complex_nowater.prmtop",
     "-rp", f"{MD}/receptor.prmtop",
     "-lp", f"{MD}/ligand.prmtop",
     "-y",  f"{MD}/prod_nowater.nc"],
    capture_output=True, text=True, timeout=1800, env=env
)
print(r.stdout[-4000:] if len(r.stdout) > 4000 else r.stdout)
if r.returncode != 0:
    print("STDERR:", r.stderr[-2000:])
    raise RuntimeError(f"MMPBSA.py failed (rc={r.returncode})")
print("Return code:", r.returncode)
