
import os, re

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Fix solvent MDPs: replace tc-grps = LIG Water_and_ions → System (single thermostat)
print("=== Fixing solvent MDP tc-grps ===")
for name in BP:
    solv_mdp_dir = f"{BASE}/md_{name}/abfe_solv_mdps"
    count = 0
    for fn in sorted(os.listdir(solv_mdp_dir)):
        if not fn.endswith(".mdp"):
            continue
        fpath = f"{solv_mdp_dir}/{fn}"
        with open(fpath) as f:
            content = f.read()
        new = re.sub(
            r"tc-grps\s*=\s*LIG Water_and_ions",
            "tc-grps              = System",
            content)
        new = re.sub(
            r"tau_t\s*=\s*0\.1\s+0\.1",
            "tau_t                = 0.1",
            new)
        new = re.sub(
            r"ref_t\s*=\s*300\s+300",
            "ref_t                = 300",
            new)
        with open(fpath, "w") as f:
            f.write(new)
        count += 1
    print(f"  {name}: {count} solvent MDPs updated")

print("\n=== Verify fix on one file ===")
test = f"{BASE}/md_EDS01806218_ent1/abfe_solv_mdps/win00.mdp"
for line in open(test):
    if any(k in line for k in ("tc-grps", "tau_t", "ref_t")):
        print(" ", line.rstrip())
