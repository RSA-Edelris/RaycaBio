
import os

INPUTS = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/md_prep/inputs'
COMPOUNDS = ['EDS00495858', 'EDS00480994', 'EDS00444974', 'EDS00481054', 'EDS00441134', 'EDS00445742']

for cid in COMPOUNDS:
    path = os.path.join(INPUTS, f'{cid}_topol.top')
    with open(path) as f:
        lines = f.readlines()

    # Find the FIRST [ system ] line index
    first_sys = None
    for i, l in enumerate(lines):
        if l.strip() == '[ system ]':
            first_sys = i
            break

    if first_sys is None:
        print(f'{cid}: no [ system ] found — skipping')
        continue

    # Find the end of the [ molecules ] block that follows
    # Scan forward from first_sys: skip [ system ], name, blank, [ molecules ], comment, count
    # Stop when we hit #ifdef or ; TIP3P or a second [ system ] or blank line after the count
    # Strategy: remove lines from first_sys up to (but not including) #ifdef POSRES or next section
    j = first_sys
    while j < len(lines):
        stripped = lines[j].strip()
        # Stop at #ifdef or #include amber or second comment for TIP3P water
        if stripped.startswith('#ifdef') or stripped.startswith('; TIP3P') or (stripped.startswith('; ') and 'TIP3P' in stripped):
            break
        j += 1

    removed = lines[first_sys:j]
    kept = lines[:first_sys] + lines[j:]

    with open(path, 'w') as f:
        f.writelines(kept)

    print(f'{cid}: removed {j - first_sys} lines ({first_sys}–{j-1})')
    print(f'  Removed: {[l.rstrip() for l in removed]}')
