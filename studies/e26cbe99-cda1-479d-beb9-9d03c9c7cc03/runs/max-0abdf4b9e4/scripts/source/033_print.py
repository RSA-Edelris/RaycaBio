
import os, subprocess, numpy as np
from pdbfixer import PDBFixer
from openmm.app import PDBFile, ForceField, Modeller, NoCutoff
import openmm as mm
from openmm import unit
from rdkit import Chem
from rdkit.Chem import AllChem
from openmmforcefields.generators import GAFFTemplateGenerator

RT_KCAL = 0.5921
LN10    = 2.30259

# ---- Re-cap the truncated receptor via PDBFixer ---------------------------
print("Re-capping truncated receptor with PDBFixer ...")
fixer = PDBFixer(filename='PB-20260903-4CI2_receptor_trimmed_noH_fixed.pdb')
fixer.findMissingResidues()
# We do NOT want to fill gaps — clear any gap entries (only keep true termini)
# Actually, for a truncated chain keep fixer.missingResidues empty
fixer.missingResidues = {}
fixer.findMissingAtoms()   # detects OXT on C-terminus
fixer.addMissingAtoms()    # adds OXT to C-term
fixer.addMissingHydrogens(7.4)  # adds H1,H2,H3 to N-term; normal H elsewhere

capped_path = 'PB-20260903-4CI2_receptor_trimmed_capped.pdb'
with open(capped_path, 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

rec_capped = PDBFile(capped_path)
print(f"Capped receptor: {rec_capped.topology.getNumResidues()} res, "
      f"{rec_capped.topology.getNumAtoms()} atoms")

# ---- Receptor energy baseline with ff14SB + OBC2 -------------------------
class MinimalOFFMolecule:
    def __init__(self, rdmol):
        self._rdmol = rdmol; self.name = 'LIG'
    def to_smiles(self, mapped=False, **kw):
        return Chem.MolToSmiles(Chem.RemoveHs(self._rdmol))
    def to_rdkit(self): return self._rdmol
    def to_file(self, path, file_format):
        fmt = file_format.lower().lstrip('.')
        if fmt in ('sdf','mol'):
            w=Chem.SDWriter(path); w.write(self._rdmol); w.close()
        else:
            sdf_tmp=path+'.tmp.sdf'; w=Chem.SDWriter(sdf_tmp); w.write(self._rdmol); w.close()
            subprocess.run(['obabel','-isdf',sdf_tmp,f'-o{fmt}','-O',path],
                           capture_output=True,check=True); os.unlink(sdf_tmp)
    @property
    def n_atoms(self): return self._rdmol.GetNumAtoms()

def mol_to_pdb_block(mol, res_name='LIG', chain_id='Z', res_seq=1):
    conf=mol.GetConformer(); lines=[]; serial={}
    for i,atom in enumerate(mol.GetAtoms()):
        pos=conf.GetAtomPosition(atom.GetIdx()); elem=atom.GetSymbol()
        anm=(f" {elem}{i+1:<3s}" if len(elem)==1 else f"{elem}{i+1:<3s}")[:4]
        lines.append(f"HETATM{i+1:5d} {anm:<4s} {res_name:3s} {chain_id}{res_seq:4d}    "
                     f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}  1.00  0.00          {elem:>2s}\n")
        serial[atom.GetIdx()]=i+1
    seen=set()
    for bond in mol.GetBonds():
        a,b=bond.GetBeginAtomIdx(),bond.GetEndAtomIdx(); sa,sb=serial[a],serial[b]
        if (sa,sb) not in seen:
            lines+=[f"CONECT{sa:5d}{sb:5d}\n",f"CONECT{sb:5d}{sa:5d}\n"]; seen.add((sa,sb))
    lines.append("END\n"); return "".join(lines)

def calc_energy_kcal(ff, topology, positions):
    system=ff.createSystem(topology, nonbondedMethod=NoCutoff,
                           implicitSolvent=mm.app.OBC2,
                           soluteDielectric=1.0, solventDielectric=78.5)
    intg=mm.VerletIntegrator(0.001*unit.picoseconds)
    ctx=mm.Context(system,intg,mm.Platform.getPlatformByName('Reference'))
    ctx.setPositions(positions)
    e=ctx.getState(getEnergy=True).getPotentialEnergy()
    del ctx,intg
    return e.value_in_unit(unit.kilojoules_per_mole)/4.184

ff_base = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
try:
    E_rec = calc_energy_kcal(ff_base, rec_capped.topology, rec_capped.positions)
    print(f"Receptor single-point energy: {E_rec:,.1f} kcal/mol  ✓")
    rec_ok = True
    rec_topology  = rec_capped.topology
    rec_positions = rec_capped.positions
except Exception as ex:
    print(f"Receptor energy FAILED: {ex}")
    rec_ok = False
