
import subprocess, os

session = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

compounds = [
    ("EDS01357518_ent1", f"{session}/npt_prod.6300385.xtc"),
    ("EDS01889984",      f"{session}/npt_prod.6304913.xtc"),
]

for comp, xtc in compounds:
    md_dir = f"{session}/md_{comp}"
    strip_in = f"{md_dir}/cpptraj_strip.in"
    nc_out   = f"{md_dir}/prod_nowater.nc"
    prmtop   = f"{md_dir}/complex.prmtop"

    cpptraj_script = f"""parm {prmtop}
trajin {xtc}
strip :WAT,Cl-
trajout {nc_out} netcdf
run
"""
    with open(strip_in, "w") as f:
        f.write(cpptraj_script)

    print(f"\n{'='*50}")
    print(f"cpptraj strip: {comp}")
    r = subprocess.run(["cpptraj", "-i", strip_in], capture_output=True, text=True)
    print(r.stdout[-2000:] if len(r.stdout) > 2000 else r.stdout)
    if r.returncode != 0:
        print("STDERR:", r.stderr[-500:])
    else:
        size_mb = os.path.getsize(nc_out) / 1e6
        print(f"  -> {nc_out}: {size_mb:.1f} MB")
