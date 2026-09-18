
import subprocess, pathlib

BASE = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
LIG_DIR   = BASE / 'md' / 'ligands'
PARAM_DIR = BASE / 'md' / 'param'

LIGS = ['REF_85C', 'CPD1', 'CPD8', 'CPD9', 'CPD11', 'CPD12']   # retry failures only

def parameterise(lig):
    sdf = LIG_DIR / f'{lig}_top.sdf'
    d = PARAM_DIR / lig
    d.mkdir(exist_ok=True)
    mol2   = d / f'{lig}.mol2'
    frcmod = d / f'{lig}.frcmod'

    r1 = subprocess.run([
        'antechamber',
        '-i', str(sdf), '-fi', 'sdf',
        '-o', str(mol2), '-fo', 'mol2',
        '-c', 'bcc', '-s', '2', '-nc', '0',
        '-rn', 'LIG', '-at', 'gaff2', '-dr', 'no'
    ], capture_output=True, text=True, cwd=str(d))

    if not mol2.exists():
        sqm_out = (d / 'sqm.out').read_text()[-400:] if (d / 'sqm.out').exists() else ''
        return lig, False, f'antechamber FAILED\n{r1.stderr[-200:]}\n{sqm_out}'

    r2 = subprocess.run([
        'parmchk2',
        '-i', str(mol2), '-f', 'mol2',
        '-o', str(frcmod), '-s', 'gaff2'
    ], capture_output=True, text=True, cwd=str(d))

    ok = frcmod.exists()
    return lig, ok, 'OK' if ok else f'parmchk2 FAILED\n{r2.stderr[-200:]}'

for lig in LIGS:
    print(f"  {lig} ...", end=' ', flush=True)
    _, ok, msg = parameterise(lig)
    print('OK' if ok else f'FAIL: {msg[:120]}')

# Final status across all 9
print("\n=== Final status ===")
for lig in ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']:
    mol2   = PARAM_DIR / lig / f'{lig}.mol2'
    frcmod = PARAM_DIR / lig / f'{lig}.frcmod'
    print(f"  {lig:<12} mol2={'OK' if mol2.exists() else 'MISS'} frcmod={'OK' if frcmod.exists() else 'MISS'}")
