
import subprocess, os
from pathlib import Path

BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
AMBER_BIN = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin"
AMBERHOME = "/home/ubuntu/rayca-runtime/.mamba/envs/rayca"
ENV = os.environ.copy()
ENV['PATH'] = AMBER_BIN + ':' + ENV.get('PATH','')
ENV['AMBERHOME'] = AMBERHOME
MMGBSA_DIR = Path(f"{BASE}/mmgbsa2")

rec_amber = MMGBSA_DIR / "receptor_amber.pdb"
lines = rec_amber.read_text().splitlines()

fixed = []
for line in lines:
    if not line.startswith('ATOM'):
        fixed.append(line)
        continue
    resseq = line[22:26].strip()
    chain  = line[21]
    resname = line[17:20].strip()
    atom_name_raw = line[12:16]  # 4-char raw field
    # Rename ' H  ' → ' H1 ' only for NMET (residue 47 chain B)
    if resseq == '47' and chain == 'B' and resname in ('MET','NMET') and atom_name_raw == ' H  ':
        line = line[:12] + ' H1 ' + line[16:]
    fixed.append(line)

rec_amber.write_text('\n'.join(fixed) + '\n')
print("Patched NMET 47 H → H1")

# Verify
found = [l for l in fixed if 'B  47' in l and ' H1 ' in l[:16]]
print(f"H1 atoms in NMET 47: {len(found)}")
if found:
    print(found[0])

# Re-run tleap receptor
rec_prmtop = MMGBSA_DIR / "receptor.prmtop"
rec_inpcrd  = MMGBSA_DIR / "receptor.inpcrd"
for f in [rec_prmtop, rec_inpcrd]: 
    if f.exists(): f.unlink()

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
print("\ntleap RC:", r.returncode)
for line in r.stdout.splitlines()[-20:]:
    print(line)

if rec_prmtop.exists() and rec_prmtop.stat().st_size > 1000:
    print(f"\n✓ receptor.prmtop: {rec_prmtop.stat().st_size:,} bytes")
else:
    print(f"\n✗ receptor.prmtop: {rec_prmtop.stat().st_size if rec_prmtop.exists() else 'MISSING'}")
