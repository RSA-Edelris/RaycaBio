
import pathlib

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
SYS_DIR = BASE / 'md' / 'systems'

for lig in ['CPD4', 'CPD7']:
    log = SYS_DIR / lig / 'leap.log'
    txt = log.read_text()
    # Print lines that actually contain the error message (not just the "Error!" banner)
    error_lines = []
    lines = txt.splitlines()
    for i, line in enumerate(lines):
        if 'Error!' in line and i+1 < len(lines):
            next_line = lines[i+1].strip()
            if next_line and not next_line.startswith('/home'):
                error_lines.append(f"  {next_line}")
    # deduplicate
    seen = set()
    unique_errors = []
    for l in error_lines:
        if l not in seen:
            seen.add(l)
            unique_errors.append(l)
    print(f"=== {lig}: unique error types ===")
    print('\n'.join(unique_errors[:30]))
    print()
