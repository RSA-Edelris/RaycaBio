
import subprocess, pathlib, textwrap

BASE    = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
PARAM   = BASE / 'md' / 'param'
SYS_DIR = BASE / 'md' / 'systems'
RECEPTOR = BASE / 'md' / 'receptor_nozn.pdb'

def rebuild_frcmod_and_system(lig):
    d = PARAM / lig
    mol2   = d / f'{lig}.mol2'
    frcmod = d / f'{lig}.frcmod'

    # Print current mol2 atom types
    types = set()
    in_atoms = False
    for line in mol2.read_text().splitlines():
        if '@<TRIPOS>ATOM' in line: in_atoms = True; continue
        if '@<TRIPOS>' in line and in_atoms: break
        if in_atoms and line.strip():
            parts = line.split()
            if len(parts) >= 6: types.add(parts[5])
    print(f"  {lig} mol2 atom types: {sorted(types)}")

    # Regenerate frcmod
    frcmod.unlink(missing_ok=True)
    r = subprocess.run([
        'parmchk2', '-i', str(mol2), '-f', 'mol2',
        '-o', str(frcmod), '-s', 'gaff2'
    ], capture_output=True, text=True, cwd=str(d))
    if not frcmod.exists():
        return False, f'parmchk2 FAILED: {r.stderr[:200]}'
    print(f"  {lig} new frcmod first 8 lines:")
    for line in frcmod.read_text().splitlines()[:8]:
        if line.strip(): print(f"    {line}")

    # Rebuild system
    sd = SYS_DIR / lig
    sd.mkdir(exist_ok=True)
    for f in ['system.prmtop', 'system.inpcrd', 'system.pdb', 'leap.log']:
        (sd / f).unlink(missing_ok=True)

    script = textwrap.dedent(f"""\
        source leaprc.protein.ff14SB
        source leaprc.gaff2
        source leaprc.water.tip3p
        loadamberparams frcmod.ionsjc_tip3p
        loadamberparams {frcmod}
        LIG_MOL = loadmol2 {mol2}
        PROT = loadpdb {RECEPTOR}
        MOL = combine {{PROT LIG_MOL}}
        solvateOct MOL TIP3PBOX 12.0
        addIons MOL Na+ 0
        addIons MOL Na+ 40 Cl- 40
        charge MOL
        saveamberparm MOL {sd}/system.prmtop {sd}/system.inpcrd
        savepdb MOL {sd}/system.pdb
        quit
    """)
    (sd / 'tleap.in').write_text(script)
    r2 = subprocess.run(['tleap', '-f', str(sd / 'tleap.in')],
                        capture_output=True, text=True, cwd=str(sd))
    prmtop = sd / 'system.prmtop'
    if prmtop.exists() and prmtop.stat().st_size > 1000:
        natoms = sum(1 for l in (sd/'system.pdb').read_text().splitlines()
                     if l.startswith(('ATOM','HETATM')))
        return True, f'{natoms} atoms, prmtop={prmtop.stat().st_size//1024}KB'
    else:
        log = (sd / 'leap.log')
        errs = [l for l in log.read_text().splitlines()
                if 'Error!' in l or 'error' in l.lower() or 'No torsion' in l] if log.exists() else []
        return False, '\n'.join(set(errs[:10]))

for lig in ['CPD4', 'CPD7']:
    print(f"\n=== Rebuilding {lig} ===")
    ok, msg = rebuild_frcmod_and_system(lig)
    print(f"  Result: {'OK: '+msg if ok else 'FAIL: '+msg[:300]}")
