
import subprocess, os, json, time
from pathlib import Path

WORK  = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
MMDIR = f"{WORK}/mmgbsa"

with open(f"{WORK}/docking_scores_all32.json") as f:
    scores = json.load(f)
names = list(scores.keys())

rec_nozn = f"{MMDIR}/receptor_nozn.pdb"

def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0].split('/')[-1]} failed:\n{r.stderr[-1000:]}")
    return r

results = {}
t0 = time.time()

for name in names:
    lig_dir = f"{MMDIR}/{name}"
    os.makedirs(lig_dir, exist_ok=True)
    sdf  = f"{WORK}/best_poses/{name}_pose1.sdf"
    mol2 = f"{lig_dir}/lig.mol2"
    frcm = f"{lig_dir}/lig.frcmod"
    cpx  = f"{lig_dir}/complex.prmtop"

    # antechamber (skip if mol2 already exists — rank-1 already done)
    if not Path(mol2).exists():
        t1 = time.time()
        run([f"{AMBER}/antechamber",
             "-i", sdf, "-fi", "sdf",
             "-o", mol2, "-fo", "mol2",
             "-c", "bcc", "-s", "2",
             "-at", "gaff2", "-nc", "0",
             "-m", "1", "-rn", "LIG"],
            cwd=lig_dir)
        dt = time.time() - t1
        print(f"[{name}] antechamber {dt:.0f}s mol2={Path(mol2).stat().st_size}B")
    else:
        print(f"[{name}] mol2 exists, skip antechamber")

    # parmchk2
    if not Path(frcm).exists():
        run([f"{AMBER}/parmchk2",
             "-i", mol2, "-f", "mol2",
             "-o", frcm, "-a", "Y"],
            cwd=lig_dir)

    # tleap (skip if topology already built)
    if not Path(cpx).exists() or Path(cpx).stat().st_size == 0:
        tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
LIG = loadmol2 {mol2}
loadamberparams {frcm}
REC = loadpdb {rec_nozn}
COMPLEX = combine {{REC LIG}}
saveamberparm LIG {lig_dir}/lig.prmtop {lig_dir}/lig.inpcrd
saveamberparm REC {lig_dir}/rec.prmtop {lig_dir}/rec.inpcrd
saveamberparm COMPLEX {lig_dir}/complex.prmtop {lig_dir}/complex.inpcrd
quit
"""
        Path(f"{lig_dir}/tleap.in").write_text(tleap_in)
        r = run([f"{AMBER}/tleap", "-f", f"{lig_dir}/tleap.in"], cwd=lig_dir)
        if "FATAL" in r.stdout:
            raise RuntimeError(f"tleap FATAL for {name}: {r.stdout[-500:]}")
        print(f"[{name}] tleap done  cpx={Path(cpx).stat().st_size}B")
    else:
        print(f"[{name}] topology exists, skip tleap")

    results[name] = {
        "mol2": Path(mol2).exists(),
        "frcmod": Path(frcm).exists(),
        "complex_prmtop": Path(cpx).stat().st_size if Path(cpx).exists() else 0
    }

elapsed = time.time() - t0
print(f"\nDone: {len(results)} ligands in {elapsed:.0f}s ({elapsed/len(results):.0f}s/ligand)")
ok = sum(1 for v in results.values() if v["complex_prmtop"] > 0)
print(f"Topologies built: {ok}/32")
