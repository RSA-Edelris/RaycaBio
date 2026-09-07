
import subprocess
from pathlib import Path

# parmchk2 — compiled binary
frcmod = f"{lig_dir}/lig.frcmod"
r = subprocess.run(
    [f"{AMBER}/parmchk2",
     "-i", f"{lig_dir}/lig.mol2", "-f", "mol2",
     "-o", frcmod, "-a", "Y"],
    cwd=lig_dir, capture_output=True, text=True, timeout=60
)
print("parmchk2 rc:", r.returncode)
print(Path(frcmod).read_text()[:300])
