
import pathlib

BASE = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
PARAM_DIR = BASE / 'md' / 'param'

# Check sqm.out for a failing ligand
for lig in ['REF_85C', 'CPD1']:
    sqm_out = PARAM_DIR / lig / 'sqm.out'
    sqm_in  = PARAM_DIR / lig / 'sqm.in'
    ac_log  = PARAM_DIR / lig / 'antechamber.log' if (PARAM_DIR / lig / 'antechamber.log').exists() else None
    print(f"=== {lig} ===")
    if sqm_out.exists():
        txt = sqm_out.read_text()
        print(f"sqm.out ({len(txt)} chars):")
        print(txt[-600:])
    else:
        print("  sqm.out not found")
    if sqm_in.exists():
        print(f"sqm.in first 5 lines: {sqm_in.read_text().splitlines()[:5]}")
    print()
