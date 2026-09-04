#!/usr/bin/env python3
"""
MM/GBSA with docked coordinates.
- Extract first Vina pose → SDF (with all H via obabel -h)
- antechamber with -c gas (Gasteiger, instant) + gaff2 types
- parmchk2 → tleap → 50-step minimize (cut=12.0) → MMPBSA.py
"""
import os, subprocess, json, re, shutil

BASE        = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
dock_dir    = os.path.join(BASE, 'docking_results')
mmgbsa_dir  = os.path.join(BASE, 'mmgbsa')
receptor_pdb = os.path.join(BASE, 'receptor_ab.pdb')

AMBER       = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin'
PYTHON      = os.path.join(AMBER, 'python')
obabel      = '/usr/bin/obabel'
antechamber = os.path.join(AMBER, 'antechamber')
parmchk2    = os.path.join(AMBER, 'parmchk2')
tleap       = os.path.join(AMBER, 'tleap')
sander      = os.path.join(AMBER, 'sander')
mmpbsa_bin  = os.path.join(AMBER, 'MMPBSA.py')
AMBERHOME   = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
ENV = {**os.environ, 'AMBERHOME': AMBERHOME}

compounds = [
    ('CTX-1020521', 61, +1), ('CTX-1020520', 62, +1), ('CTX-1020810', 12, +1),
    ('CTX-1019660', 77, +1), ('CTX-1020458', 68, +1), ('CTX-1019813', 74, +1),
    ('CTX-1020882',  4, +1), ('CTX-1020555', 59, +1), ('CTX-1020816', 10, +1),
    ('CTX-1020751', 27,  0), ('CTX-1017233', 84, +1),
]

MIN_IN = """Minimization
&cntrl
 imin=1, maxcyc=50, ncyc=25,
 ntb=0, igb=5, cut=12.0,
/
"""

MMPBSA_IN = """Input file for running GB
&general
 startframe=1, endframe=1, verbose=2,
/
&gb
 igb=5, saltcon=0.150,
/
"""

def run(cmd, cwd=None, timeout=300, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, env=ENV)
    if check and r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(str(cmd[0]))} rc={r.returncode}\n"
                           f"STDERR:{r.stderr[-1500:]}")
    return r

def extract_first_pose_sdf(pdbqt_in, sdf_out):
    """Extract first MODEL from Vina PDBQT, save as pdbqt, convert to SDF with H."""
    lines = open(pdbqt_in).readlines()
    pose1 = []
    for l in lines:
        if l.startswith('MODEL') and pose1:
            break
        pose1.append(l)
    if not any(l.startswith('ENDMDL') for l in pose1):
        pose1.append('ENDMDL\n')
    tmp = sdf_out.replace('.sdf', '_p1.pdbqt')
    with open(tmp, 'w') as f:
        f.writelines(pose1)
    # Convert PDBQT → SDF, add all H (-h), best 3D geometry
    run([obabel, tmp, '-O', sdf_out, '-h'], env=ENV)

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run6.log'), 'w', buffering=1)

for name, lig_n, nc in compounds:
    log.write(f"\n=== {name} (lig{lig_n}, nc={nc:+d}) ===\n"); log.flush()
    wdir = os.path.join(mmgbsa_dir, name)
    os.makedirs(wdir, exist_ok=True)

    pdbqt_docked = os.path.join(dock_dir, f'lig{lig_n}_out.pdbqt')
    if not os.path.exists(pdbqt_docked):
        log.write("  MISSING docked pdbqt\n"); log.flush()
        results[name] = {'error': 'missing pdbqt'}
        continue

    # 1. Extract first docked pose → SDF with all H
    docked_sdf = os.path.join(wdir, 'lig_docked.sdf')
    try:
        extract_first_pose_sdf(pdbqt_docked, docked_sdf)
        log.write("  pose extracted → SDF\n"); log.flush()
    except Exception as e:
        log.write(f"  POSE EXTRACT FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'pose: {e}'}
        continue

    # 2. antechamber with Gasteiger (instant), gaff2 types
    mol2 = os.path.join(wdir, 'lig_dock_gas.mol2')
    try:
        run([antechamber,
             '-i', docked_sdf, '-fi', 'sdf',
             '-o', mol2, '-fo', 'mol2',
             '-c', 'gas', '-at', 'gaff2',
             '-nc', str(nc), '-pf', 'yes', '-s', '2'],
            cwd=wdir, timeout=60)
        log.write("  antechamber (Gasteiger) done\n"); log.flush()
    except Exception as e:
        log.write(f"  ANTECHAMBER FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'antechamber: {str(e)[:300]}'}
        continue

    # 3. parmchk2
    frcmod = os.path.join(wdir, 'lig_dock_gas.frcmod')
    try:
        run([parmchk2, '-i', mol2, '-f', 'mol2', '-o', frcmod, '-s', 'gaff2'],
            cwd=wdir, timeout=60)
        log.write("  parmchk2 done\n"); log.flush()
    except Exception as e:
        log.write(f"  PARMCHK2 FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'parmchk2: {str(e)[:200]}'}
        continue

    # 4. tleap — build complex with docked ligand coordinates
    leap_in = f"""source leaprc.protein.ff14SB
source leaprc.gaff2
loadAmberParams {frcmod}
LIG = loadmol2 {mol2}
REC = loadpdb {receptor_pdb}
COM = combine {{REC LIG}}
saveamberparm LIG {wdir}/lig_dock.prmtop {wdir}/lig_dock.rst7
saveamberparm REC {wdir}/rec_dock.prmtop {wdir}/rec_dock.rst7
saveamberparm COM {wdir}/complex_dock.prmtop {wdir}/complex_dock.rst7
quit
"""
    with open(os.path.join(wdir, 'tleap_dock.in'), 'w') as f:
        f.write(leap_in)
    try:
        run([tleap, '-f', os.path.join(wdir, 'tleap_dock.in')], cwd=wdir)
        log.write("  tleap done\n"); log.flush()
    except Exception as e:
        log.write(f"  TLEAP FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'tleap: {str(e)[:300]}'}
        continue

    # 5. Sander minimize — 50 steps, cut=12.0
    with open(os.path.join(wdir, 'min_dock.in'), 'w') as f:
        f.write(MIN_IN)
    min_rst = os.path.join(wdir, 'min_dock.rst7')
    try:
        run([sander, '-O',
             '-i',   os.path.join(wdir, 'min_dock.in'),
             '-o',   os.path.join(wdir, 'min_dock.out'),
             '-p',   os.path.join(wdir, 'complex_dock.prmtop'),
             '-c',   os.path.join(wdir, 'complex_dock.rst7'),
             '-r',   min_rst,
             '-ref', os.path.join(wdir, 'complex_dock.rst7')],
            cwd=wdir, timeout=120)
        log.write("  sander 50 steps done\n"); log.flush()
    except subprocess.TimeoutExpired:
        log.write("  SANDER TIMEOUT — using unminimized\n"); log.flush()
        shutil.copy(os.path.join(wdir, 'complex_dock.rst7'), min_rst)
    except Exception as e:
        log.write(f"  SANDER FAILED — using unminimized: {e}\n"); log.flush()
        shutil.copy(os.path.join(wdir, 'complex_dock.rst7'), min_rst)

    # 6. MMPBSA.py
    with open(os.path.join(wdir, 'mmpbsa_dock.in'), 'w') as f:
        f.write(MMPBSA_IN)
    dat = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA_dock.dat')
    try:
        run([PYTHON, mmpbsa_bin, '-O',
             '-i',  os.path.join(wdir, 'mmpbsa_dock.in'),
             '-o',  dat,
             '-cp', os.path.join(wdir, 'complex_dock.prmtop'),
             '-rp', os.path.join(wdir, 'rec_dock.prmtop'),
             '-lp', os.path.join(wdir, 'lig_dock.prmtop'),
             '-y',  min_rst],
            cwd=wdir, timeout=600)
        log.write("  MMPBSA.py done\n"); log.flush()
    except Exception as e:
        log.write(f"  MMPBSA FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'mmpbsa: {str(e)[:400]}'}
        continue

    # 7. Parse ΔG
    try:
        txt = open(dat).read()
        log.write(f"  tail:\n{txt[-500:]}\n"); log.flush()
        m = re.search(r'DELTA TOTAL\s+([-\d.]+)', txt, re.IGNORECASE)
        if not m:
            for line in txt.split('\n'):
                if 'TOTAL' in line.upper() and 'DELTA' in line.upper():
                    nums = re.findall(r'-?\d+\.\d+', line)
                    if nums:
                        results[name] = {'dg_mmgbsa': float(nums[0]), 'charge': 'gasteiger'}
                        log.write(f"  ΔG = {nums[0]} kcal/mol\n"); log.flush()
                        m = 'found'
                        break
        if m and m != 'found':
            results[name] = {'dg_mmgbsa': float(m.group(1)), 'charge': 'gasteiger'}
            log.write(f"  ΔG = {m.group(1)} kcal/mol\n"); log.flush()
        elif not m:
            results[name] = {'error': 'parse: no DELTA TOTAL'}
    except Exception as e:
        results[name] = {'error': f'parse: {e}'}
        log.write(f"  PARSE ERROR: {e}\n"); log.flush()

with open(os.path.join(mmgbsa_dir, 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
