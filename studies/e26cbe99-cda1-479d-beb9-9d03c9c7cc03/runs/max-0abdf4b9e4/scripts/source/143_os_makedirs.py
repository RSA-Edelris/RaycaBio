
import os, shutil

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
STAGE = f"{BASE}/abfe_stage"
os.makedirs(STAGE, exist_ok=True)

# Copy all ABFE input files to a flat staging area with compound-prefixed names
# so each compound's files are uniquely named and all at the top level

names = ["EDS01806218_ent1", "EDS01806218_ent2", "EDS01889984"]
staged = {}  # name -> {leg -> list of (staged_name, original_path)}

for name in names:
    d = f"md_{name}"
    staged[name] = {"complex": [], "solvent": []}

    # --- Complex leg files ---
    # start.gro
    src = f"{BASE}/{d}/abfe_start.gro"
    dst_name = f"{name}_abfe_start.gro"
    shutil.copy2(src, f"{STAGE}/{dst_name}")
    staged[name]["complex"].append((dst_name, src))

    # topology
    src = f"{BASE}/{d}/complex_abfe.top"
    dst_name = f"{name}_complex_abfe.top"
    shutil.copy2(src, f"{STAGE}/{dst_name}")
    staged[name]["complex"].append((dst_name, src))

    # index
    src = f"{BASE}/{d}/index.ndx"
    dst_name = f"{name}_index.ndx"
    shutil.copy2(src, f"{STAGE}/{dst_name}")
    staged[name]["complex"].append((dst_name, src))

    # 17 complex MDPs
    for w in range(17):
        src = f"{BASE}/{d}/abfe_complex_mdps/win{w:02d}.mdp"
        dst_name = f"{name}_cplx_win{w:02d}.mdp"
        shutil.copy2(src, f"{STAGE}/{dst_name}")
        staged[name]["complex"].append((dst_name, src))

    # --- Solvent leg files ---
    src = f"{BASE}/{d}/abfe_solv/lig_solv.gro"
    dst_name = f"{name}_lig_solv.gro"
    shutil.copy2(src, f"{STAGE}/{dst_name}")
    staged[name]["solvent"].append((dst_name, src))

    src = f"{BASE}/{d}/abfe_solv/lig_solv.top"
    dst_name = f"{name}_lig_solv.top"
    shutil.copy2(src, f"{STAGE}/{dst_name}")
    staged[name]["solvent"].append((dst_name, src))

    for w in range(17):
        src = f"{BASE}/{d}/abfe_solvent_mdps/win{w:02d}.mdp"
        dst_name = f"{name}_solv_win{w:02d}.mdp"
        shutil.copy2(src, f"{STAGE}/{dst_name}")
        staged[name]["solvent"].append((dst_name, src))

# Summary
for name in names:
    nc = len(staged[name]["complex"])
    ns = len(staged[name]["solvent"])
    print(f"{name}: {nc} complex files, {ns} solvent files")

print(f"\nAll files staged in: {STAGE}")
print(f"Total files: {sum(len(staged[n]['complex']) + len(staged[n]['solvent']) for n in names)}")
