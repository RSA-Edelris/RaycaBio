
import os

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Verify all required files exist for each compound
names = ["EDS01806218_ent1", "EDS01806218_ent2", "EDS01889984"]

for name in names:
    d = f"md_{name}"
    checks = [
        f"{d}/abfe_start.gro",
        f"{d}/complex_abfe.top",
        f"{d}/index.ndx",
        f"{d}/abfe_solv/lig_solv.gro",
        f"{d}/abfe_solv/lig_solv.top",
    ]
    for w in range(17):
        checks.append(f"{d}/abfe_complex_mdps/win{w:02d}.mdp")
        checks.append(f"{d}/abfe_solvent_mdps/win{w:02d}.mdp")

    missing = []
    for c in checks:
        if not os.path.exists(f"{BASE}/{c}"):
            missing.append(c)
    
    if missing:
        print(f"MISSING for {name}:")
        for m in missing:
            print(f"  {m}")
    else:
        print(f"OK: {name} — all {len(checks)} files present")
