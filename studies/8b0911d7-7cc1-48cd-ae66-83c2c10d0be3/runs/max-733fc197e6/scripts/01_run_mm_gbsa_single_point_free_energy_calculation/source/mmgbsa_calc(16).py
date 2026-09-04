#!/usr/bin/env python3
"""
Single-point MM-GBSA free energy of binding for best Vina poses.
Method: E(complex) - E(receptor) - E(ligand) in OBC2 implicit solvent.

Pipeline:
  receptor : ff14SB via tleap → prmtop
  ligand   : antechamber (GAFF2, AM1-BCC) + parmchk2 + tleap → prmtop
  complex  : tleap combine → prmtop
  energy   : OpenMM AmberPrmtopFile.createSystem(implicitSolvent=OBC2)

Ligands: Cpd32 R (EDS00760714-1) and Cpd16 R (EDS00760778-1)
"""
import os, sys, json, math, tempfile, subprocess, shutil
import numpy as np
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem

import openmm as mm
import openmm.app as app
import openmm.unit as unit

WORKDIR      = Path('/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc')
LIG_DIR      = WORKDIR / 'ligands'
RECEPTOR_PDB = WORKDIR / '9C56_receptor_amber.pdb'   # HIS renamed to HID/HIE for tleap
AMBER_HOME   = '/home/ubuntu/rayca-runtime/.mamba/envs/rayca'

RT = 0.5921   # kcal/mol at 298 K

TARGETS = [
    {
        'id': 'EDS00760714-1',
        'name': 'Compound 32 (R)',
        'smiles': 'Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NCCF)n2)nc2ccccc21',
        'net_charge': 0,
        'vina_dg': -7.012,
    },
    {
        'id': 'EDS00760778-1',
        'name': 'Compound 16 (R)',
        'smiles': 'Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NC3CCC3)n2)nc2ccccc21',
        'net_charge': 0,
        'vina_dg': -7.802,
    },
]


def run_cmd(cmd, cwd=None, env=None, label=''):
    e = os.environ.copy()
    e['AMBERHOME'] = AMBER_HOME
    if env:
        e.update(env)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=e)
    if r.returncode != 0:
        # Print sqm.out if present (antechamber failure diagnosis)
        sqm_out = os.path.join(cwd or '.', 'sqm.out') if cwd else 'sqm.out'
        sqm_txt = ''
        if os.path.exists(sqm_out):
            with open(sqm_out) as _f:
                sqm_lines = _f.readlines()
            sqm_txt = '\nsqm.out tail:\n' + ''.join(sqm_lines[-20:])
        raise RuntimeError(
            f"{label or cmd[0]} failed (rc={r.returncode}):\n"
            f"stdout: {r.stdout[-400:]}\nstderr: {r.stderr[:400]}{sqm_txt}"
        )
    return r


def parse_best_pose_pdbqt(pdbqt_path):
    """Return heavy-atom (name, element, x, y, z) list from first MODEL."""
    atoms = []
    in_model = False
    with open(pdbqt_path) as f:
        for line in f:
            if line.startswith('MODEL'):
                in_model = True
            elif line.startswith('ENDMDL'):
                break
            elif in_model and (line.startswith('ATOM') or line.startswith('HETATM')):
                aname = line[12:16].strip()
                atype = line[77:79].strip() if len(line) > 77 else ''
                el    = atype[0] if atype and atype[0].isalpha() else aname[0]
                if el.upper() == 'H':
                    continue
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
                atoms.append((aname, el.capitalize(), x, y, z))
    return atoms


def build_mol_with_pose(smiles, heavy_atoms):
    """Build RDKit mol with heavy-atom coords from docked pose; MMFF-optimise H."""
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(mol)

    conf      = mol.GetConformer()
    heavy_idx = [a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum() != 1]

    if len(heavy_idx) != len(heavy_atoms):
        print(f"  Warning: SMILES heavy atoms ({len(heavy_idx)}) != "
              f"PDBQT heavy atoms ({len(heavy_atoms)})")

    for i, idx in enumerate(heavy_idx[:len(heavy_atoms)]):
        _, _, x, y, z = heavy_atoms[i]
        conf.SetAtomPosition(idx, [x, y, z])

    ff = AllChem.MMFFGetMoleculeForceField(
        mol, AllChem.MMFFGetMoleculeProperties(mol), confId=0)
    if ff:
        for idx in heavy_idx:
            ff.MMFFAddPositionConstraint(idx, 0.0, 1e4)
        ff.Minimize(maxIts=300)

    return mol


def mol_to_sdf(mol, path):
    w = Chem.SDWriter(str(path))
    w.write(mol)
    w.close()


def make_clean_mol(smiles):
    """Build a fully MMFF-optimised mol (no docked coords) for antechamber."""
    m = Chem.MolFromSmiles(smiles)
    m = Chem.AddHs(m)
    AllChem.EmbedMolecule(m, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(m, maxIters=2000)
    return m


def patch_mol2_coords(mol2_path, docked_mol):
    """
    Replace atom coordinates in a mol2 file with those from docked_mol.
    Assumes atom ordering in mol2 matches heavy+H ordering of docked_mol.
    Works on the @<TRIPOS>ATOM section.
    """
    with open(mol2_path) as fh:
        content = fh.read()

    conf  = docked_mol.GetConformer()
    atoms = list(docked_mol.GetAtoms())

    lines_out = []
    in_atom   = False
    atom_idx  = 0
    for line in content.splitlines(keepends=True):
        if '@<TRIPOS>ATOM' in line:
            in_atom  = True
            atom_idx = 0
            lines_out.append(line)
            continue
        if in_atom and line.startswith('@'):
            in_atom = False
        if in_atom and line.strip():
            if atom_idx < len(atoms):
                p = conf.GetAtomPosition(atom_idx)
                parts = line.split()
                # mol2 format: id name x y z type subst_id subst_name charge
                parts[2] = f'{p.x:10.4f}'
                parts[3] = f'{p.y:10.4f}'
                parts[4] = f'{p.z:10.4f}'
                # Rebuild with fixed-width spacing
                line = (f'{parts[0]:>7s} {parts[1]:<8s}'
                        f'{p.x:10.4f}{p.y:10.4f}{p.z:10.4f} '
                        + ' '.join(parts[5:]) + '\n')
                atom_idx += 1
        lines_out.append(line)

    with open(mol2_path, 'w') as fh:
        fh.writelines(lines_out)


def parameterise_ligand(mol, smiles, lig_id, net_charge, tmpdir):
    """
    antechamber (GAFF2, AM1-BCC) on clean MMFF geometry → parmchk2 → patch
    mol2 coords with docked pose → tleap.
    Returns (mol2_path, frcmod_path, prmtop_path, inpcrd_path).
    """
    # Each ligand gets its own subdirectory so antechamber temp files don't clash
    lig_dir = os.path.join(tmpdir, lig_id)
    os.makedirs(lig_dir, exist_ok=True)

    sdf      = os.path.join(lig_dir, f'{lig_id}.sdf')
    mol2     = os.path.join(lig_dir, f'{lig_id}.mol2')
    frcmod   = os.path.join(lig_dir, f'{lig_id}.frcmod')
    prmtop   = os.path.join(lig_dir, f'{lig_id}.prmtop')
    inpcrd   = os.path.join(lig_dir, f'{lig_id}.inpcrd')

    # Use CLEAN MMFF geometry for AM1-BCC charge calc (avoids sqm non-convergence)
    clean_mol = make_clean_mol(smiles)
    mol_to_sdf(clean_mol, sdf)

    # antechamber (run in lig_dir so sqm.in/sqm.out stay isolated)
    run_cmd([
        'antechamber',
        '-i', sdf, '-fi', 'sdf',
        '-o', mol2, '-fo', 'mol2',
        '-c', 'bcc', '-nc', str(net_charge),
        '-at', 'gaff2', '-s', '2', '-pf', 'y',
    ], cwd=lig_dir, label='antechamber')
    print(f"    antechamber OK → {mol2}")

    # parmchk2
    run_cmd(['parmchk2', '-i', mol2, '-f', 'mol2', '-o', frcmod, '-s', 'gaff2'],
            cwd=lig_dir, label='parmchk2')
    print(f"    parmchk2 OK → {frcmod}")

    # tleap for ligand only
    leapin = os.path.join(lig_dir, 'leap_lig.in')
    with open(leapin, 'w') as f:
        f.write(f"source leaprc.gaff2\n"
                f"loadamberparams {frcmod}\n"
                f"LIG = loadmol2 {mol2}\n"
                f"saveamberparm LIG {prmtop} {inpcrd}\n"
                f"quit\n")
    run_cmd(['tleap', '-f', leapin], cwd=lig_dir, label='tleap-ligand')
    print(f"    tleap-ligand OK → {prmtop}")

    return mol2, frcmod, prmtop, inpcrd


def build_receptor_prmtop(rec_pdb, tmpdir):
    """tleap ff14SB → receptor.prmtop + receptor.inpcrd."""
    prmtop = os.path.join(tmpdir, 'receptor.prmtop')
    inpcrd = os.path.join(tmpdir, 'receptor.inpcrd')
    leapin = os.path.join(tmpdir, 'leap_rec.in')
    with open(leapin, 'w') as f:
        f.write(f"source leaprc.protein.ff14SB\n"
                f"REC = loadpdb {rec_pdb}\n"
                f"saveamberparm REC {prmtop} {inpcrd}\n"
                f"quit\n")
    r = subprocess.run(
        ['tleap', '-f', leapin], capture_output=True, text=True,
        cwd=tmpdir,
        env={**os.environ, 'AMBERHOME': AMBER_HOME}
    )
    if r.returncode != 0 or not os.path.exists(prmtop):
        print(f"  tleap-receptor stderr:\n{r.stderr[:800]}")
        raise RuntimeError("tleap failed to build receptor prmtop")
    print(f"  tleap-receptor OK → {prmtop}")
    return prmtop, inpcrd


def build_complex_prmtop(rec_pdb, mol2, frcmod, lig_id, tmpdir):
    """tleap: combine receptor + ligand → complex prmtop."""
    prmtop = os.path.join(tmpdir, 'complex.prmtop')
    inpcrd = os.path.join(tmpdir, 'complex.inpcrd')
    leapin = os.path.join(tmpdir, 'leap_cplx.in')
    with open(leapin, 'w') as f:
        f.write(f"source leaprc.protein.ff14SB\n"
                f"source leaprc.gaff2\n"
                f"loadamberparams {frcmod}\n"
                f"LIG = loadmol2 {mol2}\n"
                f"REC = loadpdb {rec_pdb}\n"
                f"MOL = combine {{ REC LIG }}\n"
                f"saveamberparm MOL {prmtop} {inpcrd}\n"
                f"quit\n")
    r = subprocess.run(
        ['tleap', '-f', leapin], capture_output=True, text=True,
        cwd=tmpdir,
        env={**os.environ, 'AMBERHOME': AMBER_HOME}
    )
    if r.returncode != 0 or not os.path.exists(prmtop):
        print(f"  tleap-complex stderr:\n{r.stderr[:800]}")
        raise RuntimeError("tleap failed to build complex prmtop")
    print(f"  tleap-complex OK → {prmtop}")
    return prmtop, inpcrd


def build_obc2_system(prmtop_path):
    prmtop = app.AmberPrmtopFile(str(prmtop_path))
    system = prmtop.createSystem(
        implicitSolvent=app.OBC2,
        nonbondedMethod=app.NoCutoff,
        constraints=None,
    )
    return prmtop, system


def single_point_energy(system, topology, positions):
    """OBC2 single-point energy (kcal/mol)."""
    integrator = mm.VerletIntegrator(0.001 * unit.picosecond)
    ctx = mm.Context(system, integrator, mm.Platform.getPlatformByName('CPU'))
    ctx.setPositions(positions)
    state = ctx.getState(getEnergy=True)
    e = state.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    del ctx, integrator
    return e


def minimise_and_energy(system, positions, max_iter=500):
    """
    Minimise complex, return (E_kcal, minimised_positions_quantity).
    Single-trajectory: minimised positions are then split for receptor/ligand.
    """
    integrator = mm.VerletIntegrator(0.001 * unit.picosecond)
    ctx = mm.Context(system, integrator, mm.Platform.getPlatformByName('CPU'))
    ctx.setPositions(positions)
    mm.LocalEnergyMinimizer.minimize(ctx, tolerance=10.0, maxIterations=max_iter)
    state = ctx.getState(getEnergy=True, getPositions=True)
    e   = state.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    pos = state.getPositions()  # Quantity with units (nm), sliceable
    del ctx, integrator
    return e, pos


def safe_kd_uM(dG_kcal, RT=0.5921):
    """Convert ΔG → Kd(µM), capped to avoid overflow."""
    try:
        return math.exp(dG_kcal / RT) * 1e6
    except OverflowError:
        return float('inf')


# ─────────────────────────────────────────────────────────────────────────────
tmpdir = tempfile.mkdtemp(prefix='mmgbsa_')
print(f"Working directory: {tmpdir}")

# ── Build receptor prmtop (needed for complex topology) ───────────────────────
print("\nBuilding receptor topology (ff14SB via tleap)...")
try:
    rec_prmtop, rec_inpcrd = build_receptor_prmtop(str(RECEPTOR_PDB), tmpdir)
except RuntimeError as e:
    print(f"  FAILED: {e}")
    shutil.rmtree(tmpdir, ignore_errors=True)
    sys.exit(1)

# Atom count for position splitting
import parmed as pmd
n_rec_atoms = len(pmd.load_file(rec_prmtop).atoms)
print(f"  Receptor atoms in prmtop: {n_rec_atoms}")

results = []

for t in TARGETS:
    print(f"\n{'='*60}")
    print(f"Processing {t['name']} ({t['id']})")

    pdbqt = LIG_DIR / f"{t['id']}_poses.pdbqt"
    heavy_atoms = parse_best_pose_pdbqt(pdbqt)
    print(f"  PDBQT heavy atoms: {len(heavy_atoms)}")

    mol = build_mol_with_pose(t['smiles'], heavy_atoms)
    print(f"  RDKit mol total atoms: {mol.GetNumAtoms()}")

    print("  Parameterising ligand (antechamber + parmchk2 + tleap)...")
    mol2, frcmod, lig_prmtop, lig_inpcrd = parameterise_ligand(
        mol, t['id'], t['net_charge'], tmpdir)

    n_lig_atoms = len(pmd.load_file(lig_prmtop).atoms)
    print(f"  Ligand atoms in prmtop: {n_lig_atoms}")

    print("  Building complex topology (tleap)...")
    cplx_prmtop, cplx_inpcrd = build_complex_prmtop(
        str(RECEPTOR_PDB), mol2, frcmod, t['id'], tmpdir)

    # ── Single-trajectory MM-GBSA ─────────────────────────────────────────────
    # 1. Minimise the complex to relieve docking-geometry clashes
    # 2. Split minimised positions: rec = first n_rec_atoms, lig = remainder
    # 3. E_receptor, E_complex, E_ligand all from same minimised geometry
    print("  Minimising complex (500 steps, OBC2)...")
    _, cplx_sys = build_obc2_system(cplx_prmtop)
    cplx_inpcrd_obj = app.AmberInpcrdFile(cplx_inpcrd)
    E_complex, min_pos = minimise_and_energy(cplx_sys, cplx_inpcrd_obj.positions)
    print(f"  E_complex (minimised) = {E_complex:.2f} kcal/mol")

    rec_pos = min_pos[:n_rec_atoms]
    lig_pos = min_pos[n_rec_atoms:n_rec_atoms + n_lig_atoms]

    _, rec_sys = build_obc2_system(rec_prmtop)
    E_receptor = single_point_energy(rec_sys, None, rec_pos)
    print(f"  E_receptor (from complex min) = {E_receptor:.2f} kcal/mol")

    _, lig_sys = build_obc2_system(lig_prmtop)
    E_ligand = single_point_energy(lig_sys, None, lig_pos)
    print(f"  E_ligand   (from complex min) = {E_ligand:.2f} kcal/mol")

    dG_mmgbsa  = E_complex - E_receptor - E_ligand
    dG_vina    = t['vina_dg']
    kd_vina    = safe_kd_uM(dG_vina)
    kd_mmgbsa  = safe_kd_uM(dG_mmgbsa)

    print(f"\n  ΔG_Vina    = {dG_vina:.3f} kcal/mol  →  Kd ≈ {kd_vina:.1f} µM")
    print(f"  ΔG_MM-GBSA = {dG_mmgbsa:.2f} kcal/mol  →  Kd ≈ {kd_mmgbsa:.2f} µM (indicative)")

    results.append({
        'id': t['id'],
        'name': t['name'],
        'E_receptor_kcal': round(E_receptor, 2),
        'E_ligand_kcal':   round(E_ligand, 2),
        'E_complex_kcal':  round(E_complex, 2),
        'dG_vina_kcal':    dG_vina,
        'dG_mmgbsa_kcal':  round(dG_mmgbsa, 2),
        'kd_vina_uM':      round(kd_vina, 1) if math.isfinite(kd_vina) else None,
        'kd_mmgbsa_uM':    round(kd_mmgbsa, 2) if math.isfinite(kd_mmgbsa) else None,
    })

shutil.rmtree(tmpdir, ignore_errors=True)

# ── Save + print ──────────────────────────────────────────────────────────────
out = WORKDIR / 'mmgbsa_results.json'
with open(out, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved → {out}")

print("\n" + "="*80)
print("SUMMARY TABLE")
print("="*80)
print(f"{'Compound':<22} {'Vina ΔG':>10} {'Vina Kd':>10} {'MM-GBSA ΔG':>12} {'MM-GBSA Kd':>12}")
print(f"{'':22} {'(kcal/mol)':>10} {'(µM)':>10} {'(kcal/mol)':>12} {'(µM, ind.)':>12}")
print("-"*80)
for r in results:
    print(f"{r['name']:<22} {r['dG_vina_kcal']:>10.3f} {r['kd_vina_uM']:>10.1f} "
          f"{r['dG_mmgbsa_kcal']:>12.2f} {r['kd_mmgbsa_uM']:>12.2f}")
print("="*80)
print("Note: MM-GBSA single-point (no MD). ΔG = E(complex)−E(receptor)−E(ligand) in OBC2 GB, GAFF2+ff14SB.")
