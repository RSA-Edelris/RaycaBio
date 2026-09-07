
import subprocess, os, json, time
from pathlib import Path

WORK      = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
AMBER_BIN = f"{AMBERHOME}/bin"
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
    env.pop("PYTHONPATH", None); env.pop("PYTHONHOME", None)
    env["AMBERHOME"] = AMBERHOME
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd,
                       capture_output=True, text=True, env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(f"FAILED: {' '.join(str(c) for c in cmd)}\n"
                           f"STDOUT: {r.stdout[-2000:]}\nSTDERR: {r.stderr[-2000:]}")
    return r

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
        for key in ["VDWAALS", "EEL", "EGB", "ESURF",
                    "DELTA G gas", "DELTA G solv", "DELTA TOTAL"]:
            if s.startswith(key):
                parts = s.split()
                try:
                    result[key]        = float(parts[-3])
                    result[key+"_std"] = float(parts[-1])
                except (IndexError, ValueError):
                    pass
    return result if result else None

def run_mmpbsa_one(d):
    d = Path(d)
    out_file = d / "FINAL_RESULTS_MMPBSA.dat"
    if out_file.exists():
        return parse_mmpbsa(d)
    (d / "mmgbsa.in").write_text(MMGBSA_IN)
    for p in list(d.glob("_MMPBSA_*")) + list(d.glob("reference.frc")):
        p.unlink(missing_ok=True)
    run([f"{AMBER_BIN}/MMPBSA.py", "-O",
         "-i",  str(d / "mmgbsa.in"),
         "-o",  str(out_file),
         "-cp", str(d / "complex.prmtop"),
         "-rp", str(d / "rec.prmtop"),
         "-lp", str(d / "lig.prmtop"),
         "-y",  str(d / "md.nc")],
        cwd=str(d))
    return parse_mmpbsa(d)

# Load compound list
with open(f"{WORK}/docking_scores_all32.json") as fh:
    scores = json.load(fh)
names = list(scores.keys())
compound_dirs = [f"{name}_ent" for name in names]

print(f"Running MMPBSA.py for {len(names)} compounds...")
results = {}
ok, fail = [], []
t_total = time.time()

for name, cdir in zip(names, compound_dirs):
    d = Path(MMDIR) / cdir
    t0 = time.time()
    try:
        r = run_mmpbsa_one(d)
        elapsed = time.time() - t0
        if r:
            results[name] = r
            ok.append(name)
            dg  = r.get("DELTA TOTAL", float("nan"))
            std = r.get("DELTA TOTAL_std", float("nan"))
            print(f"  OK  {name:<30}  ΔG={dg:>8.2f} ±{std:.2f}  ({elapsed:.0f}s)")
        else:
            fail.append(name)
            print(f"  FAIL {name}: parse None  ({elapsed:.0f}s)")
    except Exception as e:
        fail.append(name)
        print(f"  FAIL {name}: {str(e)[:120]}")

total_t = time.time() - t_total
print(f"\n{'='*60}")
print(f"Done: {len(ok)}/32 OK, {len(fail)} failed  |  total={total_t/60:.1f} min")

# Save
with open(f"{MMDIR}/mmgbsa_results.json", "w") as fh:
    json.dump(results, fh, indent=2)
print(f"Saved → mmgbsa/mmgbsa_results.json")
