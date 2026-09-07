
# Check if LVY is present in the prepared receptor, and look for the original 4CI2
BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")

rec_text = (BASE / "4CI2_receptor_for_docking.pdb").read_text()
lvy_lines = [l for l in rec_text.splitlines() if "LVY" in l]
print(f"LVY lines in 4CI2_receptor_for_docking.pdb: {len(lvy_lines)}")
if lvy_lines:
    print("  First:", lvy_lines[0][:80])

# Also check amber receptor
rec_amber = (BASE / "mmgbsa2" / "receptor_amber.pdb").read_text()
lvy_amber = [l for l in rec_amber.splitlines() if "LVY" in l]
print(f"LVY lines in receptor_amber.pdb: {len(lvy_amber)}")

# Look for any raw 4CI2 PDB
import subprocess
res = subprocess.run(["find", str(BASE), "-name", "*.pdb", "-not", "-path", "*/mmgbsa2/*"],
                     capture_output=True, text=True)
for p in res.stdout.strip().splitlines():
    sz = Path(p).stat().st_size
    print(f"  {sz:>8,}  {Path(p).name}")
