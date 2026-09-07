
import subprocess, pathlib

INPUT_SDF = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_lig_results_2.sdf"
BASE = "/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
V2000_SDF = f"{BASE}/CRBN_lig_results_2_v2000.sdf"

# Convert V3000 → V2000 with obabel, keeping SD data
r = subprocess.run(
    ['obabel', INPUT_SDF, '-O', V2000_SDF, '--gen2D'],
    capture_output=True, text=True
)
print("obabel stdout:", r.stdout[:300])
print("obabel stderr:", r.stderr[:300])
print("return code:", r.returncode)
print("output exists:", pathlib.Path(V2000_SDF).exists())
if pathlib.Path(V2000_SDF).exists():
    print("output size:", pathlib.Path(V2000_SDF).stat().st_size)
