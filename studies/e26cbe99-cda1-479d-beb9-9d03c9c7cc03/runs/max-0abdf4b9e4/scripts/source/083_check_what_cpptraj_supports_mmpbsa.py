
import subprocess

# Check what cpptraj supports for MMPBSA
r = subprocess.run(['cpptraj', '--help', 'mmgbsa'], capture_output=True, text=True)
print("mmgbsa help:", r.returncode, r.stdout[:400] if r.stdout else r.stderr[:400])

# Check MMPBSA.py under various names
for cmd in ['MMPBSA.py', 'ante-MMPBSA.py', 'MM_PBSA.py', 'gmx_MMPBSA']:
    r2 = subprocess.run(['which', cmd], capture_output=True, text=True)
    if r2.returncode == 0:
        print(f"Found: {cmd} -> {r2.stdout.strip()}")

# Check if cpptype can read XTC directly
# Write a test cpptraj script that checks parm loading
test_script = f"""\
parm {MD_DIR}/complex.prmtop
trajin {MD_DIR}/complex.gro [1]
atominfo :LIG
run
quit
"""
with open(f'{MD_DIR}/test_cpptraj.in', 'w') as fh:
    fh.write(test_script)

r3 = subprocess.run(['cpptraj', '-i', f'{MD_DIR}/test_cpptraj.in'],
                    capture_output=True, text=True)
for line in (r3.stdout + r3.stderr).splitlines():
    if 'LIG' in line or 'Error' in line or 'parm' in line.lower() or 'atom' in line.lower():
        print(line)
