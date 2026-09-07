
import subprocess
from pathlib import Path

# Find which ligand failed (first one without mol2 after EDEL-CRBN-0005_ent)
for name in names:
    mol2 = Path(f"{MMDIR}/{name}/lig.mol2")
    if not mol2.exists():
        print(f"First missing mol2: {name}")
        failed_dir = f"{MMDIR}/{name}"
        break

sqm_out = Path(f"{failed_dir}/sqm.out")
sqm_in  = Path(f"{failed_dir}/sqm.in")
if sqm_out.exists():
    print("sqm.out tail:\n", sqm_out.read_text()[-600:])
if sqm_in.exists():
    print("sqm.in head:\n", sqm_in.read_text()[:200])

# Also test sqm binary directly
r = subprocess.run([f"{AMBER}/sqm", "--version"],
                   capture_output=True, text=True, timeout=10)
print("sqm test:", r.returncode, r.stdout[:100], r.stderr[:200])

# Check what's in the antechamber error more carefully
r2 = subprocess.run(
    [f"{AMBER}/antechamber",
     "-i", f"{WORK}/best_poses/{name}_pose1.sdf", "-fi", "sdf",
     "-o", f"{failed_dir}/lig.mol2", "-fo", "mol2",
     "-c", "bcc", "-s", "2", "-at", "gaff2", "-nc", "0",
     "-m", "1", "-rn", "LIG"],
    cwd=failed_dir, capture_output=True, text=True, timeout=600
)
print("antechamber rc:", r2.returncode)
print("stdout:", r2.stdout[-400:])
print("stderr:", r2.stderr[-400:])
