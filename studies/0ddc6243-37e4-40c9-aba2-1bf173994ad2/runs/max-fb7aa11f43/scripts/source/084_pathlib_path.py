
import subprocess, pathlib, textwrap

BASE      = pathlib.Path('/home/ubuntu/rayca-sessions/0ddc6243-37e4-40c9-aba2-1bf173994ad2-eaff7adfa74b')
PARAM     = BASE / 'md' / 'param'
SYS_DIR   = BASE / 'md' / 'systems'
RECEPTOR  = BASE / 'md' / 'receptor_nozn.pdb'
SYS_DIR.mkdir(exist_ok=True)

LIGS = ['REF_85C','CPD1','CPD4','CPD7','CPD8','CPD9','CPD10','CPD11','CPD12']

def build_system(lig):
    mol2   = PARAM / lig / f'{lig}.mol2'
    frcmod = PARAM / lig / f'{lig}.frcmod'
    d      = SYS_DIR / lig
    d.mkdir(exist_ok=True)

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
        saveamberparm MOL {d}/system.prmtop {d}/system.inpcrd
        savepdb MOL {d}/system.pdb
        quit
    """)
    leap_in = d / 'tleap.in'
    leap_in.write_text(script)

    r = subprocess.run(['tleap', '-f', str(leap_in)],
                       capture_output=True, text=True, cwd=str(d))
    prmtop = d / 'system.prmtop'
    inpcrd = d / 'system.inpcrd'

    if prmtop.exists() and inpcrd.exists():
        # Count atoms from pdb
        natoms = sum(1 for l in (d/'system.pdb').read_text().splitlines()
                     if l.startswith(('ATOM','HETATM')))
        return lig, True, f'{natoms} atoms, prmtop={prmtop.stat().st_size//1024}KB'
    else:
        # Extract tleap error
        err_lines = [l for l in r.stdout.splitlines() if 'error' in l.lower() or 'fatal' in l.lower() or 'Error' in l]
        return lig, False, '\n'.join(err_lines[-5:]) or r.stdout[-300:]

print("Building AMBER systems with tleap:")
results = []
for lig in LIGS:
    print(f"  {lig} ...", end=' ', flush=True)
    _, ok, msg = build_system(lig)
    results.append((lig, ok, msg))
    print('OK: ' + msg if ok else 'FAIL: ' + msg[:120])

print(f"\n{sum(ok for _,ok,_ in results)}/{len(results)} systems built successfully")
