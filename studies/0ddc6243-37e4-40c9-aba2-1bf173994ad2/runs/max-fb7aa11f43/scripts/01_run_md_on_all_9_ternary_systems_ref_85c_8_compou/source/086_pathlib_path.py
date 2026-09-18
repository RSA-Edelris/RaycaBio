
import pathlib

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
SYS_DIR = BASE / 'md' / 'systems'

for lig in ['CPD4', 'CPD7']:
    prmtop = SYS_DIR / lig / 'system.prmtop'
    leap_in = SYS_DIR / lig / 'tleap.in'
    print(f"=== {lig}: prmtop size = {prmtop.stat().st_size} bytes ===")
    # Read leap log (tleap writes to leap.log in cwd)
    log = SYS_DIR / lig / 'leap.log'
    if log.exists():
        txt = log.read_text()
        # Show lines with error/warning/fatal
        lines = txt.splitlines()
        errs = [l for l in lines if any(k in l.lower() for k in ['error','fatal','warning','failed','cannot'])]
        print('\n'.join(errs[-20:]) or "No error lines found")
        print(f"  (last 10 lines): {chr(10).join(lines[-10:])}")
    else:
        print("  no leap.log found")
    print()
