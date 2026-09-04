
import subprocess, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
results_dir = os.path.join(wd, "docking_results")
vina_bin = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/vina"
receptor_pdbqt = os.path.join(wd, "receptor.pdbqt")

# Check the PDBQT file for lig1
pdbqt1 = os.path.join(ligands_dir, "lig1.pdbqt")
print(f"lig1.pdbqt exists: {os.path.exists(pdbqt1)}, size: {os.path.getsize(pdbqt1) if os.path.exists(pdbqt1) else 0}")
if os.path.exists(pdbqt1):
    with open(pdbqt1) as f:
        content = f.read()
    print("First 400 chars:")
    print(content[:400])
    print("...")
    
# Also check if docking_results has any log files
logs = [f for f in os.listdir(results_dir) if f.endswith('.log')]
print(f"\nLog files in results: {len(logs)}")
if logs:
    with open(os.path.join(results_dir, logs[0])) as f:
        print(f"\n{logs[0]} content:")
        print(f.read()[:500])
