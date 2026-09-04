
import subprocess, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
results_dir = os.path.join(wd, "docking_results")
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

pdbqt1 = os.path.join(ligands_dir, "lig1.pdbqt")
out1 = os.path.join(results_dir, "lig1_test_out.pdbqt")
log1 = os.path.join(results_dir, "lig1_test.log")

r = subprocess.run([
    vina_bin,
    '--receptor', receptor_pdbqt,
    '--ligand', pdbqt1,
    '--out', out1,
    '--log', log1,
    '--center_x', '30.0', '--center_y', '3.4', '--center_z', '-24.8',
    '--size_x', '25', '--size_y', '25', '--size_z', '25',
    '--exhaustiveness', '8',
    '--num_modes', '5',
    '--energy_range', '3'
], capture_output=True, text=True, timeout=120)

print("RC:", r.returncode)
print("STDOUT:", r.stdout[:1000])
print("STDERR:", r.stderr[:500])
