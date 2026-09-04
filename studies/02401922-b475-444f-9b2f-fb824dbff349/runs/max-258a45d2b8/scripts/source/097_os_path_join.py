
import os

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
log_path = os.path.join(wd, "mmgbsa_run.log")

with open(log_path) as f:
    content = f.read()
print(content[-1500:])
