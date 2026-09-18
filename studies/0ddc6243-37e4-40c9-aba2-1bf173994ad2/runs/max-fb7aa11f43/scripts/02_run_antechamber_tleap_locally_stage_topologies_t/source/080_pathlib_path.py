
import pathlib

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
AMBER_DIR = SESSION / "md" / "amber_inputs"

# Update equil: 200 ps (100 k steps × 2 fs)
(AMBER_DIR / "equil.in").write_text("""\
Equilibration 200 ps NPT - backbone restrained 1 kcal/mol
 &cntrl
  imin=0, ntx=5, irest=1,
  nstlim=100000, dt=0.002,
  ntpr=2500, ntwx=0, ntwe=0,
  ntf=2, ntc=2,
  cut=10.0,
  ntt=3, gamma_ln=2.0, temp0=300.0,
  ntp=1, barostat=2, pres0=1.0, taup=2.0,
  ig=-1,
  ntr=1, restraintmask='@CA,C,N,O', restraint_wt=1.0,
 /
""")

# Update prod: 1 ns (500 k steps × 2 fs), save every 5 ps (2500 steps)
(AMBER_DIR / "prod.in").write_text("""\
Production 1 ns NPT 300 K
 &cntrl
  imin=0, ntx=5, irest=1,
  nstlim=500000, dt=0.002,
  ntpr=2500, ntwx=2500, ntwe=0,
  ntf=2, ntc=2,
  cut=10.0,
  ntt=3, gamma_ln=2.0, temp0=300.0,
  ntp=1, barostat=2, pres0=1.0, taup=2.0,
  ig=-1,
  iwrap=1,
 /
""")

# Rebuild tarball with updated inputs
import tarfile

tar_path = SESSION / "md" / "systems_stage.tar.gz"
SYSTEMS_DIR = SESSION / "md" / "systems"
LIGS = ["REF_85C","CPD1","CPD4","CPD7","CPD8","CPD9","CPD10","CPD11","CPD12"]

with tarfile.open(tar_path, "w:gz") as tar:
    for f in AMBER_DIR.iterdir():
        tar.add(f, arcname=f"inputs/{f.name}")
    for lig in LIGS:
        d = SYSTEMS_DIR / lig
        tar.add(d / "system.prmtop", arcname=f"systems/{lig}/system.prmtop")
        tar.add(d / "system.inpcrd", arcname=f"systems/{lig}/system.inpcrd")

print(f"Tarball rebuilt: {tar_path.stat().st_size/1e6:.1f} MB")
print("Inputs:")
for f in sorted(AMBER_DIR.iterdir()):
    print(f"  {f.name}: {f.read_text()[:60].strip()}")
