
import pathlib

BASE  = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
H_DIR = BASE / 'md' / 'ligands_h'
PARAM = BASE / 'md' / 'param'

print("H-added SDFs:")
for f in sorted(H_DIR.glob('*.sdf')):
    print(f"  {f.name} ({f.stat().st_size} bytes)")

print("\nparam results so far:")
for lig in ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']:
    mol2   = PARAM / lig / f'{lig}.mol2'
    frcmod = PARAM / lig / f'{lig}.frcmod'
    m = mol2.stat().st_size if mol2.exists() else 0
    f = frcmod.stat().st_size if frcmod.exists() else 0
    print(f"  {lig:<12} mol2={m:6d}B  frcmod={f:6d}B")
