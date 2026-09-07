
from rdkit import Chem
from rdkit.Chem import AllChem
from openmmforcefields.generators import GAFFTemplateGenerator, EspalomaTemplateGenerator
from openmm.app import ForceField, PDBFile, Modeller
import openmm as mm
from openmm import unit
import numpy as np, gzip, io

# ── Test GAFFTemplateGenerator with RDKit mol ─────────────────────────────────
smi0 = 'CCc1cc(C(=O)N2CCO[C@H](c3cccc(C(=O)NCc4sc(C)nc4C)n3)C2)n(C)n1'
rdmol = Chem.MolFromSmiles(smi0)
rdmol = Chem.AddHs(rdmol)
AllChem.EmbedMolecule(rdmol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(rdmol)

generator_ok = None
for GenClass, label in [(GAFFTemplateGenerator, 'GAFF-2.11'),
                         (EspalomaTemplateGenerator, 'Espaloma')]:
    try:
        kw = {'forcefield': 'gaff-2.11'} if GenClass == GAFFTemplateGenerator else {}
        gen = GenClass(molecules=[rdmol], **kw)
        ff_test = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
        ff_test.registerTemplateGenerator(gen.generator)
        print(f"{label}: REGISTERED OK")
        generator_ok = (GenClass, kw, label)
        break
    except Exception as e:
        print(f"{label}: FAILED — {e}")

if generator_ok is None:
    print("\nFalling back to MM interaction energy (no solvation) via RDKit MMFF94")
