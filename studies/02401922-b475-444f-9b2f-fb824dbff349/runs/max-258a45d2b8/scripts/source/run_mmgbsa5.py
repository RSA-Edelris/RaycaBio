#!/usr/bin/env python3
"""
MM/GBSA with correct docked coordinates.
1. Extract first Vina pose → update antechamber mol2 XYZ (charges/types stay).
2. Rebuild tleap complex.
3. Brief minimize (50 steps, cut=12.0).
4. MMPBSA.py single-frame.
"""
import os, subprocess, json, re
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolAlign

BASE        = '/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a'
ligands_dir = os.path.join(BASE, 'ligands_3d')
dock_dir    = os.path.join(BASE, 'docking_results')
mmgbsa_dir  = os.path.join(BASE, 'mmgbsa')
receptor_pdb = os.path.join(BASE, 'receptor_ab.pdb')

AMBER   = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin'
OBABEL  = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca/bin/obabel'
PYTHON  = os.path.join(AMBER, 'python')
tleap   = os.path.join(AMBER, 'tleap')
sander  = os.path.join(AMBER, 'sander')
mmpbsa  = os.path.join(AMBER, 'MMPBSA.py')
AMBERHOME = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'
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

def run(cmd, cwd=None, timeout=300, env=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, env=env or ENV)
    if r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(str(cmd[0]))} rc={r.returncode}\n"
                           f"STDERR:{r.stderr[-1500:]}\nSTDOUT:{r.stdout[-500:]}")
    return r

def extract_first_pose(pdbqt_in, sdf_out):
    """Extract first model from Vina PDBQT → SDF."""
    lines = open(pdbqt_in).readlines()
    first = []
    for l in lines:
        if l.startswith('MODEL') and first:
            break
        first.append(l)
    tmp_pdbqt = sdf_out.replace('.sdf', '_pose1.pdbqt')
    with open(tmp_pdbqt, 'w') as f:
        f.writelines(first)
    run([OBABEL, tmp_pdbqt, '-O', sdf_out, '-h'], env=ENV)
    return sdf_out

def update_mol2_coords(mol2_in, docked_sdf, mol2_out, log):
    """
    Replace XYZ in mol2_in with coords from docked_sdf, preserving
    GAFF2 atom types and AM1-BCC charges. Uses RDKit MCS for safe mapping.
    """
    mol_ref = Chem.MolFromMol2File(mol2_in, removeHs=False)
    mol_docked = Chem.SDMolSupplier(docked_sdf, removeHs=False)[0]

    if mol_ref is None or mol_docked is None:
        raise ValueError(f"RDKit failed to read mol2 or docked SDF")

    # Try direct heavy-atom match (same molecule, same topology)
    ref_h = Chem.RemoveHs(mol_ref)
    doc_h = Chem.RemoveHs(mol_docked)

    match = mol_ref.GetSubstructMatch(doc_h)
    if not match or len(match) != doc_h.GetNumAtoms():
        # fallback: match via MCS on heavy atoms
        from rdkit.Chem import rdFMCS
        res = rdFMCS.FindMCS([ref_h, doc_h])
        patt = Chem.MolFromSmarts(res.smartsString)
        m1 = mol_ref.GetSubstructMatch(patt)
        m2 = mol_docked.GetSubstructMatch(patt)
        if not m1 or not m2:
            raise ValueError("MCS match failed")
        # build mapping ref_atom_idx -> docked_atom_idx
        mapping = {m1[i]: m2[i] for i in range(len(m1))}
    else:
        mapping = {match[i]: i for i in range(len(match))}

    conf_ref = mol_ref.GetConformer()
    conf_doc = mol_docked.GetConformer()

    # Update positions for matched atoms
    from rdkit.Geometry import rdGeometry
    for ref_idx, doc_idx in mapping.items():
        pos = conf_doc.GetAtomPosition(doc_idx)
        conf_ref.SetAtomPosition(ref_idx, pos)

    log.write(f"    matched {len(mapping)} atoms\n"); log.flush()

    # Now write updated mol2: read original, replace XYZ section
    lines = open(mol2_in).readlines()
    in_atom = False
    atom_lines = []
    out_lines = []
    atom_idx = 0  # 1-based in mol2

    for line in lines:
        if line.strip() == '@<TRIPOS>ATOM':
            in_atom = True
            out_lines.append(line)
            continue
        if in_atom and line.strip().startswith('@'):
            in_atom = False
        if in_atom:
            parts = line.split()
            if len(parts) >= 6:
                # mol2: id name x y z type [subst_id subst_name charge]
                rid = atom_idx  # 0-based
                try:
                    pos = conf_ref.GetAtomPosition(rid)
                    parts[2] = f'{pos.x:.4f}'
                    parts[3] = f'{pos.y:.4f}'
                    parts[4] = f'{pos.z:.4f}'
                except Exception:
                    pass
                atom_idx += 1
                # reconstruct with fixed-width
                new_line = (f"{parts[0]:>7} {parts[1]:<4} "
                            f"{parts[2]:>10} {parts[3]:>10} {parts[4]:>10} "
                            + ' '.join(parts[5:]) + '\n')
                out_lines.append(new_line)
            else:
                out_lines.append(line)
                atom_idx += 1
        else:
            out_lines.append(line)

    with open(mol2_out, 'w') as f:
        f.writelines(out_lines)

results = {}
log = open(os.path.join(BASE, 'mmgbsa_run5.log'), 'w', buffering=1)

for name, lig_n, nc in compounds:
    log.write(f"\n=== {name} (lig{lig_n}) ===\n"); log.flush()
    wdir = os.path.join(mmgbsa_dir, name)
    os.makedirs(wdir, exist_ok=True)

    mol2_orig = os.path.join(wdir, 'lig.mol2')
    pdbqt_docked = os.path.join(dock_dir, f'lig{lig_n}_out.pdbqt')

    if not os.path.exists(mol2_orig):
        log.write("  MISSING lig.mol2\n"); log.flush()
        results[name] = {'error': 'missing mol2'}
        continue
    if not os.path.exists(pdbqt_docked):
        log.write("  MISSING docked pdbqt\n"); log.flush()
        results[name] = {'error': 'missing pdbqt'}
        continue

    # 1. Extract first pose → SDF
    docked_sdf = os.path.join(wdir, 'lig_docked_pose1.sdf')
    try:
        extract_first_pose(pdbqt_docked, docked_sdf)
        log.write("  first pose extracted\n"); log.flush()
    except Exception as e:
        log.write(f"  POSE EXTRACT FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'pose extract: {e}'}
        continue

    # 2. Update mol2 coordinates
    mol2_docked = os.path.join(wdir, 'lig_docked.mol2')
    try:
        update_mol2_coords(mol2_orig, docked_sdf, mol2_docked, log)
        log.write("  mol2 coords updated\n"); log.flush()
    except Exception as e:
        log.write(f"  MOL2 UPDATE FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'mol2 update: {e}'}
        continue

    # 3. tleap rebuild with docked mol2
    leap_in = f"""source leaprc.protein.ff14SB
source leaprc.gaff2
loadAmberParams {wdir}/lig.frcmod
LIG = loadmol2 {mol2_docked}
REC = loadpdb {receptor_pdb}
COM = combine {{REC LIG}}
saveamberparm LIG {wdir}/lig_dock.prmtop {wdir}/lig_dock.rst7
saveamberparm REC {wdir}/rec.prmtop {wdir}/rec.rst7
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

    # 4. Sander minimize — 50 steps, cut=12.0 (fast clash relief)
    with open(os.path.join(wdir, 'min_dock.in'), 'w') as f:
        f.write(MIN_IN)
    try:
        run([sander, '-O',
             '-i',   os.path.join(wdir, 'min_dock.in'),
             '-o',   os.path.join(wdir, 'min_dock.out'),
             '-p',   os.path.join(wdir, 'complex_dock.prmtop'),
             '-c',   os.path.join(wdir, 'complex_dock.rst7'),
             '-r',   os.path.join(wdir, 'min_dock.rst7'),
             '-ref', os.path.join(wdir, 'complex_dock.rst7')],
            cwd=wdir, timeout=120)
        log.write("  sander minimize done\n"); log.flush()
    except subprocess.TimeoutExpired:
        log.write("  SANDER TIMEOUT — using unminimized\n"); log.flush()
        import shutil
        shutil.copy(os.path.join(wdir, 'complex_dock.rst7'),
                    os.path.join(wdir, 'min_dock.rst7'))
    except Exception as e:
        log.write(f"  SANDER FAILED: {e}\n"); log.flush()
        import shutil
        shutil.copy(os.path.join(wdir, 'complex_dock.rst7'),
                    os.path.join(wdir, 'min_dock.rst7'))

    # 5. MMPBSA.py
    with open(os.path.join(wdir, 'mmpbsa_dock.in'), 'w') as f:
        f.write(MMPBSA_IN)
    try:
        run([PYTHON, mmpbsa, '-O',
             '-i',  os.path.join(wdir, 'mmpbsa_dock.in'),
             '-o',  os.path.join(wdir, 'FINAL_RESULTS_MMGBSA_dock.dat'),
             '-cp', os.path.join(wdir, 'complex_dock.prmtop'),
             '-rp', os.path.join(wdir, 'rec.prmtop'),
             '-lp', os.path.join(wdir, 'lig_dock.prmtop'),
             '-y',  os.path.join(wdir, 'min_dock.rst7')],
            cwd=wdir, timeout=600)
        log.write("  MMPBSA.py done\n"); log.flush()
    except Exception as e:
        log.write(f"  MMPBSA FAILED: {e}\n"); log.flush()
        results[name] = {'error': f'mmpbsa: {str(e)[:400]}'}
        continue

    # 6. Parse
    dat = os.path.join(wdir, 'FINAL_RESULTS_MMGBSA_dock.dat')
    try:
        txt = open(dat).read()
        log.write(f"  tail:\n{txt[-600:]}\n"); log.flush()
        m = re.search(r'DELTA TOTAL\s+([-\d.]+)', txt, re.IGNORECASE)
        if not m:
            for line in txt.split('\n'):
                if 'TOTAL' in line.upper() and 'DELTA' in line.upper():
                    nums = re.findall(r'-?\d+\.\d+', line)
                    if nums:
                        results[name] = {'dg_mmgbsa': float(nums[0])}
                        log.write(f"  ΔG = {nums[0]} kcal/mol\n"); log.flush()
                        m = 'done'
                        break
        if m and m != 'done':
            dg = float(m.group(1))
            results[name] = {'dg_mmgbsa': dg}
            log.write(f"  ΔG = {dg:.2f} kcal/mol\n"); log.flush()
        elif not m:
            results[name] = {'error': 'parse failed'}
    except Exception as e:
        results[name] = {'error': f'parse: {e}'}
        log.write(f"  PARSE ERROR: {e}\n"); log.flush()

with open(os.path.join(mmgbsa_dir, 'mmgbsa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
log.write("\nALL DONE\n"); log.flush()
log.close()
print("ALL DONE")
