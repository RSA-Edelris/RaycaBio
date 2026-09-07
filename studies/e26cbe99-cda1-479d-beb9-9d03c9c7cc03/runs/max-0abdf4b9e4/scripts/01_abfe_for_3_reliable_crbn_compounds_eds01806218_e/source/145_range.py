
import os, glob

session = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

compounds = ["EDS01806218_ent1", "EDS01806218_ent2", "EDS01889984"]

n_fixed = 0
for cname in compounds:
    for leg in ["cplx", "solv"]:
        for w in range(17):
            mdp_path = os.path.join(session, f"{cname}_{leg}_win{w:02d}.mdp")
            if not os.path.exists(mdp_path):
                print(f"MISSING: {mdp_path}")
                continue
            with open(mdp_path, "r") as f:
                content = f.read()
            orig = content
            content = content.replace("rcoulomb             = 1.0", "rcoulomb             = 1.2")
            content = content.replace("rvdw                 = 1.0", "rvdw                 = 1.2")
            if content != orig:
                with open(mdp_path, "w") as f:
                    f.write(content)
                n_fixed += 1

print(f"Fixed rcoulomb/rvdw in {n_fixed} MDP files")

# Verify one file
with open(os.path.join(session, "EDS01806218_ent1_solv_win00.mdp")) as f:
    for line in f:
        if "rcoulomb" in line or "rvdw" in line:
            print("  ", line.rstrip())
