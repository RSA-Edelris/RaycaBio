
import os

d = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/mmgbsa_EDS01806218_ent2"
content = open(f"{d}/mmgbsa_result.dat").read()
for line in content.splitlines():
    if "DELTA TOTAL" in line:
        print("Single-frame MM-GBSA:", line.strip())
        break

import json
fr = json.load(open("/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/final_results.json"))
print("\nfinal_results.json:")
for k,v in fr.items():
    if "ent2" in k.lower() or "EDS01806218" in k:
        print(f"  {k}: {v}")
