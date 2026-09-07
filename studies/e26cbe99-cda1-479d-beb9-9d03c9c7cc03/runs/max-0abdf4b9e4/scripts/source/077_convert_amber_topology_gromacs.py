
import parmed as pmd
import os

# ── Convert AMBER topology → GROMACS ──────────────────────────────────────
print("Loading AMBER topology...")
amber_sys = pmd.load_file(f'{MD_DIR}/complex.prmtop', f'{MD_DIR}/complex.inpcrd')

n_atoms = len(amber_sys.atoms)
n_res   = len(amber_sys.residues)
box     = amber_sys.box
print(f"  Atoms: {n_atoms:,}")
print(f"  Residues: {n_res:,}")
print(f"  Box (Å): {box[0]:.2f} x {box[1]:.2f} x {box[2]:.2f}")

print("Saving GROMACS topology and coordinates...")
amber_sys.save(f'{MD_DIR}/complex.top', overwrite=True)
amber_sys.save(f'{MD_DIR}/complex.gro', overwrite=True)

for fname in ['complex.top', 'complex.gro']:
    path = f'{MD_DIR}/{fname}'
    print(f"  {fname}: {os.path.getsize(path):,} bytes")
