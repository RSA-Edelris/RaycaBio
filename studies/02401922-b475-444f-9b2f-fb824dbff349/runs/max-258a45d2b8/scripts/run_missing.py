#!/usr/bin/env python3
import subprocess, os, time
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a/receptor.pdbqt"
results_dir = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a/docking_results"
ligands_dir = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a/ligands_3d"
missing = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]

for n in missing:
    pdbqt = os.path.join(ligands_dir, f"lig{n}.pdbqt")
    out = os.path.join(results_dir, f"lig{n}_out.pdbqt")
    if os.path.exists(out):
        print(f"skip {n} (exists)", flush=True)
        continue
    r = subprocess.run([
        vina_bin, '--receptor', receptor, '--ligand', pdbqt,
        '--out', out,
        '--center_x','30.0','--center_y','3.4','--center_z','-24.8',
        '--size_x','25','--size_y','25','--size_z','25',
        '--exhaustiveness','8','--num_modes','5','--energy_range','3',
        '--verbosity','0'
    ], capture_output=True, text=True, timeout=120)
    print(f"done {n} rc={r.returncode}", flush=True)

print("ALL DONE", flush=True)
