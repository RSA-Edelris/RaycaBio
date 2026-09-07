
import tarfile, os
from pathlib import Path

# Pack only what sander needs on LUMI (complex.prmtop + complex.inpcrd)
# min.rst7 for EDEL-CRBN-0001 already exists, include it too
staging_tar = f"{MMDIR}/mmgbsa_staging.tar.gz"

with tarfile.open(staging_tar, "w:gz") as tar:
    for name in names:
        d = Path(MMDIR) / f"{name}_ent"
        for fname in ["complex.prmtop", "complex.inpcrd", "min.rst7"]:
            p = d / fname
            if p.exists():
                arcname = f"{name}_ent/{fname}"
                tar.add(str(p), arcname=arcname)
                print(f"  + {arcname}  ({p.stat().st_size//1024} kB)")

sz = Path(staging_tar).stat().st_size
print(f"\nTotal tar: {sz//1024//1024} MB")
