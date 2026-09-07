
import os
from pathlib import Path

# Remove AM1-BCC mol2 + topology for EDEL-CRBN-0005_ent so we redo with Gasteiger
for fname in ["lig.mol2", "lig.frcmod",
              "complex.prmtop", "complex.inpcrd",
              "rec.prmtop", "rec.inpcrd",
              "lig.prmtop", "lig.inpcrd"]:
    p = Path(MMDIR) / "EDEL-CRBN-0005_ent" / fname
    if p.exists():
        p.unlink()
        print(f"  removed {fname}")

print("\nRunning antechamber + parmchk2 for all 32 ligands...")
ok, failed = [], []
for name in names:
    try:
        mol2, frcmod = pipe.prepare_ligand(name)
        sz = mol2.stat().st_size
        ok.append(name)
        print(f"  {name:<28} mol2={sz}B")
    except Exception as e:
        failed.append((name, str(e)[:120]))
        print(f"  FAIL {name}: {str(e)[:120]}")

print(f"\nDone: {len(ok)}/32 OK, {len(failed)} failed")
if failed:
    for n, e in failed:
        print(f"  {n}: {e}")
