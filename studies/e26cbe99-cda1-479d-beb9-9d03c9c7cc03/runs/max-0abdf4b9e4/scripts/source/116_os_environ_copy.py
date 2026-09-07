
import subprocess, os, threading

session = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"

env = os.environ.copy()
env["AMBERHOME"] = AMBERHOME

compounds = ["EDS01357518_ent1", "EDS01889984"]
results = {}

def run_mmpbsa(comp):
    md_dir = f"{session}/md_{comp}"
    cmd = [
        "MMPBSA.py", "-O",
        "-i",  f"{md_dir}/mmpbsa.in",
        "-o",  f"{md_dir}/mmpbsa_results.dat",
        "-do", f"{md_dir}/mmpbsa_decomp.dat",
        "-cp", f"{md_dir}/complex_nowater.prmtop",
        "-rp", f"{md_dir}/receptor.prmtop",
        "-lp", f"{md_dir}/ligand.prmtop",
        "-y",  f"{md_dir}/prod_nowater.nc",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=md_dir, env=env)
    results[comp] = r

threads = [threading.Thread(target=run_mmpbsa, args=(c,)) for c in compounds]
for t in threads: t.start()
for t in threads: t.join()

for comp in compounds:
    r = results[comp]
    print(f"\n=== {comp} (rc={r.returncode}) ===")
    if r.returncode == 0:
        md_dir = f"{session}/md_{comp}"
        with open(f"{md_dir}/mmpbsa_results.dat") as f:
            for line in f:
                if any(k in line for k in ["DELTA TOTAL", "VDWAALS", "EEL", "EGB", "ESURF"]):
                    print(line.rstrip())
    else:
        print(r.stdout[-1500:])
        print("STDERR:", r.stderr[-800:])
