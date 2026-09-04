
import subprocess, os, re

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
results_dir = os.path.join(wd, "docking_results")
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

# Check score format in output PDBQT
out1 = os.path.join(results_dir, "lig1_out.pdbqt")
with open(out1) as f:
    c = f.read()
print("lig1_out.pdbqt head (first 600 chars):")
print(c[:600])
