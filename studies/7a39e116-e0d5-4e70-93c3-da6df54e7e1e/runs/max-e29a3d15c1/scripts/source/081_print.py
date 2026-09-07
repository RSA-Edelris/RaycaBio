
import os, json

ART = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"

pose_file = f"{ART}/all_poses/EL2003A_pose2.sdf"
recep_file = f"{ART}/1Z5M_receptor_pH7.4.pdb"

print("Pose file exists:", os.path.exists(pose_file))
print("Receptor exists:", os.path.exists(recep_file))

# File sizes
print(f"Pose size:     {os.path.getsize(pose_file):,} bytes")
print(f"Receptor size: {os.path.getsize(recep_file):,} bytes")
