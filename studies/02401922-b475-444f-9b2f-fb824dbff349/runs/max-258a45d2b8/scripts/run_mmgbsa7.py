#!/usr/bin/env python3
"""
MM/GBSA with correct docked coordinates (final version).
Algorithm:
  mol2 heavy → SDF (proximity <0.001 Å, antechamber preserves coords)
  SDF → input PDBQT (linear_sum_assignment <0.001 Å, same gen3D coords reordered by obabel)
  input PDBQT[j] → docked PDBQT[j] (Vina preserves atom order)
  H atoms: parent_new + (H_old - parent_old)
Then: reuse existing lig.frcmod → tleap rebuild → MMPBSA.py single-frame.
"""
import os, subprocess, json, re
import numpy as np
from collections import defaultdict
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

# ── parsers ────────────────────────────────────────────────────────────────────

def parse_mol2_full(path):
    lines = open(path).readlines()
    in_atom = in_bond = False
    atoms = []; bonds = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s == '@<TRIPOS>ATOM':   in_atom = True;  in_bond = False; continue
        if s == '@<TRIPOS>BOND':   in_bond = True;  in_atom = False; continue
        if s.startswith('@<TRIPOS>'): in_atom = in_bond = False; continue
        if in_atom and s:
            p = line.split()
            if len(p) >= 6:
                atoms.append({'idx': int(p[0]), 'name': p[1],
                               'x': float(p[2]), 'y': float(p[3]), 'z': float(p[4]),
                               'type': p[5], 'rest': p[5:],
                               'is_h': p[5].lower().startswith('h'),
                               'line': i})
        if in_bond and s:
            p = line.split()
            if len(p) >= 3:
                bonds.append((int(p[1]), int(p[2])))
    return lines, atoms, bonds

def parse_sdf_heavy(path):
    lines = open(path).readlines(); n = int(lines[3][:3]); pts = []
    for i in range(4, 4+n):
        p = lines[i].split()
        if len(p) >= 4 and p[3] != 'H':
            pts.append([float(p[0]), float(p[1]), float(p[2])])
    return np.array(pts)

def parse_pdbqt_heavy_nomodel(path):
    c = []
    for line in open(path):
        if line[:6] in ('ATOM  ', 'HETATM') and line[77:79].strip() != 'HD':
            c.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(c)

def parse_pdbqt_first_heavy(path):
    c = []; seen = False
    for line in open(path):
        if line.startswith('MODEL'):
            if seen: break
            seen = True; continue
        if line.startswith('ENDMDL'): break
        if line[:6] in ('ATOM  ', 'HETATM') and line[77:79].strip() != 'HD':
            c.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    return np.array(c)

# ── coordinate update ──────────────────────────────────────────────────────────

def update_mol2_with_docked_coords(mol2_in, sdf_path, in_pdbqt_path,
                                    out_pdbqt_path, mol2_out, log):
    """
    Place mol2 atoms at docked-pose coordinates.
    Heavy atoms: directly from docked PDBQT via mol2→SDF→inPDBQT chain.
    H atoms: follow parent heavy atom (parent_new + H_old - parent_old).
    Returns max heavy-atom displacement from expected docked coords (Å).
    """
    lines, atoms, bonds = parse_mol2_full(mol2_in)
    heavy = [a for a in atoms if not a['is_h']]
    h_list = [a for a in atoms if a['is_h']]

    mol2_heavy_xyz = np.array([[a['x'], a['y'], a['z']] for a in heavy])
    sdf_xyz    = parse_sdf_heavy(sdf_path)
    in_xyz     = parse_pdbqt_heavy_nomodel(in_pdbqt_path)
    docked_xyz = parse_pdbqt_first_heavy(out_pdbqt_path)

    N = len(sdf_xyz)
    assert len(in_xyz) == N and len(docked_xyz) == N and len(mol2_heavy_xyz) == N, \
        f"atom count mismatch: mol2={len(mol2_heavy_xyz)} sdf={N} inpdbqt={len(in_xyz)} out={len(docked_xyz)}"

    # mol2 heavy → SDF (proximity)
    D1 = cdist(mol2_heavy_xyz, sdf_xyz)
    mol2_to_sdf = D1.argmin(axis=1)
    max_d1 = D1[range(N), mol2_to_sdf].max()
    assert max_d1 < 0.01, f"mol2↔SDF mismatch {max_d1:.4f} Å"

    # SDF → input PDBQT (linear_sum_assignment, same gen3D coords reordered by obabel)
    D2 = cdist(sdf_xyz, in_xyz)
    _, sdf_to_pdbqt = linear_sum_assignment(D2)
    max_d2 = D2[range(N), sdf_to_pdbqt].max()
    assert max_d2 < 0.01, f"SDF↔InPDBQT mismatch {max_d2:.4f} Å"

    log.write(f"  mol2↔SDF max: {max_d1:.5f} Å  SDF↔InPDBQT max: {max_d2:.5f} Å\n")

    # Build new coordinates dict (mol2 1-based index → new xyz)
    idx_to_old = {a['idx']: np.array([a['x'], a['y'], a['z']]) for a in atoms}
    idx_to_new = {}
    for k, a in enumerate(heavy):
        idx_to_new[a['idx']] = docked_xyz[sdf_to_pdbqt[mol2_to_sdf[k]]]

    # H: build adjacency, find parent heavy, follow parent
    adj = defaultdict(list)
    for a1, a2 in bonds:
        adj[a1].append(a2)
        adj[a2].append(a1)
    atom_by_idx = {a['idx']: a for a in atoms}
    for a in h_list:
        for nb_idx in adj[a['idx']]:
            if not atom_by_idx[nb_idx]['is_h']:
                p_old = idx_to_old[nb_idx]
                p_new = idx_to_new[nb_idx]
                idx_to_new[a['idx']] = p_new + (idx_to_old[a['idx']] - p_old)
                break
        else:
            idx_to_new[a['idx']] = idx_to_old[a['idx']]  # no parent found, keep original

    # Write updated mol2
    new_lines = list(lines)
    for a in atoms:
        xyz = idx_to_new[a['idx']]
        old = lines[a['line']].split()
        new_line = (f"{old[0]:>7} {old[1]:<4} "
                    f"{xyz[0]:>10.4f} {xyz[1]:>10.4f} {xyz[2]:>10.4f} "
                    + ' '.join(old[5:]) + '\n')
        new_lines[a['line']] = new_line
    with open(mol2_out, 'w') as f:
        f.writelines(new_lines)

    return max_d1, max_d2

# ── main pipeline ──────────────────────────────────────────────────────────────

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run7.log'), 'w', buffering=1)

for name, lig_n, nc in compounds:
    log.write(f"\n=== {name} (lig{lig_n}) ===\n"); log.flush()
    wdir         = os.path.join(mmgbsa_dir, name)
    mol2_orig    = os.path.join(wdir, 'lig.mol2')
    frcmod_orig  = os.path.join(wdir, 'lig.frcmod')
    sdf_path     = os.path.join(ligands_dir, f'lig{lig_n}.sdf')
    in_pdbqt     = os.path.join(ligands_dir, f'lig{lig_n}.pdbqt')
    out_pdbqt    = os.path.join(dock_dir, f'lig{lig_n}_out.pdbqt')

    missing = [f for f, p in [('lig.mol2', mol2_orig), ('lig.frcmod', frcmod_orig),
                                (f'lig{lig_n}.sdf', sdf_path), (f'lig{lig_n}.pdbqt', in_pdbqt),
                                (f'lig{lig_n}_out.pdbqt', out_pdbqt)] if not os.path.exists(p)]
    if missing:
        log.write(f"  MISSING: {missing}\n"); log.flush()
        results[name] = {'error': f'missing {missing}'}
        continue

    # 1. Update mol2 coordinates to docked pose
    mol2_docked = os.path.join(wdir, 'lig_docked.mol2')
    try:
        d1, d2 = update_mol2_with_docked_coords(
            mol2_orig, sdf_path, in_pdbqt, out_pdbqt, mol2_docked, log)
        log.write(f"  mol2 coords updated (d1={d1:.5f}, d2={d2:.5f})\n"); log.flush()
    except Exception as e:
        log.write(f"  MOL2 UPDATE FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'mol2 update: {str(e)[:300]}'}
        continue

    # 2. tleap rebuild
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
    leap_f = os.path.join(wdir, 'tleap_dock.in')
    with open(leap_f, 'w') as f:
        f.write(leap_in)
    try:
        run([tleap_bin, '-f', leap_f], cwd=wdir)
        log.write("  tleap done\n"); log.flush()
    except Exception as e:
        log.write(f"  TLEAP FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'tleap: {str(e)[:400]}'}
        continue

    # 3. MMPBSA.py single-frame
    mmpbsa_in_f = os.path.join(wdir, 'mmpbsa_dock.in')
    dat_f       = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA_dock.dat')
    with open(mmpbsa_in_f, 'w') as f:
        f.write(MMPBSA_IN)
    try:
        run([PYTHON, mmpbsa_bin, '-O',
             '-i',  mmpbsa_in_f, '-o',  dat_f,
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
        txt = open(dat_f).read()
        log.write(f"  dat tail:\n{txt[-500:]}\n"); log.flush()
        dg = None
        for pattern in [r'DELTA Total\s+([-\d.]+)', r'DELTA TOTAL\s+([-\d.]+)']:
            m = re.search(pattern, txt, re.IGNORECASE)
            if m: dg = float(m.group(1)); break
        if dg is None:
            for line in txt.split('\n'):
                if 'TOTAL' in line.upper() and 'DELTA' in line.upper():
                    nums = re.findall(r'-?\d+\.\d+', line)
                    if nums: dg = float(nums[0]); break
        if dg is not None:
            results[name] = {'dg_mmgbsa': dg}
            log.write(f"  ΔG = {dg:.3f} kcal/mol\n"); log.flush()
        else:
            results[name] = {'error': 'parse: no DELTA TOTAL'}
            log.write("  PARSE FAILED: no DELTA TOTAL\n"); log.flush()
    except Exception as e:
        results[name] = {'error': f'parse: {e}'}
        log.write(f"  PARSE ERROR: {e}\n"); log.flush()

with open(os.path.join(mmgbsa_dir, 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
