
# Verify all files to stage exist and get sizes
import os
stage_files = [
    f'{MD_DIR}/complex.gro',
    f'{MD_DIR}/complex.top',
    f'{MD_DIR}/em.mdp',
    f'{MD_DIR}/npt_eq.mdp',
    f'{MD_DIR}/prod.mdp',
    f'{MD_DIR}/index.ndx',
]
all_ok = True
for f in stage_files:
    sz = os.path.getsize(f) if os.path.exists(f) else None
    ok = sz is not None
    print(f"  {'OK' if ok else 'MISSING':7s} {os.path.basename(f):20s} {sz:>10,} bytes" if ok else f"  MISSING  {os.path.basename(f)}")
    all_ok = all_ok and ok
print(f"\nAll files ready: {all_ok}")
