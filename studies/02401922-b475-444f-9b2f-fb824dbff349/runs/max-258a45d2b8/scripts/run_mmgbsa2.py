#!/usr/bin/env python3
"""MM/GBSA pipeline — revised with longer timeouts (antechamber 1800s)."""
import os, subprocess, shutil, json, re, sys

BASE = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
ligands_dir = os.path.join(BASE, 'ligands_3d')
mmgbsa_dir  = os.path.join(BASE, 'mmgbsa')
receptor_pdb = os.path.join(BASE, 'receptor_ab.pdb')

AMBER = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin'
antechamber = os.path.join(AMBER, 'antechamber')
parmchk2    = os.path.join(AMBER, 'parmchk2')
tleap       = os.path.join(AMBER, 'tleap')
sander      = os.path.join(AMBER, 'sander')
mmpbsa      = os.path.join(AMBER, 'MMPBSA.py')

compounds = [
    ('CTX-1020521', 61, +1), ('CTX-1020520', 62, +1), ('CTX-1020810', 12, +1),
    ('CTX-1019660', 77, +1), ('CTX-1020458', 68, +1), ('CTX-1019813', 74, +1),
    ('CTX-1020882',  4, +1), ('CTX-1020555', 59, +1), ('CTX-1020816', 10, +1),
    ('CTX-1020751', 27,  0), ('CTX-1017233', 84, +1),
]

min_in = """Minimization
&cntrl
 imin=1, maxcyc=1500, ncyc=500,
 ntb=0, igb=5, cut=999.0,
/
"""

mmpbsa_in = """Input file for running PB and GB
&general
 endframe=1, verbose=1,
/
&gb
 igb=5, saltcon=0.150,
/
"""

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run2.log'), 'w', buffering=1)

def run(cmd, cwd=None, timeout=300, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"cmd {cmd[0]} failed rc={r.returncode}\n{r.stderr[-2000:]}")
    return r

for name, lig_n, nc in compounds:
    log.write(f"\n=== {name} (lig{lig_n}, nc={nc:+d}) ===\n"); log.flush()
    wdir = os.path.join(mmgbsa_dir, name)
    os.makedirs(wdir, exist_ok=True)
    lig_sdf = os.path.join(ligands_dir, f'lig{lig_n}.sdf')

    # 1. antechamber — AM1-BCC, gaff2; long timeout for large aromatic systems
    mol2 = os.path.join(wdir, 'lig.mol2')
    try:
        log.write("  antechamber AM1-BCC...\n"); log.flush()
        run([antechamber, '-i', lig_sdf, '-fi', 'sdf',
             '-o', mol2, '-fo', 'mol2',
             '-c', 'bcc', '-s', '2', '-nc', str(nc),
             '-pf', 'yes', '-at', 'gaff2'],
            cwd=wdir, timeout=1800)
        log.write("  antechamber done\n"); log.flush()
    except Exception as e:
        log.write(f"  ANTECHAMBER FAILED: {e}\n"); log.flush()
        results[name] = {'error': 'antechamber failed'}
        continue

    # 2. parmchk2 frcmod
    frcmod = os.path.join(wdir, 'lig.frcmod')
    try:
        run([parmchk2, '-i', mol2, '-f', 'mol2', '-o', frcmod, '-s', 'gaff2'], cwd=wdir)
        log.write("  parmchk2 done\n"); log.flush()
    except Exception as e:
        log.write(f"  PARMCHK2 FAILED: {e}\n"); log.flush()
        results[name] = {'error': 'parmchk2 failed'}
        continue

    # 3. tleap — build receptor+ligand complex
    leap_in = f"""source leaprc.protein.ff14SB
source leaprc.gaff2
loadAmberParams {frcmod}
LIG = loadmol2 {mol2}
REC = loadpdb {receptor_pdb}
COM = combine {{REC LIG}}
saveamberparm LIG {wdir}/lig.prmtop {wdir}/lig.rst7
saveamberparm REC {wdir}/rec.prmtop {wdir}/rec.rst7
saveamberparm COM {wdir}/complex.prmtop {wdir}/complex.rst7
quit
"""
    with open(os.path.join(wdir, 'tleap.in'), 'w') as f:
        f.write(leap_in)
    try:
        run([tleap, '-f', os.path.join(wdir, 'tleap.in')], cwd=wdir)
        log.write("  tleap done\n"); log.flush()
    except Exception as e:
        log.write(f"  TLEAP FAILED: {e}\n"); log.flush()
        results[name] = {'error': 'tleap failed'}
        continue

    # 4. sander minimization (implicit GB, dry complex)
    with open(os.path.join(wdir, 'min.in'), 'w') as f:
        f.write(min_in)
    try:
        run([sander, '-O',
             '-i', os.path.join(wdir, 'min.in'),
             '-o', os.path.join(wdir, 'min.out'),
             '-p', os.path.join(wdir, 'complex.prmtop'),
             '-c', os.path.join(wdir, 'complex.rst7'),
             '-r', os.path.join(wdir, 'min.rst7'),
             '-ref', os.path.join(wdir, 'complex.rst7')],
            cwd=wdir, timeout=600)
        log.write("  sander minimize done\n"); log.flush()
    except Exception as e:
        log.write(f"  SANDER FAILED: {e}\n"); log.flush()
        results[name] = {'error': 'sander failed'}
        continue

    # 5. MMPBSA.py
    with open(os.path.join(wdir, 'mmpbsa.in'), 'w') as f:
        f.write(mmpbsa_in)
    try:
        PYTHON = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/python'
        run([PYTHON, mmpbsa, '-O',
             '-i', os.path.join(wdir, 'mmpbsa.in'),
             '-o', os.path.join(wdir, 'FINAL_RESULTS_MMGBSA.dat'),
             '-cp', os.path.join(wdir, 'complex.prmtop'),
             '-rp', os.path.join(wdir, 'rec.prmtop'),
             '-lp', os.path.join(wdir, 'lig.prmtop'),
             '-y',  os.path.join(wdir, 'min.rst7')],
            cwd=wdir, timeout=300)
        log.write("  MMPBSA.py done\n"); log.flush()
    except Exception as e:
        log.write(f"  MMPBSA FAILED: {e}\n"); log.flush()
        results[name] = {'error': 'mmpbsa failed'}
        continue

    # 6. Parse result
    dat = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA.dat')
    try:
        txt = open(dat).read()
        m = re.search(r'ΔTOTAL\s+([-\d.]+)\s+\+/-\s+([-\d.]+)', txt)
        if not m:
            m = re.search(r'DELTA TOTAL\s+([-\d.]+)\s+\+/-\s+([-\d.]+)', txt)
        if not m:
            # try line-by-line
            for line in txt.split('\n'):
                if 'TOTAL' in line and 'DELTA' in line.upper():
                    parts = line.split()
                    for i,p in enumerate(parts):
                        try:
                            float(p)
                            m = type('M', (), {'group': lambda self,n: parts[i] if n==1 else parts[i+2]})()
                            break
                        except: pass
        dg = float(m.group(1))
        log.write(f"  ΔG_MMGBSA = {dg:.2f} kcal/mol\n"); log.flush()
        results[name] = {'dg_mmgbsa': dg, 'lig_n': lig_n, 'nc': nc}
    except Exception as e:
        log.write(f"  PARSE FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'parse failed: {e}'}

# Save JSON
with open(os.path.join(BASE, 'mmgbsa', 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
