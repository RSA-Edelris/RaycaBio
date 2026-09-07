
import os, glob

session = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
compounds = ["EDS01806218_ent1", "EDS01806218_ent2", "EDS01889984"]

n_fixed = 0
for cname in compounds:
    for leg in ["cplx", "solv"]:
        for w in range(17):
            mdp_path = os.path.join(session, f"{cname}_{leg}_win{w:02d}.mdp")
            if not os.path.exists(mdp_path):
                continue
            with open(mdp_path) as f:
                content = f.read()
            orig = content
            content = content.replace("couple-intramol      = no", "couple-intramol      = yes")
            if content != orig:
                with open(mdp_path, "w") as f:
                    f.write(content)
                n_fixed += 1

print(f"Changed couple-intramol in {n_fixed} files")

# Verify
with open(os.path.join(session, "EDS01806218_ent1_solv_win00.mdp")) as f:
    for line in f:
        if "couple-intramol" in line:
            print("  ", line.rstrip())
with open(os.path.join(session, "EDS01889984_cplx_win08.mdp")) as f:
    for line in f:
        if "couple-intramol" in line or "rcoulomb" in line or "rvdw " in line:
            print("  ", line.rstrip())
