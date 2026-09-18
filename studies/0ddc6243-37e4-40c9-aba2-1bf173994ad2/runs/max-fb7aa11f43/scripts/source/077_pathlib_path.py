
import subprocess, pathlib

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
d4 = SESSION / "md" / "param" / "CPD4"
mol2 = d4 / "CPD4_fixed.mol2"
frc2 = d4 / "CPD4_v2.frcmod"

r = subprocess.run(
    ["parmchk2", "-i", str(mol2), "-f", "mol2", "-o", str(frc2), "-s", "gaff2", "-a", "Y"],
    capture_output=True, text=True, cwd=str(d4)
)
print(f"rc={r.returncode}")
print(r.stdout[:3000])
print(r.stderr[:500])
