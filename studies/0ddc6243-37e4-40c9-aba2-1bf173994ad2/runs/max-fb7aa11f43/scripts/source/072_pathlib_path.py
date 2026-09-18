
import subprocess, pathlib

SESSION = pathlib.Path("/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b")
d4 = SESSION / "md" / "systems" / "CPD4"
tleap_in = d4 / "tleap.in"

r4 = subprocess.run(
    ["tleap", "-f", str(tleap_in)],
    capture_output=True, text=True, cwd=str(d4)
)
# Show only the Error lines
errors = [l for l in (r4.stdout + r4.stderr).splitlines() if "Error" in l or "torsion" in l.lower()]
for l in errors:
    print(l)
