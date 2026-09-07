
import os, io, subprocess, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import openmm as mm
from openmm.app import PDBFile, ForceField, Modeller, NoCutoff
from openmm import unit
from openmmforcefields.generators import GAFFTemplateGenerator

RT_KCAL = 0.5921
LN10    = 2.30259

# ---- helpers ---------------------------------------------------------------
class MinimalOFFMolecule:
    def __init__(self, rdmol):
        self._rdmol = rdmol; self.name = 'LIG'
    def to_smiles(self, mapped=False, **kw):
        return Chem.MolToSmiles(Chem.RemoveHs(self._rdmol))
    def to_rdkit(self):   return self._rdmol
    def to_file(self, path, file_format):
        fmt = file_format.lower().lstrip('.')
        if fmt in ('sdf','mol'):
            w = Chem.SDWriter(path); w.write(self._rdmol); w.close()
        else:
            sdf_tmp = path+'.tmp.sdf'
            w = Chem.SDWriter(sdf_tmp); w.write(self._rdmol); w.close()
            subprocess.run(['obabel','-isdf',sdf_tmp,f'-o{fmt}','-O',path],
                           capture_output=True, check=True)
            os.unlink(sdf_tmp)
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

# ---- Fix noH trimmed PDB (same orphan-TER issue) then strip H --------------
with open('PB-20260903-4CI2_receptor_trimmed_noH.pdb') as f:
    noH_lines = f.readlines()

chains_with_atoms = set()
for ln in noH_lines:
    if ln[:6].strip() in ('ATOM','HETATM') and len(ln)>=22:
        chains_with_atoms.add(ln[21])

fixed_noH_lines = [ln for ln in noH_lines
                   if not (ln[:3]=='TER' and len(ln)>=22 and ln[21] not in chains_with_atoms)]

fixed_noH_path = 'PB-20260903-4CI2_receptor_trimmed_noH_fixed.pdb'
with open(fixed_noH_path,'w') as f:
    f.writelines(fixed_noH_lines)
print(f"noH fixed PDB: {len(fixed_noH_lines)} lines")

# ---- Build receptor with OpenMM-added H at pH 7.4 -------------------------
ff_base = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
rec_noH = PDBFile(fixed_noH_path)
print(f"noH topology: {rec_noH.topology.getNumResidues()} res, "
      f"{rec_noH.topology.getNumAtoms()} atoms")

mod_rec = Modeller(rec_noH.topology, rec_noH.positions)
try:
    mod_rec.addHydrogens(ff_base, pH=7.4)
    print(f"After addHydrogens: {mod_rec.topology.getNumAtoms()} atoms")
    E_rec = calc_energy_kcal(ff_base, mod_rec.topology, mod_rec.positions)
    print(f"Receptor energy (ff14SB + OBC2): {E_rec:,.1f} kcal/mol")
    rec_ok = True
    rec_topology = mod_rec.topology
    rec_positions = mod_rec.positions
except Exception as ex:
    print(f"Receptor H-add / energy FAILED: {ex}")
    rec_ok = False
