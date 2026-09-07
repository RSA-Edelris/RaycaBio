
import subprocess, os

cid = 'EDS01357518_ent1'
d   = f'{WD}/md_{cid}'

# Show all groups in the gro file
r = subprocess.run(
    ['gmx', 'make_ndx', '-f', f'{d}/complex.gro', '-o', '/dev/null'],
    input='q\n', capture_output=True, text=True, env=env
)
print(r.stdout[-2000:])
print(r.stderr[-500:] if r.stderr else "")
