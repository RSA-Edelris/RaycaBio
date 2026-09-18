
import subprocess, pathlib
from rdkit import Chem
from rdkit.Chem import AllChem

BASE      = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
LIG_DIR   = BASE / 'md' / 'ligands'
PARAM_DIR = BASE / 'md' / 'param'
H_DIR     = BASE / 'md' / 'ligands_h'   # H-added SDFs
H_DIR.mkdir(exist_ok=True)

LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']

# Step 1: add H to all SDFs
def add_H(lig):
    sdf = LIG_DIR / f'{lig}_top.sdf'
    mol = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)[0]
    if mol is None:
        return lig, None, 'parse failed'
    mol_h = Chem.AddHs(mol, addCoords=True)   # place H in 3D using existing geometry
    n = mol_h.GetNumAtoms()
    n_H = sum(1 for a in mol_h.GetAtoms() if a.GetAtomicNum() == 1)
    elec = sum(a.GetAtomicNum() for a in mol_h.GetAtoms())
    parity = 'even' if elec % 2 == 0 else 'ODD'
    out = H_DIR / f'{lig}_h.sdf'
    w = Chem.SDWriter(str(out))
    w.write(mol_h); w.close()
    return lig, out, f'{n} atoms ({n_H} H), {elec} electrons → {parity}'

print("Adding explicit H:")
h_sdfs = {}
for lig in LIGS:
    lig_name, out_path, msg = add_H(lig)
    print(f"  {lig_name:<12} {msg}")
    if out_path:
        h_sdfs[lig_name] = out_path

# Step 2: antechamber + parmchk2 sequentially on H-added SDFs
def parameterise_h(lig, sdf_h):
    d = PARAM_DIR / lig
    d.mkdir(exist_ok=True)
    mol2   = d / f'{lig}.mol2'
    frcmod = d / f'{lig}.frcmod'
    mol2.unlink(missing_ok=True)
    frcmod.unlink(missing_ok=True)

    r1 = subprocess.run([
        'antechamber',
        '-i', str(sdf_h), '-fi', 'sdf',
        '-o', str(mol2), '-fo', 'mol2',
        '-c', 'bcc', '-s', '0', '-nc', '0',
        '-rn', 'LIG', '-at', 'gaff2', '-dr', 'no'
    ], capture_output=True, text=True, cwd=str(d))

    if not mol2.exists():
        sqm = (d/'sqm.out').read_text()[-300:] if (d/'sqm.out').exists() else r1.stderr[-200:]
        return lig, False, sqm

    r2 = subprocess.run([
        'parmchk2', '-i', str(mol2), '-f', 'mol2',
        '-o', str(frcmod), '-s', 'gaff2'
    ], capture_output=True, text=True, cwd=str(d))

    return lig, frcmod.exists(), 'OK'

print("\nRunning antechamber (sequential):")
for lig, sdf_h in h_sdfs.items():
    print(f"  {lig} ...", end=' ', flush=True)
    _, ok, msg = parameterise_h(lig, sdf_h)
    print('OK' if ok else f'FAIL: {msg[:150]}')
