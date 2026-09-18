
import pathlib, subprocess

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
PARAM   = BASE / 'md' / 'param'
SYS_DIR = BASE / 'md' / 'systems'

# === CPD7: check frcmod presence and tleap.in path ===
frcmod7 = PARAM / 'CPD7' / 'CPD7.frcmod'
print(f"CPD7 frcmod exists: {frcmod7.exists()}, size: {frcmod7.stat().st_size if frcmod7.exists() else 0}")
leap7 = SYS_DIR / 'CPD7' / 'tleap.in'
print(f"CPD7 tleap.in frcmod line: {[l for l in leap7.read_text().splitlines() if 'frcmod' in l and 'CPD7' in l]}")
print()

# === CPD4: check atom types in mol2 ===
mol2_4 = PARAM / 'CPD4' / 'CPD4.mol2'
print("CPD4 atom types present:")
in_atoms = False
types = set()
for line in mol2_4.read_text().splitlines():
    if '@<TRIPOS>ATOM' in line: in_atoms = True; continue
    if '@<TRIPOS>' in line and in_atoms: break
    if in_atoms and line.strip():
        parts = line.split()
        if len(parts) >= 6:
            types.add(parts[5])   # atom type is column 6 in mol2
print(f"  {sorted(types)}")
print()

# === CPD7: check atom types in mol2 ===
mol2_7 = PARAM / 'CPD7' / 'CPD7.mol2'
types7 = set()
in_atoms = False
for line in mol2_7.read_text().splitlines():
    if '@<TRIPOS>ATOM' in line: in_atoms = True; continue
    if '@<TRIPOS>' in line and in_atoms: break
    if in_atoms and line.strip():
        parts = line.split()
        if len(parts) >= 6:
            types7.add(parts[5])
print(f"CPD7 atom types: {sorted(types7)}")

# Check if frcmod7 was written with the right path
print(f"\nfrcmod7 first 5 lines:\n{chr(10).join(frcmod7.read_text().splitlines()[:5])}")
