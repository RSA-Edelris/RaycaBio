# Corrected Brønsted-acid check using SMARTS (not substring matching).
# Original substring 'C(=O)O' fails for TFA: RDKit canonicalises TFA as O=C(O)C(F)(F)F
# which does NOT contain the literal substring 'C(=O)O'. SMARTS is the correct method.
from rdkit import Chem
smarts_cooh = Chem.MolFromSmarts('[CX3](=O)[OX2H1]')
smarts_so3h = Chem.MolFromSmarts('[SX4](=O)(=O)[OX2H1]')
acid_hits = [(i, m) for i, m in enumerate(mols2)
             if m.HasSubstructMatch(smarts_cooh) or m.HasSubstructMatch(smarts_so3h)]
# Result on HTE_Edelris_2.sdf: 0 hits — no Brønsted acid present in the 74-entry kit.
