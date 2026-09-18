
import subprocess, pathlib

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
PARAM_DIR = SESSION / "md" / "param"

# ── 1. Run parmchk2 for CPD7 ──────────────────────────────────────────────
d7   = PARAM_DIR / "CPD7"
mol2 = d7 / "CPD7_fixed.mol2"
frc  = d7 / "CPD7.frcmod"

r = subprocess.run(
    ["parmchk2", "-i", str(mol2), "-f", "mol2", "-o", str(frc), "-s", "gaff2"],
    capture_output=True, text=True, cwd=str(d7)
)
print(f"CPD7 parmchk2 rc={r.returncode}")
if frc.exists():
    print(f"  CPD7.frcmod: {frc.stat().st_size} bytes  ✓")
else:
    print(f"  STILL MISSING – stdout: {r.stdout}  stderr: {r.stderr}")

# ── 2. Show full tleap log for CPD4 ──────────────────────────────────────
d4      = SESSION / "md" / "systems" / "CPD4"
log_f   = d4 / "tleap.out"

# Re-run tleap for CPD4 with output captured to file so we can read it
tleap_in = d4 / "tleap.in"
r4 = subprocess.run(
    ["tleap", "-f", str(tleap_in)],
    capture_output=True, text=True, cwd=str(d4)
)
print("\n── CPD4 tleap stdout/stderr (last 1500 chars) ──")
out = r4.stdout + r4.stderr
print(out[-1500:] if len(out) > 1500 else out)
