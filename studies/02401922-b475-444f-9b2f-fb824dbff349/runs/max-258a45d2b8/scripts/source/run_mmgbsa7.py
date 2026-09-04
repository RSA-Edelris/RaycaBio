#!/usr/bin/env python3
"""
MM/GBSA with correct docked coordinates.
Chain: mol2 heavy → SDF (proximity) → input PDBQT (linear_sum_assignment) → docked PDBQT (same index)
Kabsch rigid fit mol2 → docked reference; apply to all atoms including H.
Then: parmchk2 reuses existing frcmod → tleap rebuild → MMPBSA.py single-frame.
"""
import os, subprocess, json, re, shutil
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment

BASE         = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
ligands_dir  = os.path.join(BASE, 'ligands_3d')
dock_dir     = os.path.join(BASE, 'docking_results')
mmgbsa_dir   = os.path.join(BASE, 'mmgbsa')
receptor_pdb = os.path.join(BASE, 'receptor_ab.pdb')

AMBER       = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin'
PYTHON      = os.path.join(AMBER, 'python')
tleap_bin   = os.path.join(AMBER, 'tleap')
mmpbsa_bin  = os.path.join(AMBER, 'MMPBSA.py')
AMBERHOME   = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
ENV = {**os.environ, 'AMBERHOME': AMBERHOME}

compounds = [
    ('CTX-1020521', 61, +1), ('CTX-1020520', 62, +1), ('CTX-1020810', 12, +1),
    ('CTX-1019660', 77, +1), ('CTX-1020458', 68, +1), ('CTX-1019813', 74, +1),
    ('CTX-1020882',  4, +1), ('CTX-1020555', 59, +1), ('CTX-1020816', 10, +1),
    ('CTX-1020751', 27,  0), ('CTX-1017233', 84, +1),
]

MMPBSA_IN = """Input file for running GB
&general
 startframe=1, endframe=1, verbose=2,
/
&gb
 igb=5, saltcon=0.150,
/
"""

def run(cmd, cwd=None, timeout=600, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, env=ENV)
    if check and r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(str(cmd[0]))} rc={r.returncode}\n"
                           f"STDERR:{r.stderr[-1500:]}\nSTDOUT:{r.stdout[-500:]}")
    return r

# ── coordinate parsers ────────────────────────────────────────────────────────

def parse_mol2(path):
    lines = open(path).readlines()
    in_atom = False
    atoms = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '@<TRIPOS>ATOM': in_atom = True; continue
        if in_atom and s.startswith('@'): in_atom = False
        if in_atom and s:
            p = line.split()
            if len(p) >= 6:
                atype = p[5].lower()
                is_h = atype.startswith('h')
                atoms.append({'idx': len(atoms), 'line': i, 'name': p[1],
                               'x': float(p[2]), 'y': float(p[3]), 'z': float(p[4]),
                               'is_h': is_h, 'raw': line})
    return lines, atoms

def parse_sdf_heavy(path):
    lines = open(path).readlines()
    n = int(lines[3][:3])
    pts = []
    for i in range(4, 4+n):
        p = lines[i].split()
        if len(p) >= 4 and p[3] != 'H':
            pts.append([float(p[0]), float(p[1]), float(p[2])])
    return np.array(pts)

def parse_pdbqt_heavy_nomodel(path):
    """Input PDBQT (no MODEL): skip HD."""
    coords = []
    for line in open(path):
        if line[:6] in ('ATOM  ', 'HETATM'):
            ad = line[77:79].strip()
            if ad == 'HD': continue
            coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords)

def parse_pdbqt_first_heavy(path):
    """Output PDBQT (MODEL tags): first model, skip HD."""
    coords = []; seen = False
    for line in open(path):
        if line.startswith('MODEL'):
            if seen: break
            seen = True; continue
        if line.startswith('ENDMDL'): break
        if line[:6] in ('ATOM  ', 'HETATM'):
            ad = line[77:79].strip()
            if ad == 'HD': continue
            coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(coords)

def kabsch(ref, mob):
    """R, t: minimise ||ref - (R@mob[i]+t)||²"""
    cr, cm = ref.mean(0), mob.mean(0)
    A = (ref-cr).T @ (mob-cm)
    U, S, Vt = np.linalg.svd(A)
    d = np.linalg.det(U @ Vt)
    R = U @ np.diag([1, 1, d]) @ Vt
    t = cr - R @ cm
    return R, t

def update_mol2_with_docked_coords(mol2_in, sdf_path, in_pdbqt_path, out_pdbqt_path, mol2_out, log):
    """
    Update mol2_in coordinates to match first docked pose.
    Returns post-fit RMSD on heavy atoms (Å).
    """
    lines, atoms = parse_mol2(mol2_in)
    heavy = [a for a in atoms if not a['is_h']]
    mol2_xyz = np.array([[a['x'], a['y'], a['z']] for a in heavy])

    sdf_xyz    = parse_sdf_heavy(sdf_path)
    in_xyz     = parse_pdbqt_heavy_nomodel(in_pdbqt_path)
    docked_xyz = parse_pdbqt_first_heavy(out_pdbqt_path)

    N = len(sdf_xyz)
    assert len(in_xyz) == N, f"Input PDBQT {len(in_xyz)} vs SDF {N}"
    assert len(docked_xyz) == N, f"Output PDBQT {len(docked_xyz)} vs SDF {N}"
    assert len(mol2_xyz) == N, f"mol2 heavy {len(mol2_xyz)} vs SDF {N}"

    # 1. mol2 heavy → SDF index (antechamber preserves XYZ from SDF → match by proximity)
    D1 = cdist(mol2_xyz, sdf_xyz)
    mol2_to_sdf = D1.argmin(axis=1)
    d1 = D1[range(N), mol2_to_sdf]
    assert d1.max() < 0.01, f"mol2↔SDF coord mismatch: max {d1.max():.4f} Å"
    log.write(f"  mol2↔SDF max dist: {d1.max():.5f} Å\n"); log.flush()

    # 2. SDF → input PDBQT (same gen3D coords, reordered by obabel → use linear_sum_assignment)
    D2 = cdist(sdf_xyz, in_xyz)
    _, sdf_to_pdbqt = linear_sum_assignment(D2)
    d2 = D2[range(N), sdf_to_pdbqt]
    assert d2.max() < 0.01, f"SDF↔InPDBQT coord mismatch: max {d2.max():.4f} Å"
    log.write(f"  SDF↔InPDBQT max dist: {d2.max():.5f} Å\n"); log.flush()

    # 3. Build reference docked coords for each mol2 heavy atom
    ref = np.array([docked_xyz[sdf_to_pdbqt[mol2_to_sdf[k]]] for k in range(N)])

    # 4. Kabsch: fit mol2_xyz → ref
    R, t = kabsch(ref, mol2_xyz)

    # 5. Apply to all atoms
    for a in atoms:
        xyz = np.array([a['x'], a['y'], a['z']])
        new = R @ xyz + t
        a['x'], a['y'], a['z'] = new

    # 6. Verify RMSD on heavy atoms
    new_heavy = np.array([[a['x'], a['y'], a['z']] for a in atoms if not a['is_h']])
    rmsd = float(np.sqrt(np.mean(np.sum((ref - new_heavy)**2, axis=1))))

    # 7. Write updated mol2
    new_lines = list(lines)
    for a in atoms:
        old = lines[a['line']].split()
        new_line = (f"{old[0]:>7} {old[1]:<4} "
                    f"{a['x']:>10.4f} {a['y']:>10.4f} {a['z']:>10.4f} "
                    + ' '.join(old[5:]) + '\n')
        new_lines[a['line']] = new_line

    with open(mol2_out, 'w') as f:
        f.writelines(new_lines)

    return rmsd

# ── main pipeline ─────────────────────────────────────────────────────────────

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run7.log'), 'w', buffering=1)

for name, lig_n, nc in compounds:
    log.write(f"\n=== {name} (lig{lig_n}) ===\n"); log.flush()
    wdir = os.path.join(mmgbsa_dir, name)
    os.makedirs(wdir, exist_ok=True)

    mol2_orig      = os.path.join(wdir, 'lig.mol2')
    frcmod_orig    = os.path.join(wdir, 'lig.frcmod')
    sdf_path       = os.path.join(ligands_dir, f'lig{lig_n}.sdf')
    in_pdbqt_path  = os.path.join(ligands_dir, f'lig{lig_n}.pdbqt')
    out_pdbqt_path = os.path.join(dock_dir, f'lig{lig_n}_out.pdbqt')

    for f, p in [('lig.mol2', mol2_orig), ('lig.frcmod', frcmod_orig),
                 (f'lig{lig_n}.sdf', sdf_path), (f'lig{lig_n}.pdbqt', in_pdbqt_path),
                 (f'lig{lig_n}_out.pdbqt', out_pdbqt_path)]:
        if not os.path.exists(p):
            log.write(f"  MISSING {f}\n"); log.flush()
            results[name] = {'error': f'missing {f}'}
            break
    else:
        # 1. Update mol2 with docked coordinates
        mol2_docked = os.path.join(wdir, 'lig_docked.mol2')
        try:
            rmsd = update_mol2_with_docked_coords(
                mol2_orig, sdf_path, in_pdbqt_path, out_pdbqt_path, mol2_docked, log)
            log.write(f"  Kabsch RMSD = {rmsd:.4f} Å\n"); log.flush()
            if rmsd > 1.0:
                log.write(f"  WARNING: RMSD > 1 Å — coordinate placement may be poor\n")
        except Exception as e:
            log.write(f"  MOL2 UPDATE FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'mol2 update: {str(e)[:300]}'}
            continue

        # 2. tleap — rebuild complex with docked ligand mol2
        leap_in = f"""source leaprc.protein.ff14SB
source leaprc.gaff2
loadAmberParams {frcmod_orig}
LIG = loadmol2 {mol2_docked}
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
            r = run([tleap_bin, '-f', os.path.join(wdir, 'tleap_dock.in')], cwd=wdir)
            log.write("  tleap done\n"); log.flush()
        except Exception as e:
            log.write(f"  TLEAP FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'tleap: {str(e)[:400]}'}
            continue

        # 3. MMPBSA.py single-frame (no sander — complex too large for GB minimize in time)
        mmpbsa_in_path = os.path.join(wdir, 'mmpbsa_dock.in')
        dat_path       = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA_dock.dat')
        with open(mmpbsa_in_path, 'w') as f:
            f.write(MMPBSA_IN)
        try:
            run([PYTHON, mmpbsa_bin, '-O',
                 '-i',  mmpbsa_in_path,
                 '-o',  dat_path,
                 '-cp', os.path.join(wdir, 'complex_dock.prmtop'),
                 '-rp', os.path.join(wdir, 'rec_dock.prmtop'),
                 '-lp', os.path.join(wdir, 'lig_dock.prmtop'),
                 '-y',  os.path.join(wdir, 'complex_dock.rst7')],
                cwd=wdir, timeout=600)
            log.write("  MMPBSA.py done\n"); log.flush()
        except Exception as e:
            log.write(f"  MMPBSA FAILED: {e}\n"); log.flush()
            results[name] = {'error': f'mmpbsa: {str(e)[:400]}'}
            continue

        # 4. Parse ΔG
        try:
            txt = open(dat_path).read()
            log.write(f"  tail:\n{txt[-600:]}\n"); log.flush()
            m = re.search(r'DELTA Total\s+([-\d.]+)', txt, re.IGNORECASE)
            if not m:
                m = re.search(r'DELTA TOTAL\s+([-\d.]+)', txt, re.IGNORECASE)
            if not m:
                for line in txt.split('\n'):
                    if 'TOTAL' in line.upper() and 'DELTA' in line.upper():
                        nums = re.findall(r'-?\d+\.\d+', line)
                        if nums:
                            dg = float(nums[0])
                            results[name] = {'dg_mmgbsa': dg, 'kabsch_rmsd': rmsd}
                            log.write(f"  ΔG = {dg:.3f} kcal/mol\n"); log.flush()
                            m = 'found'
                            break
            if m and m != 'found':
                dg = float(m.group(1))
                results[name] = {'dg_mmgbsa': dg, 'kabsch_rmsd': rmsd}
                log.write(f"  ΔG = {dg:.3f} kcal/mol\n"); log.flush()
            elif not m:
                results[name] = {'error': 'parse: no DELTA TOTAL', 'kabsch_rmsd': rmsd}
        except Exception as e:
            results[name] = {'error': f'parse: {e}', 'kabsch_rmsd': rmsd}
            log.write(f"  PARSE ERROR: {e}\n"); log.flush()

with open(os.path.join(mmgbsa_dir, 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
