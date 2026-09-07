
import subprocess, os

# Check antechamber
r = subprocess.run(['which', 'antechamber'], capture_output=True, text=True)
antechamber_path = r.stdout.strip()
print(f"antechamber: {antechamber_path or 'NOT FOUND'}")

r2 = subprocess.run(['which', 'obabel'], capture_output=True, text=True)
print(f"obabel: {r2.stdout.strip() or 'NOT FOUND'}")

# Try to get openff.toolkit via a wrapper approach - create a minimal Molecule wrapper
# that satisfies the to_smiles() call needed by openmmforcefields
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np

class MinimalOFFMolecule:
    """Minimal wrapper so GAFFTemplateGenerator accepts an RDKit mol."""
    def __init__(self, rdmol):
        self._rdmol = rdmol
        self.name  = 'LIG'
    def to_smiles(self, mapped=False, **kw):
        smi = Chem.MolToSmiles(Chem.RemoveHs(self._rdmol))
        return smi
    def to_rdkit(self):
        return self._rdmol
    @property
    def n_atoms(self):
        return self._rdmol.GetNumAtoms()
    def to_file(self, path, file_format):
        ext = file_format.lower().lstrip('.')
        if ext in ('mol', 'sdf', 'mol2'):
            writer = Chem.SDWriter(path) if ext in ('sdf','mol') else None
            if writer:
                writer.write(self._rdmol); writer.close()

smi0 = 'CCc1cc(C(=O)N2CCO[C@H](c3cccc(C(=O)NCc4sc(C)nc4C)n3)C2)n(C)n1'
rdmol = Chem.AddHs(Chem.MolFromSmiles(smi0))
AllChem.EmbedMolecule(rdmol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(rdmol)

wrapper = MinimalOFFMolecule(rdmol)
try:
    from openmmforcefields.generators import GAFFTemplateGenerator
    from openmm.app import ForceField
    gen = GAFFTemplateGenerator(molecules=[wrapper], forcefield='gaff-2.11')
    ff_test = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
    ff_test.registerTemplateGenerator(gen.generator)
    print("\nGAFF-2.11 via wrapper: REGISTERED OK")
    gaff_method = 'gaff-2.11'
except Exception as e:
    print(f"\nGAFF wrapper failed: {e}")
    gaff_method = None
