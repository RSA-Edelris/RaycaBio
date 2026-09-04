
import subprocess, os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
prot_sdf = os.path.join(wd, "all_protonated_3d.sdf")

# Split multi-mol SDF into individual SDF files, then convert each to PDBQT
# Use obabel to split: obabel -isdf multi.sdf -osdf -O lig.sdf -m (makes lig001.sdf, lig002.sdf...)
# Then per-file: obabel lig001.sdf -O lig001.pdbqt --partialcharge gasteiger

# First split
r = subprocess.run(
    ['/usr/bin/obabel', prot_sdf, '-osdf', '-O', os.path.join(ligands_dir, 'lig.sdf'), '-m'],
    capture_output=True, text=True, cwd=ligands_dir
)
print("Split RC:", r.returncode)
print(r.stderr[:300])

# Count output files
sdfs = sorted([f for f in os.listdir(ligands_dir) if f.endswith('.sdf')])
print(f"Individual SDF files: {len(sdfs)}")
print("First 5:", sdfs[:5])
