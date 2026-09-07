
import subprocess, os

MD = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/md_EDS01806218_ent2"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"

print("=== Step 1: cpptraj strip ===")
r = subprocess.run(
    [f"{AMBERHOME}/bin/cpptraj", "-i", f"{MD}/cpptraj_strip.in"],
    capture_output=True, text=True, timeout=300
)
print(r.stdout[-3000:] if len(r.stdout) > 3000 else r.stdout)
if r.returncode != 0:
    print("STDERR:", r.stderr[-2000:])
    raise RuntimeError(f"cpptraj failed (rc={r.returncode})")

nc = f"{MD}/prod_nowater.nc"
size = os.path.getsize(nc) if os.path.exists(nc) else 0
print(f"\nprod_nowater.nc: {size/1e6:.1f} MB — {'OK' if size > 0 else 'MISSING'}")
