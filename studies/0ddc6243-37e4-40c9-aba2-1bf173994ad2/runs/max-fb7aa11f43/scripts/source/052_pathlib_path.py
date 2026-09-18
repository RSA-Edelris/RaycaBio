
import subprocess, os, pathlib, concurrent.futures

BASE = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
LIG_DIR  = BASE / 'md' / 'ligands'
PARAM_DIR = BASE / 'md' / 'param'
PARAM_DIR.mkdir(parents=True, exist_ok=True)

LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']

def parameterise(lig):
    sdf = LIG_DIR / f'{lig}_top.sdf'
    if not sdf.exists():
        return lig, False, f'SDF not found: {sdf}'
    d = PARAM_DIR / lig
    d.mkdir(exist_ok=True)
    mol2 = d / f'{lig}.mol2'
    frcmod = d / f'{lig}.frcmod'

    # antechamber
    r1 = subprocess.run([
        'antechamber',
        '-i', str(sdf), '-fi', 'sdf',
        '-o', str(mol2), '-fo', 'mol2',
        '-c', 'bcc', '-s', '2', '-nc', '0',
        '-rn', 'LIG', '-at', 'gaff2', '-dr', 'no'
    ], capture_output=True, text=True, cwd=str(d))

    if r1.returncode != 0 or not mol2.exists():
        return lig, False, f'antechamber FAILED:\n{r1.stderr[-300:]}'

    # parmchk2
    r2 = subprocess.run([
        'parmchk2',
        '-i', str(mol2), '-f', 'mol2',
        '-o', str(frcmod), '-s', 'gaff2'
    ], capture_output=True, text=True, cwd=str(d))

    if r2.returncode != 0 or not frcmod.exists():
        return lig, False, f'parmchk2 FAILED:\n{r2.stderr[-300:]}'

    n_atoms = sum(1 for l in mol2.read_text().splitlines() if l.strip() and not l.startswith('@') and len(l.split()) >= 9)
    n_missing = sum(1 for l in frcmod.read_text().splitlines() if l.strip() and not l.startswith('#'))
    return lig, True, f'mol2 OK ({n_atoms} atom lines), frcmod OK ({n_missing} param lines)'

print(f"Parameterising {len(LIGS)} ligands in parallel...")
with concurrent.futures.ThreadPoolExecutor(max_workers=9) as ex:
    futures = {ex.submit(parameterise, lig): lig for lig in LIGS}
    for f in concurrent.futures.as_completed(futures):
        lig, ok, msg = f.result()
        status = 'OK' if ok else 'FAIL'
        print(f"  {lig:<12} {status}: {msg}")

print("\nDone.")
