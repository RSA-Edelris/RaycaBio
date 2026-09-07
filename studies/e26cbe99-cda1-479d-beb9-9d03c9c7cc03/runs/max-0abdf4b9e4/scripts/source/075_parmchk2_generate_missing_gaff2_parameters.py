
import subprocess, os, re

# ── parmchk2: generate missing GAFF2 parameters ───────────────────────────
lig_frcmod = f'{MD_DIR}/ligand.frcmod'
r = subprocess.run(
    ['parmchk2', '-i', lig_mol2, '-f', 'mol2', '-o', lig_frcmod, '-s', 'gaff2'],
    capture_output=True, text=True, cwd=MD_DIR
)
print("parmchk2:", "OK" if r.returncode == 0 else "FAIL")
if r.returncode != 0: print(r.stderr)
else: print(f"  frcmod: {os.path.getsize(lig_frcmod)} bytes")

# ── Prepare receptor PDB for tleap ────────────────────────────────────────
# Load receptor, strip H (tleap re-adds), rename HIS → HIE (epsilon default)
rec_pdb = f'{WD}/PB-20260903-4CI2_receptor_trimmed_fixed.pdb'

with open(rec_pdb) as fh:
    lines = fh.readlines()

out_lines = []
for line in lines:
    rec_type = line[:6].strip()
    if rec_type not in ('ATOM', 'TER', 'END'): continue
    if rec_type == 'ATOM':
        # skip hydrogens
        elem = line[76:78].strip() if len(line) > 76 else ''
        aname = line[12:16].strip()
        if elem == 'H' or aname.startswith('H'): continue
        # rename HIS → HIE (epsilon tautomer, AMBER default)
        resn = line[17:20]
        if resn == 'HIS':
            line = line[:17] + 'HIE' + line[20:]
    out_lines.append(line)

rec_tleap = f'{MD_DIR}/receptor_tleap.pdb'
with open(rec_tleap, 'w') as fh:
    fh.writelines(out_lines)

atom_count = sum(1 for l in out_lines if l[:4] == 'ATOM')
print(f"\nReceptor for tleap: {atom_count} heavy atoms, written to {os.path.basename(rec_tleap)}")

# Count HIS residues renamed
his_count = sum(1 for l in out_lines if l[:4]=='ATOM' and l[17:20]=='HIE')
print(f"  HIE residues present: {len(set(l[22:26].strip() for l in out_lines if l[:4]=='ATOM' and l[17:20]=='HIE'))}")
