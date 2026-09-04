
import subprocess, os, re

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
results_dir = os.path.join(wd, "docking_results")
ligands_dir = os.path.join(wd, "ligands_3d")
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

missing_nums = [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,
                51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,
                70,71,72,73,74,75,76,77,78,79,80,81,82,83,84]

missing_pdbqts = [os.path.join(ligands_dir, f"lig{n}.pdbqt") for n in missing_nums]

# Write batch script
script = f"""#!/usr/bin/env python3
import subprocess, os, time
vina_bin = "{vina_bin}"
receptor = "{receptor_pdbqt}"
results_dir = "{results_dir}"
ligands_dir = "{ligands_dir}"
missing = {missing_nums}

for n in missing:
    pdbqt = os.path.join(ligands_dir, f"lig{{n}}.pdbqt")
    out = os.path.join(results_dir, f"lig{{n}}_out.pdbqt")
    if os.path.exists(out):
        print(f"skip {{n}} (exists)", flush=True)
        continue
    r = subprocess.run([
        vina_bin, '--receptor', receptor, '--ligand', pdbqt,
        '--out', out,
        '--center_x','30.0','--center_y','3.4','--center_z','-24.8',
        '--size_x','25','--size_y','25','--size_z','25',
        '--exhaustiveness','8','--num_modes','5','--energy_range','3',
        '--verbosity','0'
    ], capture_output=True, text=True, timeout=120)
    print(f"done {{n}} rc={{r.returncode}}", flush=True)

print("ALL DONE", flush=True)
"""

script_path = os.path.join(wd, "run_missing.py")
with open(script_path, 'w') as f:
    f.write(script)

bg_log = os.path.join(wd, "missing_docking.log")
proc = subprocess.Popen(
    ['/usr/bin/python3', script_path],
    stdout=open(bg_log, 'w'), stderr=subprocess.STDOUT
)
print(f"PID {proc.pid} launched, log: {bg_log}")
print(f"Running {len(missing_nums)} compounds in background (~{len(missing_nums)*26//60} min)")
