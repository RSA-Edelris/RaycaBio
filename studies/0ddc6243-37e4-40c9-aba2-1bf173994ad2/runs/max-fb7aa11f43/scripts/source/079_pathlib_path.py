
import pathlib, tarfile

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
AMBER_DIR = SESSION / "md" / "amber_inputs"
AMBER_DIR.mkdir(exist_ok=True)
LIGS = ["REF_85C","CPD1","CPD4","CPD7","CPD8","CPD9","CPD10","CPD11","CPD12"]

# ── AMBER input decks ──────────────────────────────────────────────────────
(AMBER_DIR / "min.in").write_text("""\
Minimization - protein backbone restrained
 &cntrl
  imin=1, ntx=1, irest=0,
  maxcyc=10000, ncyc=5000,
  ntpr=500, ntwx=0,
  ntf=1, ntc=1,
  cut=10.0,
  ntr=1, restraintmask='@CA,C,N,O', restraint_wt=5.0,
 /
""")

(AMBER_DIR / "heat.in").write_text("""\
Heating 0-300 K 100 ps NVT - protein backbone restrained
 &cntrl
  imin=0, ntx=1, irest=0,
  nstlim=50000, dt=0.002,
  ntpr=1000, ntwx=0, ntwe=0,
  ntf=2, ntc=2,
  cut=10.0,
  ntt=3, gamma_ln=2.0,
  tempi=0.0, temp0=300.0,
  ig=-1,
  ntr=1, restraintmask='@CA,C,N,O', restraint_wt=5.0,
 /
""")

(AMBER_DIR / "equil.in").write_text("""\
Equilibration 500 ps NPT - protein backbone restrained 1 kcal/mol
 &cntrl
  imin=0, ntx=5, irest=1,
  nstlim=250000, dt=0.002,
  ntpr=2500, ntwx=0, ntwe=0,
  ntf=2, ntc=2,
  cut=10.0,
  ntt=3, gamma_ln=2.0, temp0=300.0,
  ntp=1, barostat=2, pres0=1.0, taup=2.0,
  ig=-1,
  ntr=1, restraintmask='@CA,C,N,O', restraint_wt=1.0,
 /
""")

(AMBER_DIR / "prod.in").write_text("""\
Production 5 ns NPT 300 K
 &cntrl
  imin=0, ntx=5, irest=1,
  nstlim=2500000, dt=0.002,
  ntpr=5000, ntwx=5000, ntwe=0,
  ntf=2, ntc=2,
  cut=10.0,
  ntt=3, gamma_ln=2.0, temp0=300.0,
  ntp=1, barostat=2, pres0=1.0, taup=2.0,
  ig=-1,
  iwrap=1,
 /
""")

print("AMBER input files written:")
for f in sorted(AMBER_DIR.iterdir()):
    print(f"  {f.name}: {f.stat().st_size} bytes")

# ── Build staging tarball ──────────────────────────────────────────────────
tar_path = SESSION / "md" / "systems_stage.tar.gz"
SYSTEMS_DIR = SESSION / "md" / "systems"

with tarfile.open(tar_path, "w:gz") as tar:
    # AMBER input decks
    for f in AMBER_DIR.iterdir():
        tar.add(f, arcname=f"inputs/{f.name}")
    # System topologies (prmtop + inpcrd only - not large .pdb)
    for lig in LIGS:
        d = SYSTEMS_DIR / lig
        tar.add(d / "system.prmtop", arcname=f"systems/{lig}/system.prmtop")
        tar.add(d / "system.inpcrd", arcname=f"systems/{lig}/system.inpcrd")

sz_mb = tar_path.stat().st_size / 1e6
print(f"\nTarball: {tar_path.name}  {sz_mb:.1f} MB")
