
import subprocess, os, textwrap

SESSION = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

compounds = {
    "EDS01806218_ent1": {
        "xtc": f"{SESSION}/npt_prod_EDS01806218_ent1.xtc",
        "md_dir": f"{SESSION}/md_EDS01806218_ent1",
    },
    "EDS01357518_ent2": {
        "xtc": f"{SESSION}/npt_prod.6309346.xtc",
        "md_dir": f"{SESSION}/md_EDS01357518_ent2",
    },
}

for name, cfg in compounds.items():
    nc = f"{cfg['md_dir']}/prod_nowater.nc"
    if os.path.exists(nc):
        print(f"{name}: stripped trajectory already exists ({os.path.getsize(nc)/1e6:.1f} MB), skipping cpptraj")
        continue

    script = textwrap.dedent(f"""\
        parm {cfg['md_dir']}/complex.prmtop
        trajin {cfg['xtc']}
        strip :WAT,Cl-
        trajout {nc} netcdf
        run
        quit
    """)
    inp_path = f"{cfg['md_dir']}/cpptraj_strip.in"
    with open(inp_path, "w") as f:
        f.write(script)

    print(f"\n--- cpptraj strip: {name} ---")
    r = subprocess.run(["cpptraj", "-i", inp_path], capture_output=True, text=True)
    for line in (r.stdout + r.stderr).splitlines():
        if any(k in line.lower() for k in ["read", "processed", "frames", "error", "warning", "written"]):
            print(line)
    print("Return code:", r.returncode)
    if r.returncode == 0 and os.path.exists(nc):
        print(f"  -> written ({os.path.getsize(nc)/1e6:.1f} MB)")
    else:
        print("STDOUT:", r.stdout[-3000:])
        print("STDERR:", r.stderr[-1000:])
