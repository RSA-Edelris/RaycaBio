
# Check first 30 lines of one SDF to see if H atoms are explicit or implicit
sdf = f"{WORK}/best_poses/EDEL-CRBN-0001_pose1.sdf"
lines = Path(sdf).read_text().split("\n")
for i, l in enumerate(lines[:35]):
    print(f"{i:3d}: {l}")
