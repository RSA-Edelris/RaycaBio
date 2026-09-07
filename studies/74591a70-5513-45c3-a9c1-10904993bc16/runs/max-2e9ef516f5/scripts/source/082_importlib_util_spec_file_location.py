
import importlib.util, time
from pathlib import Path

spec = importlib.util.spec_from_file_location("pipeline", f"{MMDIR}/pipeline.py")
pipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipe)

# Delete old partial min.rst7 from cut=999 run
old_min = Path(MMDIR) / "EDEL-CRBN-0005_ent" / "min.rst7"
if old_min.exists():
    old_min.unlink()
    print("Removed old cut=999 min.rst7 for EDEL-CRBN-0005_ent")

# Time minimization on the first compound
test = names[0]  # EDEL-CRBN-0001
print(f"\nTiming sander minimization (500 steps, cut=12.0, igb=5) on {test}...")
t0 = time.time()
try:
    pipe.run_min(test)
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.1f}s  ({elapsed/500*1000:.1f} ms/step)")
    print(f"  Estimated for 32 compounds x 500 min steps: {elapsed*32/60:.1f} min")
    # Also estimate MD time (10000 steps, but GB is ~same cost)
    # MD has 10000 steps, so ~20x longer
    print(f"  Estimated for 32 compounds x 10000 MD steps: {elapsed*20*32/60:.1f} min")
except Exception as e:
    elapsed = time.time() - t0
    print(f"  FAILED after {elapsed:.1f}s: {e}")
