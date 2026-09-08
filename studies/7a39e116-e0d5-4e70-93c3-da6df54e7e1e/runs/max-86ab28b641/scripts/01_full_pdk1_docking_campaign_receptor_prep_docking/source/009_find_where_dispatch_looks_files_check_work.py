
import os
# Find where dispatch looks for files - check /work
print("os.getcwd():", os.getcwd())
print("/work exists:", os.path.exists("/work"))
if os.path.exists("/work"):
    print("/work contents:", os.listdir("/work")[:10])
print("workspace file exists:", os.path.exists(
    "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/1Z5M.pdb"))
print("Size:", os.path.getsize(
    "/home/ubuntu/rayca-sessions/7a39e116-e0d5-4e70-93c3-da6df54e7e1e-cacaa3ede777/1Z5M.pdb"))
