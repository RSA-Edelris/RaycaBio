
import os, subprocess

# Split the 8-compound SDF into individual files for GNINA
sdf_path = "/home/ubuntu/rayca-artifacts/eaff7adfa74be7523e4a94b7/files/CRBN_lig_results_2.sdf"
out_dir = "/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/docking/ligands"
os.makedirs(out_dir, exist_ok=True)

# Read and split SDF
with open(sdf_path) as f:
    content = f.read()

# Split on $$$$
blocks = [b.strip() for b in content.split("$$$$") if b.strip()]
print(f"Found {len(blocks)} compounds in SDF")

# Extract names and write individual files
for i, block in enumerate(blocks):
    lines = block.split('\n')
    # First line is the molecule name
    mol_name = lines[0].strip() if lines[0].strip() else f"compound_{i}"
    fname = f"{out_dir}/lig_{i:02d}_{mol_name.replace(' ','_')}.sdf"
    with open(fname, 'w') as f:
        f.write(block + "\n$$$$\n")
    print(f"  [{i}] {mol_name} -> {os.path.basename(fname)}")
