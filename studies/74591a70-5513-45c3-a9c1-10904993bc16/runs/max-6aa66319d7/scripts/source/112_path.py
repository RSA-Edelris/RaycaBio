
import subprocess
from pathlib import Path

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
V2000_SDF = str(BASE / "CRBN_lig_results_2_v2000.sdf")
STAGE1    = str(BASE / "CRBN_enantio2_stage1.sdf")

# Check obabel stereo enumeration options
r = subprocess.run(['obabel', '--help'], capture_output=True, text=True)
stereo_line = [l for l in (r.stdout+r.stderr).split('\n') if 'stereo' in l.lower() or 'enantiomer' in l.lower() or 'enum' in l.lower()]
print("Stereo-related obabel options:")
for l in stereo_line: print(" ", l)
print()
# Check --enumerate
r2 = subprocess.run(['obabel', '--help', '--enumerate'], capture_output=True, text=True)
print(r2.stderr[:500])
