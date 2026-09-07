
# ── Test openmmforcefields GAFF2 + RDKit ─────────────────────────────────────
from openmmforcefields.generators import GAFFTemplateGenerator
from openmm.app import ForceField, PDBFile, Modeller, OBC2
from openmm import unit, LangevinMiddleIntegrator
import openmm as mm
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

test_smi = 'CCc1cc(C(=O)N2CCOC[C@@H]2c2cccc(C(=O)NCc3sc(C)nc3C)n2)n(C)n1'
test_mol = Chem.MolFromSmiles(test_smi)
test_mol = Chem.AddHs(test_mol)
AllChem.EmbedMolecule(test_mol, AllChem.ETKDGv3())

try:
    gen = GAFFTemplateGenerator.from_molecules([test_mol], forcefield='gaff-2.11')
    print("GAFFTemplateGenerator from_molecules(RDKit): OK")
    ff = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
    ff.registerTemplateGenerator(gen.generator)
    print("Force field + GAFF2 + OBC2: registered OK")
except Exception as e:
    print(f"GAFFTemplateGenerator (RDKit direct) failed: {e}")
    # Try with openff Molecule
    try:
        from openff.toolkit import Molecule as OFFMol
        off_mol = OFFMol.from_smiles(test_smi)
        gen = GAFFTemplateGenerator.from_molecules([off_mol], forcefield='gaff-2.11')
        print("GAFFTemplateGenerator (openff.toolkit): OK")
    except Exception as e2:
        print(f"openff.toolkit also failed: {e2}")
