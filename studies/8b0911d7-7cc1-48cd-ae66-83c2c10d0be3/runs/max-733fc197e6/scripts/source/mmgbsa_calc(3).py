#!/usr/bin/env python3
"""
Single-point MM-GBSA free energy of binding for best Vina poses.
Method: E(complex) - E(receptor) - E(ligand) in OBC2 implicit solvent.
No MD sampling; single-trajectory approximation on the docked pose.

Ligands: Cpd32 R (EDS00760714-1) and Cpd16 R (EDS00760778-1)
"""
import os, sys, json, math
import numpy as np
from pathlib import Path

# ── RDKit
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

# ── OpenMM
import openmm as mm
import openmm.app as app
import openmm.unit as unit
from openmmforcefields.generators import GAFFTemplateGenerator

WORKDIR = Path('/home/ubuntu/rayca-sessions/8b0911d7-7cc1-48cd-ae66-83c2c10d0be3-c43f8bb507fc')
LIG_DIR = WORKDIR / 'ligands'
RECEPTOR_PDB = WORKDIR / '9C56_receptor.pdb'

RT = 0.5921  # kcal/mol at 298 K

TARGETS = [
    {
        'id': 'EDS00760714-1',
        'name': 'Compound 32 (R)',
        'smiles': 'Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NCCF)n2)nc2ccccc21',
        'vina_dg': -7.012,
    },
    {
        'id': 'EDS00760778-1',
        'name': 'Compound 16 (R)',
        'smiles': 'Cn1c(CN2CC3(CC3)C[C@@H]2c2cccc(C(=O)NC3CCC3)n2)nc2ccccc21',
        'vina_dg': -7.802,
    },
]


def parse_best_pose_pdbqt(pdbqt_path):
    """Parse first MODEL from PDBQT, return (atom_names, element_symbols, coords_nm)."""
    atom_names, elements, coords = [], [], []
    in_model = False
    with open(pdbqt_path) as f:
        for line in f:
            if line.startswith('MODEL'):
                in_model = True
            elif line.startswith('ENDMDL'):
                break
            elif in_model and (line.startswith('ATOM') or line.startswith('HETATM')):
                aname = line[12:16].strip()
                # PDBQT atom type in cols 77-78; fallback to first char of name
                atype = line[77:79].strip() if len(line) > 77 else ''
                el = atype[0] if atype and atype[0].isalpha() else aname[0]
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                # Skip hydrogens added by vina (type H or HD)
                if el.upper() != 'H':
                    atom_names.append(aname)
                    elements.append(el.capitalize())
                    coords.append([x, y, z])   # Angstrom
    return atom_names, elements, np.array(coords)


def build_ligand_mol_with_pose(smiles, pose_coords_ang):
    """
    Build RDKit mol from SMILES, embed with ETKDGv3,
    then align to pose_coords_ang (heavy atoms only).
    Returns mol with pose coordinates.
    """
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(mol)

    # Heavy-atom count check
    heavy = [a for a in mol.GetAtoms() if a.GetAtomicNum() != 1]
    if len(heavy) != len(pose_coords_ang):
        print(f"  Warning: SMILES heavy atoms ({len(heavy)}) != PDBQT heavy atoms ({len(pose_coords_ang)})")

    # Set heavy-atom coordinates from pose; rebuild H positions
    conf = mol.GetConformer()
    heavy_idx = [a.GetIdx() for a in mol.GetAtoms() if a.GetAtomicNum() != 1]
    for i, idx in enumerate(heavy_idx[:len(pose_coords_ang)]):
        conf.SetAtomPosition(idx, pose_coords_ang[i].tolist())

    # Re-optimize H positions only (freeze heavy atoms)
    # Use MMFF constrained minimization
    ff = AllChem.MMFFGetMoleculeForceField(
        mol, AllChem.MMFFGetMoleculeProperties(mol), confId=0
    )
    if ff:
        for idx in heavy_idx:
            ff.MMFFAddPositionConstraint(idx, 0.0, 1e4)
        ff.Minimize(maxIts=200)

    return mol


def single_point_energy_kcal(system, topology, positions):
    """Compute single-point potential energy in kcal/mol."""
    integrator = mm.VerletIntegrator(0.001 * unit.picosecond)
    platform = mm.Platform.getPlatformByName('CPU')
    ctx = mm.Context(system, integrator, platform)
    ctx.setPositions(positions)
    state = ctx.getState(getEnergy=True)
    e = state.getPotentialEnergy().value_in_unit(unit.kilocalorie_per_mole)
    del ctx, integrator
    return e


def build_system_implicit(topology, molecules=None):
    """Build ff14SB + GAFF2 system in OBC2 implicit solvent (via XML)."""
    from openmm.app import ForceField
    if molecules:
        gaff = GAFFTemplateGenerator(molecules=molecules, forcefield='gaff2')
        ff = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
        ff.registerTemplateGenerator(gaff.generator)
    else:
        ff = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
    system = ff.createSystem(
        topology,
        nonbondedMethod=app.NoCutoff,
        constraints=app.HBonds,
    )
    return system


# ── Load receptor ──
print("Loading receptor...")
rec_pdb = app.PDBFile(str(RECEPTOR_PDB))
rec_top = rec_pdb.topology
rec_pos = rec_pdb.positions

print(f"  Receptor atoms: {rec_top.getNumAtoms()}")

# Build receptor-only system (cached for reuse)
print("  Building receptor system (ff14SB + OBC2)...")
rec_system = build_system_implicit(rec_top)
E_receptor = single_point_energy_kcal(rec_system, rec_top, rec_pos)
print(f"  E_receptor = {E_receptor:.2f} kcal/mol")

results = []

for t in TARGETS:
    print(f"\n{'='*60}")
    print(f"Processing {t['name']} ({t['id']})")
    pdbqt = LIG_DIR / f"{t['id']}_poses.pdbqt"

    # Parse best pose heavy atom coords from PDBQT
    anames, elements, pose_coords = parse_best_pose_pdbqt(pdbqt)
    print(f"  Pose heavy atoms parsed: {len(pose_coords)}")

    # Build RDKit mol with pose coords
    mol = build_ligand_mol_with_pose(t['smiles'], pose_coords)
    print(f"  RDKit mol: {mol.GetNumAtoms()} atoms (with H)")

    # Build ligand-only topology + system for E_ligand
    from openmmforcefields.generators import GAFFTemplateGenerator
    from openmm.app import Modeller

    # Use openff Molecule or RDKit mol for GAFF
    gaff_gen = GAFFTemplateGenerator(molecules=[mol], forcefield='gaff2')
    lig_ff = app.ForceField('implicit/obc2.xml')
    lig_ff.registerTemplateGenerator(gaff_gen.generator)

    # Create ligand topology from mol
    lig_top = app.Topology()
    lig_chain = lig_top.addChain()
    lig_res = lig_top.addResidue('LIG', lig_chain)
    atom_map = {}
    for atom in mol.GetAtoms():
        el_sym = atom.GetSymbol()
        omm_el = app.Element.getBySymbol(el_sym)
        omm_atom = lig_top.addAtom(f'{el_sym}{atom.GetIdx()}', omm_el, lig_res)
        atom_map[atom.GetIdx()] = omm_atom
    for bond in mol.GetBonds():
        lig_top.addBond(atom_map[bond.GetBeginAtomIdx()], atom_map[bond.GetEndAtomIdx()])

    conf = mol.GetConformer()
    lig_pos = [
        mm.Vec3(conf.GetAtomPosition(i).x * 0.1,
                conf.GetAtomPosition(i).y * 0.1,
                conf.GetAtomPosition(i).z * 0.1) * unit.nanometer
        for i in range(mol.GetNumAtoms())
    ]

    print("  Building ligand system (GAFF2 + OBC2)...")
    lig_system = lig_ff.createSystem(
        lig_top,
        nonbondedMethod=app.NoCutoff,
        constraints=app.HBonds,
    )
    E_ligand = single_point_energy_kcal(lig_system, lig_top, lig_pos)
    print(f"  E_ligand = {E_ligand:.2f} kcal/mol")

    # Build complex topology = receptor + ligand
    print("  Building complex system (ff14SB + GAFF2 + OBC2)...")
    modeller = Modeller(rec_top, rec_pos)
    modeller.add(lig_top, lig_pos)
    cplx_top = modeller.topology
    cplx_pos = modeller.positions

    cplx_ff = app.ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
    gaff_cplx = GAFFTemplateGenerator(molecules=[mol], forcefield='gaff2')
    cplx_ff.registerTemplateGenerator(gaff_cplx.generator)

    cplx_system = cplx_ff.createSystem(
        cplx_top,
        nonbondedMethod=app.NoCutoff,
        constraints=app.HBonds,
        implicitSolvent=app.OBC2,
    )
    E_complex = single_point_energy_kcal(cplx_system, cplx_top, cplx_pos)
    print(f"  E_complex = {E_complex:.2f} kcal/mol")

    dG_mmgbsa = E_complex - E_receptor - E_ligand
    dG_vina   = t['vina_dg']
    kd_vina   = math.exp(dG_vina / RT) * 1e6   # µM
    kd_mmgbsa = math.exp(dG_mmgbsa / RT) * 1e6 # µM (indicative only)

    print(f"\n  ΔG_Vina     = {dG_vina:.2f} kcal/mol  →  Kd_pred = {kd_vina:.1f} µM")
    print(f"  ΔG_MM-GBSA  = {dG_mmgbsa:.2f} kcal/mol  →  Kd_pred = {kd_mmgbsa:.2f} µM (indicative)")

    results.append({
        'id': t['id'],
        'name': t['name'],
        'E_receptor_kcal': round(E_receptor, 2),
        'E_ligand_kcal': round(E_ligand, 2),
        'E_complex_kcal': round(E_complex, 2),
        'dG_vina_kcal': dG_vina,
        'dG_mmgbsa_kcal': round(dG_mmgbsa, 2),
        'kd_vina_uM': round(kd_vina, 1),
        'kd_mmgbsa_uM': round(kd_mmgbsa, 2),
    })

# ── Save results ──
out = WORKDIR / 'mmgbsa_results.json'
with open(out, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved: {out}")

# ── Print summary table ──
print("\n" + "="*80)
print("SUMMARY TABLE")
print("="*80)
print(f"{'Compound':<20} {'Vina ΔG':>10} {'Vina Kd':>10} {'MM-GBSA ΔG':>12} {'MM-GBSA Kd':>12}")
print(f"{'':20} {'(kcal/mol)':>10} {'(µM)':>10} {'(kcal/mol)':>12} {'(µM, ind.)':>12}")
print("-"*80)
for r in results:
    print(f"{r['name']:<20} {r['dG_vina_kcal']:>10.2f} {r['kd_vina_uM']:>10.1f} "
          f"{r['dG_mmgbsa_kcal']:>12.2f} {r['kd_mmgbsa_uM']:>12.2f}")
print("="*80)
print("Note: MM-GBSA is single-point (no MD sampling). ΔG_MM-GBSA = E(complex) - E(receptor) - E(ligand) in OBC2 GB.")
