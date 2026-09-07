
import subprocess, os, json, shutil
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

def prepare_ligand(name):
    """antechamber (-c gas) + parmchk2 + tleap for one ligand."""
    d = Path(MMDIR) / f"{name}_ent"
    d.mkdir(exist_ok=True)
    sdf = f"{WORK}/best_poses/{name}_pose1.sdf"
    mol2 = d / "lig.mol2"
    frcmod = d / "lig.frcmod"

    # antechamber with Gasteiger charges (no sqm, no odd-electron issue)
    if not mol2.exists():
        run([f"{AMBER}/antechamber",
             "-i", sdf, "-fi", "sdf",
             "-o", str(mol2), "-fo", "mol2",
             "-c", "gas",       # Gasteiger — bypasses sqm
             "-at", "gaff2",
             "-rn", "LIG",
             "-pf", "y"],
            cwd=str(d))

    # parmchk2 for missing parameters
    if not frcmod.exists():
        run([f"{AMBER}/parmchk2",
             "-i", str(mol2), "-f", "mol2",
             "-o", str(frcmod),
             "-s", "gaff2"],
            cwd=str(d))

    return mol2, frcmod

def build_topology(name):
    """tleap: combine receptor + ligand into complex prmtop/inpcrd."""
    d = Path(MMDIR) / f"{name}_ent"
    mol2   = d / "lig.mol2"
    frcmod = d / "lig.frcmod"
    rec_nozn = f"{MMDIR}/receptor_nozn.pdb"

    cpx_top = d / "complex.prmtop"
    cpx_crd = d / "complex.inpcrd"
    rec_top = d / "rec.prmtop"
    rec_crd = d / "rec.inpcrd"
    lig_top = d / "lig.prmtop"
    lig_crd = d / "lig.inpcrd"

    if cpx_top.exists() and rec_top.exists() and lig_top.exists():
        return  # already done

    tleap_in = f"""
source leaprc.protein.ff14SB
source leaprc.gaff2
loadamberparams {frcmod}
LIG = loadmol2 {mol2}
REC = loadpdb {rec_nozn}
CPX = combine {{REC LIG}}
saveamberparm CPX {cpx_top} {cpx_crd}
saveamberparm REC {rec_top} {rec_crd}
saveamberparm LIG {lig_top} {lig_crd}
quit
"""
    tleap_file = d / "tleap.in"
    tleap_file.write_text(tleap_in)
    run([f"{AMBER}/tleap", "-f", str(tleap_file)], cwd=str(d))

# Sander input templates
MIN_IN = """\
Minimization
 &cntrl
  imin=1, maxcyc=500, ncyc=200,
  ntb=0, cut=12.0,
  igb=5, saltcon=0.10,
  ntpr=100,
 /
"""

MD_IN = """\
NVT MD
 &cntrl
  imin=0, nstlim=10000, dt=0.002,
  ntb=0, cut=12.0,
  igb=5, saltcon=0.10,
  tempi=300.0, temp0=300.0,
  ntt=3, gamma_ln=2.0,
  ntc=2, ntf=2,
  ntpr=1000, ntwx=200,
  ioutfm=1,
 /
"""

MMGBSA_IN = """\
MM-GBSA
 &general
  startframe=1, endframe=50, interval=1,
 /
 &gb
  igb=5, saltcon=0.10, intdiel=1.0, extdiel=78.5,
 /
"""

def run_min(name):
    d = Path(MMDIR) / f"{name}_ent"
    min_rst = d / "min.rst7"
    if min_rst.exists() and min_rst.stat().st_size > 10000:
        return  # already done
    (d / "min.in").write_text(MIN_IN)
    run([f"{AMBER}/sander",
         "-O", "-i", "min.in",
         "-o", "min.out",
         "-p", "complex.prmtop",
         "-c", "complex.inpcrd",
         "-r", "min.rst7",
         "-ref", "complex.inpcrd"],
        cwd=str(d))

def run_md(name):
    d = Path(MMDIR) / f"{name}_ent"
    md_nc = d / "md.nc"
    if md_nc.exists() and md_nc.stat().st_size > 100000:
        return  # already done
    (d / "md.in").write_text(MD_IN)
    run([f"{AMBER}/sander",
         "-O", "-i", "md.in",
         "-o", "md.out",
         "-p", "complex.prmtop",
         "-c", "min.rst7",
         "-r", "md.rst7",
         "-x", "md.nc",
         "-ref", "min.rst7"],
        cwd=str(d))

def run_mmpbsa(name):
    d = Path(MMDIR) / f"{name}_ent"
    out_file = d / "FINAL_RESULTS_MMPBSA.dat"
    if out_file.exists():
        return
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

def parse_mmpbsa(name):
    dat = Path(MMDIR) / f"{name}_ent" / "FINAL_RESULTS_MMPBSA.dat"
    if not dat.exists():
        return None
    text = dat.read_text()
    result = {}
    for line in text.split("\n"):
        for key in ["DELTA G binding", "VDWAALS", "EEL", "EGB", "ESURF"]:
            if line.strip().startswith(key):
                parts = line.split()
                try:
                    result[key] = float(parts[-3])   # mean
                    result[key+"_std"] = float(parts[-1])
                except (IndexError, ValueError):
                    pass
    return result if result else None

if __name__ == "__main__":
    print("Pipeline module loaded OK")
