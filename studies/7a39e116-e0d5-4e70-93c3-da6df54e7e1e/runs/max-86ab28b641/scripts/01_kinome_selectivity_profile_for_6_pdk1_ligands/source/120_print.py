
import os
print("Workspace:", WS)
print("AGC results rows:", len(df_agc))
# What keys does kinasedocker2 accept?
# Try a micro-test call with just CDK2 named explicitly
# First verify the output already on disk
import glob
existing = glob.glob(f"{WS}/kd2_out/**/docking_results/*.csv", recursive=True)
for f in existing:
    print(os.path.getsize(f), f)
