
import pathlib
PARAM = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b/md/param')

LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']
ok_all = True
for lig in LIGS:
    mol2   = PARAM / lig / f'{lig}.mol2'
    frcmod = PARAM / lig / f'{lig}.frcmod'
    # Check residue name in mol2
    mol2_txt = mol2.read_text()
    has_LIG = 'LIG' in mol2_txt
    # Count atoms in mol2
    in_atoms = False
    n_atoms = 0
    for line in mol2_txt.splitlines():
        if line.startswith('@<TRIPOS>ATOM'): in_atoms = True; continue
        if line.startswith('@<TRIPOS>') and in_atoms: break
        if in_atoms and line.strip(): n_atoms += 1
    # Count non-comment lines in frcmod
    n_frc = sum(1 for l in frcmod.read_text().splitlines() if l.strip() and not l.startswith('!'))
    status = 'OK' if has_LIG else 'BAD_RESNAME'
    print(f"  {lig:<12} mol2: {n_atoms:3d} atoms, LIG={has_LIG} | frcmod: {n_frc:3d} lines  → {status}")
    if not has_LIG: ok_all = False

print(f"\nAll mol2 have LIG residue name: {ok_all}")
