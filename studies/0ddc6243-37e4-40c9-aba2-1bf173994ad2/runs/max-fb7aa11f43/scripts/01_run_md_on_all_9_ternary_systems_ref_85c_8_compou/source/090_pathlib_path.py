
import pathlib

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
SYS_DIR = BASE / 'md' / 'systems'
LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']

total = 0
files_to_stage = []
print(f"{'Ligand':<12} {'prmtop MB':>10} {'inpcrd MB':>10} {'atoms':>8}")
for lig in LIGS:
    p = SYS_DIR / lig / 'system.prmtop'
    c = SYS_DIR / lig / 'system.inpcrd'
    pm = p.stat().st_size / 1e6
    cm = c.stat().st_size / 1e6
    total += pm + cm
    files_to_stage += [str(p), str(c)]
    natoms = sum(1 for l in (SYS_DIR/lig/'system.pdb').read_text().splitlines()
                 if l.startswith(('ATOM','HETATM')))
    print(f"{lig:<12} {pm:>10.1f} {cm:>10.1f} {natoms:>8}")

print(f"\nTotal to stage: {total:.0f} MB across {len(files_to_stage)} files")
print("\nFile paths:")
for f in files_to_stage:
    print(f"  {f}")
