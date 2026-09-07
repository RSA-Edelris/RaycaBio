
import importlib.util, sys

spec = importlib.util.spec_from_file_location("pipeline", f"{MMDIR}/pipeline.py")
pipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipe)

# Verify test on first compound (skip EDEL-CRBN-0005_ent which already has AM1-BCC mol2)
test = "EDEL-CRBN-0001"
print(f"Testing antechamber -c gas on {test}...")
try:
    mol2, frcmod = pipe.prepare_ligand(test)
    print(f"  mol2:   {mol2} ({mol2.stat().st_size} B)")
    print(f"  frcmod: {frcmod} ({frcmod.stat().st_size} B)")
    print("  SUCCESS")
except Exception as e:
    print(f"  FAILED: {e}")
