
import subprocess, os

# ── Create custom index with Protein_LIG and Water_and_ions ──────────────
ndx_input = '1 | 13\nname 18 Protein_LIG\n15 | 14\nname 19 Water_and_ions\nq\n'

r = subprocess.run(
    ['gmx', 'make_ndx', '-f', f'{MD_DIR}/complex.gro',
     '-n', f'{MD_DIR}/index.ndx', '-o', f'{MD_DIR}/index.ndx'],
    input=ndx_input, capture_output=True, text=True
)
# Verify groups exist
r2 = subprocess.run(
    ['gmx', 'make_ndx', '-f', f'{MD_DIR}/complex.gro',
     '-n', f'{MD_DIR}/index.ndx', '-o', '/dev/null'],
    input='q\n', capture_output=True, text=True
)
for line in r2.stdout.splitlines():
    if 'Protein_LIG' in line or 'Water_and_ions' in line or 'atoms' in line.lower():
        print(line)

# ── Test EM grompp locally ────────────────────────────────────────────────
print("\nRunning local grompp for EM...")
r3 = subprocess.run(
    ['gmx', 'grompp',
     '-f', f'{MD_DIR}/em.mdp',
     '-c', f'{MD_DIR}/complex.gro',
     '-p', f'{MD_DIR}/complex.top',
     '-n', f'{MD_DIR}/index.ndx',
     '-o', f'{MD_DIR}/em.tpr',
     '-maxwarn', '5'],
    capture_output=True, text=True
)
for line in (r3.stdout + r3.stderr).splitlines():
    if any(k in line for k in ['ERROR', 'WARNING', 'error', 'System has', 'atoms in']):
        print(line)
em_ok = os.path.exists(f'{MD_DIR}/em.tpr')
print(f"\nem.tpr created: {em_ok} ({os.path.getsize(f'{MD_DIR}/em.tpr'):,} bytes)" if em_ok else "\nem.tpr NOT created")
