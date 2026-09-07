
import subprocess, os
from pathlib import Path

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER_BIN = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
ENV = os.environ.copy()
ENV['PATH'] = AMBER_BIN + ':' + ENV.get('PATH','')
ENV['AMBERHOME'] = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
MMGBSA_DIR = Path(f"{BASE}/mmgbsa2")

rec_amber = MMGBSA_DIR / "receptor_amber.pdb"
rec_prmtop = MMGBSA_DIR / "receptor.prmtop"
rec_inpcrd  = MMGBSA_DIR / "receptor.inpcrd"
for f in [rec_prmtop, rec_inpcrd]: 
    if f.exists(): f.unlink()

# No water model source — implicit solvent doesn't need TIP3P parameters
tleap_rec = f"""source leaprc.protein.ff14SB
rec = loadpdb {rec_amber}
saveamberparm rec {rec_prmtop} {rec_inpcrd}
quit
"""
tf = MMGBSA_DIR / "tleap_rec.in"
tf.write_text(tleap_rec)

r = subprocess.run(
    f"{AMBER_BIN}/tleap -f {tf}",
    shell=True, capture_output=True, text=True, cwd=str(MMGBSA_DIR), env=ENV
)
print("RC:", r.returncode)
for line in r.stdout.splitlines()[-25:]:
    print(line)
if r.returncode != 0 and r.stderr:
    print("STDERR:", r.stderr[:200])

if rec_prmtop.exists() and rec_prmtop.stat().st_size > 1000:
    print(f"\n✓ receptor.prmtop: {rec_prmtop.stat().st_size:,} bytes")
else:
    print(f"\n✗ receptor.prmtop: {rec_prmtop.stat().st_size if rec_prmtop.exists() else 'MISSING'} bytes")
