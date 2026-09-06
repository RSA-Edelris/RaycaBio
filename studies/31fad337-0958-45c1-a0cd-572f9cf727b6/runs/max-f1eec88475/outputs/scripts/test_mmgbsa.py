#!/usr/bin/env python3
"""Feasibility test: OpenMM ff14SB + GAFF2 + OBC2 single-point MM-GBSA."""
import sys, traceback
from pathlib import Path
from io import StringIO

WDIR = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC  = str(WDIR / "receptor_prepared.pdb")
SDF  = str(WDIR / "poses_top20/CTX-1020732_poses.sdf")

from rdkit import Chem
from rdkit.Chem import AllChem
import openmm.app as app
import openmm
import openmm.unit as unit
from openmmforcefields.generators import GAFFTemplateGenerator
from openmm.app import Modeller

# ── 1. Load ligand best pose ──────────────────────────────────────────────────
suppl = Chem.SDMolSupplier(SDF, removeHs=False)
mol = next((m for m in suppl if m is not None), None)
assert mol is not None, "Could not read ligand SDF"
print(f"Ligand: {mol.GetNumAtoms()} atoms (incl H)")

# ── 2. Register GAFF2 template generator ─────────────────────────────────────
gaff = GAFFTemplateGenerator(molecules=[mol], forcefield='gaff2')
ff   = app.ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
ff.registerTemplateGenerator(gaff.generator)
print("GAFFTemplateGenerator: registered")

# ── 3. Load receptor ──────────────────────────────────────────────────────────
pdb = app.PDBFile(REC)
print(f"Receptor: {pdb.topology.getNumAtoms()} atoms")

# ── 4. Convert ligand to PDB topology ────────────────────────────────────────
lig_pdb_block = Chem.MolToPDBBlock(mol)
lig_pdb = app.PDBFile(StringIO(lig_pdb_block))

# ── 5. Build complex modeller ─────────────────────────────────────────────────
modeller = Modeller(pdb.topology, pdb.positions)
modeller.add(lig_pdb.topology, lig_pdb.positions)
print(f"Complex: {modeller.topology.getNumAtoms()} atoms")

# ── 6. Create complex system ──────────────────────────────────────────────────
system_c = ff.createSystem(modeller.topology,
                            nonbondedMethod=app.NoCutoff,
                            constraints=None,
                            implicitSolvent=app.OBC2)
print(f"Complex forces: {[type(f).__name__ for f in system_c.getForces()]}")

def minimize_and_energy(topology, positions, system, label):
    integrator = openmm.LangevinIntegrator(300*unit.kelvin, 1/unit.picosecond, 0.002*unit.picoseconds)
    platform   = openmm.Platform.getPlatformByName('CPU')
    sim = app.Simulation(topology, system, integrator, platform)
    sim.context.setPositions(positions)
    sim.minimizeEnergy(maxIterations=500)
    state = sim.context.getState(getEnergy=True)
    e = state.getPotentialEnergy().value_in_unit(unit.kilocalories_per_mole)
    print(f"  {label}: {e:.3f} kcal/mol")
    return e, sim.context.getState(getPositions=True).getPositions()

print("\nMinimising complex ...")
E_complex, pos_complex = minimize_and_energy(modeller.topology, modeller.positions, system_c, "E_complex")

# ── Receptor alone ────────────────────────────────────────────────────────────
system_r = ff.createSystem(pdb.topology,
                            nonbondedMethod=app.NoCutoff,
                            constraints=None,
                            implicitSolvent=app.OBC2)
# Use receptor positions from minimised complex
import numpy as np
n_rec = pdb.topology.getNumAtoms()
rec_pos = pos_complex[:n_rec]
print("Minimising receptor ...")
E_receptor, _ = minimize_and_energy(pdb.topology, rec_pos, system_r, "E_receptor")

# ── Ligand alone ──────────────────────────────────────────────────────────────
system_l = ff.createSystem(lig_pdb.topology,
                            nonbondedMethod=app.NoCutoff,
                            constraints=None,
                            implicitSolvent=app.OBC2)
lig_pos = pos_complex[n_rec:]
print("Minimising ligand ...")
E_ligand, _ = minimize_and_energy(lig_pdb.topology, lig_pos, system_l, "E_ligand")

# ── MM-GBSA ───────────────────────────────────────────────────────────────────
dG = E_complex - E_receptor - E_ligand
print(f"\nMM-GBSA dG_bind (single-point) = {dG:.3f} kcal/mol")
print("FEASIBILITY TEST: PASSED")
