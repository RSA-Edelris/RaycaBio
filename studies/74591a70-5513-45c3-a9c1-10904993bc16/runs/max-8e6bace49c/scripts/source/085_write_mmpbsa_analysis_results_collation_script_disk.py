
# Write the MMPBSA analysis + results collation script to disk
mmpbsa_script = r'''#!/usr/bin/env python3
"""
Run MMPBSA.py for all 32 compounds after LUMI trajectories return.
Expects md.nc files in {MMDIR}/{name}_ent/ or copied from LUMI.
"""
import subprocess, os, json, re
from pathlib import Path

WORK  = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
MMDIR = f"{WORK}/mmgbsa"

def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd],
                       cwd=cwd, capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(
            f"FAILED: {' '.join(str(c) for c in cmd)}\n"
            f"STDOUT: {r.stdout[-2000:]}\nSTDERR: {r.stderr[-2000:]}")
    return r

MMGBSA_IN = """\
MM-GBSA single-trajectory
 &general
  startframe=1, endframe=50, interval=1,
 /
 &gb
  igb=5, saltcon=0.10, intdiel=1.0, extdiel=78.5,
 /
"""

def run_mmpbsa(d):
    """Run MMPBSA.py in directory d. Returns parsed dict or None."""
    d = Path(d)
    out_file = d / "FINAL_RESULTS_MMPBSA.dat"
    if out_file.exists():
        print(f"  {d.name}: already done, parsing")
        return parse_mmpbsa(d)
    
    (d / "mmgbsa.in").write_text(MMGBSA_IN)
    run([f"{AMBER}/MMPBSA.py",
         "-O",
         "-i", "mmgbsa.in",
         "-o", "FINAL_RESULTS_MMPBSA.dat",
         "-sp", "complex.prmtop",
         "-rp", "rec.prmtop",
         "-lp", "lig.prmtop",
         "-y", "md.nc"],
        cwd=str(d))
    return parse_mmpbsa(d)

def parse_mmpbsa(d):
    dat = Path(d) / "FINAL_RESULTS_MMPBSA.dat"
    if not dat.exists():
        return None
    text = dat.read_text()
    result = {}
    for line in text.split("\n"):
        s = line.strip()
        for key in ["DELTA G binding", "VDWAALS", "EEL", "EGB", "ESURF"]:
            if s.startswith(key):
                parts = s.split()
                try:
                    idx = parts.index("=") + 1 if "=" in parts else 1
                    result[key] = float(parts[-3])
                    result[key + "_std"] = float(parts[-1])
                except (IndexError, ValueError):
                    pass
    return result if result else None

def install_trajectories(traj_dir):
    """Copy md.nc files from traj_dir to their compound directories."""
    traj_dir = Path(traj_dir)
    installed = 0
    for nc_file in traj_dir.glob("*_md.nc"):
        dir_name = nc_file.stem.replace("_md", "")
        dest = Path(MMDIR) / dir_name / "md.nc"
        if not dest.exists():
            import shutil
            dest.parent.mkdir(exist_ok=True)
            shutil.copy(nc_file, dest)
            print(f"  Installed {dir_name}/md.nc ({nc_file.stat().st_size//1024} kB)")
            installed += 1
    return installed

if __name__ == "__main__":
    import sys
    # Optional: install trajectories from a directory
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        traj_dir = sys.argv[2]
        n = install_trajectories(traj_dir)
        print(f"Installed {n} trajectories")

    # Run MMPBSA.py for all compounds that have md.nc
    with open(f"{WORK}/docking_scores_all32.json") as fh:
        scores = json.load(fh)
    names = list(scores.keys())
    compound_dirs = [f"{name}_ent" for name in names]
    
    results = {}
    ok, skip, fail = [], [], []
    for name, cdir in zip(names, compound_dirs):
        d = Path(MMDIR) / cdir
        nc = d / "md.nc"
        if not nc.exists():
            print(f"  SKIP {name}: no md.nc")
            skip.append(name)
            continue
        try:
            r = run_mmpbsa(d)
            if r:
                results[name] = r
                ok.append(name)
                print(f"  OK   {name:<28}  dG={r.get('DELTA G binding','?'):>8.2f} ± {r.get('DELTA G binding_std',0):.2f}")
            else:
                fail.append(name)
                print(f"  FAIL {name}: parse returned None")
        except Exception as e:
            fail.append(name)
            print(f"  FAIL {name}: {e}")

    print(f"\nDone: {len(ok)} OK, {len(skip)} skipped (no traj), {len(fail)} failed")
    
    # Save results
    out = f"{MMDIR}/mmgbsa_results.json"
    with open(out, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Results saved to {out}")
'''

with open(f"{MMDIR}/run_mmpbsa.py", "w") as fh:
    fh.write(mmpbsa_script)
print("run_mmpbsa.py written")

# Also verify MMPBSA.py is available locally
import subprocess, os
env = dict(os.environ); env.pop("PYTHONPATH", None); env.pop("PYTHONHOME", None)
r = subprocess.run([f"{AMBER}/MMPBSA.py", "--version"], capture_output=True, text=True, env=env)
print(f"MMPBSA.py version: {(r.stdout+r.stderr).strip()[:100]}")
