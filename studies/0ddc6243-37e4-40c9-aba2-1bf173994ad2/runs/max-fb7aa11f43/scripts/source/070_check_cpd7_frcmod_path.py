
# Check CPD7 frcmod path
import pathlib
SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
PARAM_DIR = SESSION / "md" / "param"

cpd7_frc = PARAM_DIR / "CPD7" / "CPD7.frcmod"
print(f"CPD7 frcmod exists: {cpd7_frc.exists()}")
print(f"CPD7 param dir contents:")
for f in (PARAM_DIR / "CPD7").iterdir():
    print(f"  {f.name}: {f.stat().st_size} bytes")
