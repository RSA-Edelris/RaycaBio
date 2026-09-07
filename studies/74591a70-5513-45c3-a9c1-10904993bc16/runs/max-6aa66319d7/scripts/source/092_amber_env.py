
updated_mmpbsa_script = r'''#!/usr/bin/env python3
"""
Run MMPBSA.py for all 32 compounds. Call after LUMI trajectories are installed.
Usage:
  python run_mmpbsa.py                     # run analysis
  python run_mmpbsa.py --install <traj_dir> # copy md.nc files first
"""
import subprocess, os, json, re, shutil
from pathlib import Path

WORK      = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER     = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
MMDIR     = f"{WORK}/mmgbsa"

MMGBSA_IN = """\
MM-GBSA single-trajectory
 &general
  startframe=1, endframe=50, interval=1,
 /
 &gb
  igb=5, saltcon=0.10,
 /
"""

def amber_env():
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    env["AMBERHOME"] = AMBERHOME
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd],
                       cwd=cwd, capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(
            f"FAILED: {' '.join(str(c) for c in cmd)}\n"
            f"STDOUT: {r.stdout[-2000:]}\nSTDERR: {r.stderr[-2000:]}")
    return r

def run_mmpbsa(d):
    d = Path(d)
    out_file = d / "FINAL_RESULTS_MMPBSA.dat"
    if out_file.exists():
        return parse_mmpbsa(d)
    (d / "mmgbsa.in").write_text(MMGBSA_IN)
    # Clean any leftover temp files from prior failed runs
    for p in list(d.glob("_MMPBSA_*")) + list(d.glob("reference.frc")):
        p.unlink(missing_ok=True)
    run([f"{AMBER}/MMPBSA.py",
         "-O",
         "-i",  str(d / "mmgbsa.in"),
         "-o",  str(out_file),
         "-cp", str(d / "complex.prmtop"),
         "-rp", str(d / "rec.prmtop"),
         "-lp", str(d / "lig.prmtop"),
         "-y",  str(d / "md.nc")],
        cwd=str(d))
    return parse_mmpbsa(d)

def parse_mmpbsa(d):
    dat = Path(d) / "FINAL_RESULTS_MMPBSA.dat"
    if not dat.exists():
        return None
    text = dat.read_text()
    result = {}
    in_diff = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("Differences"):
            in_diff = True
        if not in_diff:
            continue
        for key in ["VDWAALS", "EEL", "EGB", "ESURF", "DELTA G gas", "DELTA G solv", "DELTA TOTAL"]:
            if s.startswith(key):
                parts = s.split()
                try:
                    result[key] = float(parts[-3])
                    result[key + "_std"] = float(parts[-1])
                except (IndexError, ValueError):
                    pass
    return result if result else None

def install_trajectories(traj_dir):
    """Copy *_md.nc files from traj_dir into their compound directories."""
    traj_dir = Path(traj_dir)
    installed = 0
    for nc_file in sorted(traj_dir.glob("*_md.nc")):
        dir_name = nc_file.stem.replace("_md", "")
        dest = Path(MMDIR) / dir_name / "md.nc"
        if not dest.exists():
            dest.parent.mkdir(exist_ok=True)
            shutil.copy(nc_file, dest)
            print(f"  Installed {dir_name}/md.nc ({nc_file.stat().st_size//1024} kB)")
            installed += 1
        else:
            print(f"  Skip {dir_name}/md.nc (already present)")
    return installed

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        n = install_trajectories(sys.argv[2])
        print(f"Installed {n} trajectories")

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
                dg  = r.get("DELTA TOTAL", float("nan"))
                std = r.get("DELTA TOTAL_std", float("nan"))
                print(f"  OK   {name:<30}  ΔG = {dg:>8.2f} ± {std:.2f} kcal/mol")
            else:
                fail.append(name)
                print(f"  FAIL {name}: parse returned None")
        except Exception as e:
            fail.append(name)
            print(f"  FAIL {name}: {e}")

    print(f"\nDone: {len(ok)} OK, {len(skip)} skipped (no traj), {len(fail)} failed")
    out = f"{MMDIR}/mmgbsa_results.json"
    with open(out, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"Results saved to {out}")
'''

with open(f"{MMDIR}/run_mmpbsa.py", "w") as fh:
    fh.write(updated_mmpbsa_script)
print("run_mmpbsa.py updated with all fixes")
print("Fixes: AMBERHOME, -cp flag, absolute paths, DELTA TOTAL parsing, _MMPBSA_* cleanup")
