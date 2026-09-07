
# Confirm report path and write the phase document
import os
ART = "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777"
print(os.path.exists(f"{ART}/PDK1_docking_campaign_final_report.md"))
print(os.path.exists(f"{ART}/full_docking_gbsa_table.csv"))
print(os.path.exists(f"{ART}/interactions_best_poses.json"))
