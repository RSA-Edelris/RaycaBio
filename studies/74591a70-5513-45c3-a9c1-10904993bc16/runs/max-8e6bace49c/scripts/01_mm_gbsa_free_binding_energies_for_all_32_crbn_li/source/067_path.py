
import subprocess
from pathlib import Path

rec_pdb = f"{WORK}/4CI2_receptor_noh.pdb"

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
Path(f"{lig_dir}/tleap.in").write_text(tleap_in)

r = subprocess.run(
    [f"{AMBER}/tleap", "-f", f"{lig_dir}/tleap.in"],
    cwd=lig_dir, capture_output=True, text=True, timeout=120
)
print("tleap rc:", r.returncode)
# Show last 60 lines — errors appear there
lines = (r.stdout + r.stderr).split("\n")
print("\n".join(lines[-60:]))

for f in ["complex.prmtop","rec.prmtop","lig.prmtop"]:
    p = Path(f"{lig_dir}/{f}")
    print(f"{f}: {'OK ' + str(p.stat().st_size) + 'B' if p.exists() else 'MISSING'}")
