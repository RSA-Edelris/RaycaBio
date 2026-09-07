
import importlib.util, subprocess, os
from pathlib import Path

spec = importlib.util.spec_from_file_location("pipeline", f"{MMDIR}/pipeline.py")
pipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipe)

print("Running antechamber + parmchk2 for all 32 ligands (Gasteiger charges)...")
ok, failed = [], []
for name in names:
    try:
        mol2, frcmod = pipe.prepare_ligand(name)
        ok.append(name)
        print(f"  OK  {name:<28} mol2={mol2.stat().st_size}B  frcmod={frcmod.stat().st_size}B")
    except Exception as e:
        failed.append((name, str(e)[:200]))
        print(f"  FAIL {name}: {str(e)[:200]}")

print(f"\nSummary: {len(ok)}/32 OK,  {len(failed)} failed")
