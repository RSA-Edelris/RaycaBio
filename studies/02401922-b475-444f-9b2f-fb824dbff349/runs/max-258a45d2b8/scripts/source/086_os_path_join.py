
import subprocess, os, re, time

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
results_dir = os.path.join(wd, "docking_results")
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

def sdf_num(f):
    m = re.search(r'lig(\d+)\.pdbqt', f)
    return int(m.group(1)) if m else 0

all_pdbqts = sorted([os.path.join(ligands_dir, f)
                     for f in os.listdir(ligands_dir) if f.endswith('.pdbqt')],
                    key=lambda p: sdf_num(os.path.basename(p)))
print(f"Running batch vina on {len(all_pdbqts)} compounds...")
print(f"First: {os.path.basename(all_pdbqts[0])}, Last: {os.path.basename(all_pdbqts[-1])}")

t0 = time.time()
r = subprocess.run(
    [vina_bin,
     '--receptor', receptor_pdbqt,
     '--batch'] + all_pdbqts + [
     '--dir', results_dir,
     '--center_x', '30.0', '--center_y', '3.4', '--center_z', '-24.8',
     '--size_x', '25', '--size_y', '25', '--size_z', '25',
     '--exhaustiveness', '8',
     '--num_modes', '5',
     '--energy_range', '3',
     '--verbosity', '1'
    ],
    capture_output=True, text=True, timeout=800
)
elapsed = time.time() - t0
print(f"Done in {elapsed:.0f}s, RC={r.returncode}")
print("STDOUT tail:", r.stdout[-800:])
if r.stderr:
    print("STDERR:", r.stderr[:200])
