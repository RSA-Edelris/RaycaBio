
import os
cwd = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
for f in ["EL2003A_pose2_MD_final.sdf",
          "EL2003A_MD_trajectory.gif",
          "EL2003A_MD_final_frame.png",
          "EL2003A_MD_ligand_RMSD.png"]:
    path = f"{cwd}/{f}"
    sz = os.path.getsize(path) if os.path.exists(path) else 0
    print(f"{f}: {sz/1024:.1f} KB")
