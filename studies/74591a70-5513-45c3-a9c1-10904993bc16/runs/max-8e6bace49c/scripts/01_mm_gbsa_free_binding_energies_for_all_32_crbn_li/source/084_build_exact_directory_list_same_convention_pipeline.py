
# Build the exact directory list (same convention as pipeline.py: d = Path(MMDIR) / f"{name}_ent")
compound_dirs = [f"{name}_ent" for name in names]
print("First 5 compound dirs:", compound_dirs[:5])
print("Total:", len(compound_dirs))

# Verify all complex.prmtop files exist
from pathlib import Path
missing = [d for d in compound_dirs if not (Path(MMDIR)/d/"complex.prmtop").exists()]
if missing:
    print("MISSING prmtop:", missing)
else:
    print("All 32 complex.prmtop files exist locally")
