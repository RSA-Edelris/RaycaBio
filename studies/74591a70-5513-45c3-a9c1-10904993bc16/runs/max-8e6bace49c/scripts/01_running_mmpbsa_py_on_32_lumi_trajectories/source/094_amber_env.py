
import shutil, subprocess, os, json, time
from pathlib import Path

WORK      = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
AMBER_BIN = f"{AMBERHOME}/bin"
MMDIR     = f"{WORK}/mmgbsa"
TRAJ_DIR  = f"{WORK}/md_traj"

def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None); env.pop("PYTHONHOME", None)
    env["AMBERHOME"] = AMBERHOME
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd,
                       capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n"
                           f"STDOUT: {r.stdout[-1500:]}\nSTDERR: {r.stderr[-1500:]}")
    return r

# Install trajectories
installed = 0
for nc_file in sorted(Path(TRAJ_DIR).glob("*_md.nc")):
    dir_name = nc_file.stem.replace("_md", "")
    dest = Path(MMDIR) / dir_name / "md.nc"
    dest.parent.mkdir(exist_ok=True)
    shutil.copy(nc_file, dest)
    installed += 1

nc_files = sorted(Path(MMDIR).glob("*_ent/md.nc"))
sizes = [f.stat().st_size for f in nc_files]
print(f"Installed {installed} → {len(nc_files)} in mmgbsa/  |  "
      f"min={min(sizes)//1024}kB  max={max(sizes)//1024}kB")
