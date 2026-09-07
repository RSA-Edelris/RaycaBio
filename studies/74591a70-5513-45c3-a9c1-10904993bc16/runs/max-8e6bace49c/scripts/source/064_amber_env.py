
pipeline_code = r'''
import subprocess, os, shutil, json, re
from pathlib import Path

WORK  = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
MMDIR = f"{WORK}/mmgbsa"

def amber_env():
    """Return os.environ with PYTHONPATH/PYTHONHOME stripped — prevents
    session numpy (cpython-312) from being injected into Python-3.14 tools."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    return env

def run(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       env=amber_env())
    if check and r.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(str(c) for c in cmd)}\n"
            f"STDOUT: {r.stdout[-2000:]}\nSTDERR: {r.stderr[-2000:]}")
    return r

# ── Step 0: prepare receptor once ────────────────────────────────────────────
def prepare_receptor():
    out = f"{MMDIR}/receptor_amber.pdb"
    if Path(out).exists():
        print("Receptor already prepared.")
        return out
    r = run([f"{AMBER}/pdb4amber",
             "-i", f"{WORK}/4CI2_receptor_noh.pdb",
             "-o", out,
             "--no-reduce"],
            cwd=MMDIR)
    print("pdb4amber:", r.stderr[-400:] if r.stderr else "ok")
    print(f"Receptor written: {Path(out).stat().st_size} bytes")
    return out

# ── Step 1: antechamber ───────────────────────────────────────────────────────
def run_antechamber(name, lig_dir):
    mol2 = f"{lig_dir}/lig.mol2"
    if Path(mol2).exists():
        print(f"  [{name}] mol2 exists, skip")
        return mol2
    sdf = f"{WORK}/best_poses/{name}_pose1.sdf"
    run([f"{AMBER}/antechamber",
         "-i", sdf, "-fi", "sdf",
         "-o", mol2, "-fo", "mol2",
         "-c", "bcc", "-s", "2",
         "-at", "gaff2", "-nc", "0",
         "-m", "1", "-rn", "LIG"],
        cwd=lig_dir)
    print(f"  [{name}] antechamber done ({Path(mol2).stat().st_size} B)")
    return mol2

# ── Step 2: parmchk2 ──────────────────────────────────────────────────────────
def run_parmchk2(name, lig_dir):
    frcmod = f"{lig_dir}/lig.frcmod"
    if Path(frcmod).exists():
        return frcmod
    run([f"{AMBER}/parmchk2",
         "-i", f"{lig_dir}/lig.mol2", "-f", "mol2",
         "-o", frcmod, "-a", "Y"],
        cwd=lig_dir)
    print(f"  [{name}] parmchk2 done")
    return frcmod

# ── Step 3: tleap ─────────────────────────────────────────────────────────────
def run_tleap(name, lig_dir, rec_pdb):
    cpx_top = f"{lig_dir}/complex.prmtop"
    if Path(cpx_top).exists():
        print(f"  [{name}] topology exists, skip")
        return
    tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
loadamberparams frcmod.ionsjc_tip3p
LIG = loadmol2 {lig_dir}/lig.mol2
loadamberparams {lig_dir}/lig.frcmod
REC = loadpdb {rec_pdb}
COMPLEX = combine {{REC LIG}}
check COMPLEX
saveamberparm LIG {lig_dir}/lig.prmtop {lig_dir}/lig.inpcrd
saveamberparm REC {lig_dir}/rec.prmtop {lig_dir}/rec.inpcrd
saveamberparm COMPLEX {lig_dir}/complex.prmtop {lig_dir}/complex.inpcrd
quit
"""
    inp = f"{lig_dir}/tleap.in"
    Path(inp).write_text(tleap_in)
    r = run([f"{AMBER}/tleap", "-f", inp], cwd=lig_dir)
    print(f"  [{name}] tleap done ({Path(cpx_top).stat().st_size} B)")
    if "FATAL" in r.stderr or "FATAL" in r.stdout:
        raise RuntimeError(f"tleap FATAL: {r.stderr[-1000:]}")

# ── Step 4: minimisation ──────────────────────────────────────────────────────
MIN_IN = """\
Energy minimization in GB implicit solvent
 &cntrl
  imin=1, maxcyc=2000, ncyc=500,
  ntb=0, cut=999.0,
  igb=5, saltcon=0.10,
  ntpr=200, ntwx=0,
 /
"""
def run_min(name, lig_dir):
    rst = f"{lig_dir}/min.rst7"
    if Path(rst).exists():
        return
    Path(f"{lig_dir}/min.in").write_text(MIN_IN)
    run([f"{AMBER}/sander",
         "-O", "-i", "min.in", "-o", "min.out",
         "-p", "complex.prmtop", "-c", "complex.inpcrd", "-r", "min.rst7"],
        cwd=lig_dir)
    print(f"  [{name}] minimisation done")

# ── Step 5: 100 ps NVT in igb=5 ──────────────────────────────────────────────
MD_IN = """\
NVT MD GB implicit solvent 100ps
 &cntrl
  imin=0, irest=0, ntx=1,
  nstlim=50000, dt=0.002,
  ntb=0, cut=999.0,
  igb=5, saltcon=0.10,
  tempi=300.0, temp0=300.0,
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntpr=5000, ntwx=1000, ntwe=0,
  iwrap=0, ioutfm=1,
 /
"""
def run_md(name, lig_dir):
    traj = f"{lig_dir}/md.nc"
    if Path(traj).exists():
        return
    Path(f"{lig_dir}/md.in").write_text(MD_IN)
    run([f"{AMBER}/sander",
         "-O", "-i", "md.in", "-o", "md.out",
         "-p", "complex.prmtop", "-c", "min.rst7",
         "-r", "md.rst7", "-x", "md.nc", "-e", "md.en"],
        cwd=lig_dir)
    print(f"  [{name}] MD done ({Path(traj).stat().st_size} B)")

# ── Step 6: MMPBSA.py ─────────────────────────────────────────────────────────
MMGBSA_IN = """\
Single-trajectory GB MM-GBSA, neutral congeneric, igb=5
 &general
  startframe=1, endframe=50, interval=1,
  keep_files=0, verbose=1,
 /
 &gb
  igb=5, saltcon=0.10,
  intdiel=1.0, extdiel=78.5,
 /
"""
def run_mmpbsa(name, lig_dir):
    result_file = f"{lig_dir}/FINAL_RESULTS_MMPBSA.dat"
    if not Path(result_file).exists():
        Path(f"{lig_dir}/mmgbsa.in").write_text(MMGBSA_IN)
        run([f"{AMBER}/MMPBSA.py",
             "-O", "-i", "mmgbsa.in",
             "-o", "FINAL_RESULTS_MMPBSA.dat",
             "-sp", "complex.prmtop",
             "-rp", "rec.prmtop",
             "-lp", "lig.prmtop",
             "-y", "md.nc"],
            cwd=lig_dir)
        print(f"  [{name}] MMPBSA.py done")
    return parse_mmpbsa(result_file)

def parse_mmpbsa(path):
    text = Path(path).read_text()
    # Find the DELTA Total line in FINAL_RESULTS_MMPBSA.dat
    # Format: TOTAL     mean     std     std_err
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("TOTAL") and not s.startswith("TOTAL ENTROPY"):
            parts = s.split()
            if len(parts) >= 4:
                try:
                    return {"MMGBSA_dG": float(parts[1]),
                            "MMGBSA_std": float(parts[2])}
                except ValueError:
                    pass
    # Fallback: grep for DELTA section
    m = re.search(r"DELTA.*?TOTAL\s+([-\d.]+)\s+([-\d.]+)", text, re.DOTALL)
    if m:
        return {"MMGBSA_dG": float(m.group(1)), "MMGBSA_std": float(m.group(2))}
    return {"MMGBSA_dG": None, "MMGBSA_std": None, "raw": text[-800:]}

# ── Full pipeline for one ligand ──────────────────────────────────────────────
def run_one(name, rec_pdb):
    lig_dir = f"{MMDIR}/{name}"
    os.makedirs(lig_dir, exist_ok=True)
    print(f"\n=== {name} ===")
    run_antechamber(name, lig_dir)
    run_parmchk2(name, lig_dir)
    run_tleap(name, lig_dir, rec_pdb)
    run_min(name, lig_dir)
    run_md(name, lig_dir)
    return run_mmpbsa(name, lig_dir)
'''

with open(f"{MMGBSA_DIR}/mmgbsa_pipeline.py", "w") as fh:
    fh.write(pipeline_code)
print("Pipeline updated.")

# Quick test: can pdb4amber run now with clean env?
import subprocess
clean_env = {k: v for k, v in os.environ.items()
             if k not in ("PYTHONPATH", "PYTHONHOME")}
r = subprocess.run([f"{AMBER}/pdb4amber", "--version"],
                   capture_output=True, text=True, env=clean_env)
print("pdb4amber version test:", r.stdout.strip() or r.stderr[:200])
