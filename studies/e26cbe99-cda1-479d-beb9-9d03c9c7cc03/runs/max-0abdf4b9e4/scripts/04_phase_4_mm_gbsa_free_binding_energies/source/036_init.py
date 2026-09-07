
import os, subprocess
from rdkit import Chem
from rdkit.Chem import AllChem
import openmm as mm
from openmm.app import PDBFile, ForceField, Modeller, NoCutoff
from openmm import unit
from openmmforcefields.generators import GAFFTemplateGenerator

RT_KCAL = 0.5921;  LN10 = 2.30259

# ============================================================
# Minimal openff-style wrappers so GAFFTemplateGenerator works
# ============================================================
class _Atom:
    def __init__(self, rdatom):
        self.atomic_number    = rdatom.GetAtomicNum()
        self.formal_charge    = rdatom.GetFormalCharge()
        self.is_aromatic      = rdatom.GetIsAromatic()
        self.stereochemistry  = None
        self.metadata         = {}
        self._idx             = rdatom.GetIdx()
    def __repr__(self):
        return f"<Atom {self._idx}>"

class _Bond:
    def __init__(self, rdbond, mol):
        self.atom1_index = rdbond.GetBeginAtomIdx()
        self.atom2_index = rdbond.GetEndAtomIdx()
        self.bond_order  = int(round(rdbond.GetBondTypeAsDouble()))
        self.is_aromatic = rdbond.GetIsAromatic()
        self.atom1       = _Atom(mol.GetAtomWithIdx(self.atom1_index))
        self.atom2       = _Atom(mol.GetAtomWithIdx(self.atom2_index))
    def __repr__(self):
        return f"<Bond {self.atom1_index}-{self.atom2_index}>"

class MinimalOFFMolecule:
    def __init__(self, rdmol):
        self._rdmol = rdmol; self.name = 'LIG'
        self._atoms  = [_Atom(a) for a in rdmol.GetAtoms()]
        self._bonds  = [_Bond(b, rdmol) for b in rdmol.GetBonds()]
    def to_smiles(self, mapped=False, **kw):
        return Chem.MolToSmiles(Chem.RemoveHs(self._rdmol))
    def to_rdkit(self): return self._rdmol
    @property
    def atoms(self):  return iter(self._atoms)
    @property
    def bonds(self):  return iter(self._bonds)
    @property
    def n_atoms(self): return len(self._atoms)
    @property
    def n_bonds(self): return len(self._bonds)
    def to_file(self, path, file_format):
        fmt = file_format.lower().lstrip('.')
        if fmt in ('sdf','mol'):
            w=Chem.SDWriter(path); w.write(self._rdmol); w.close()
        else:
            sdf_tmp=path+'.tmp.sdf'; w=Chem.SDWriter(sdf_tmp); w.write(self._rdmol); w.close()
            subprocess.run(['obabel','-isdf',sdf_tmp,f'-o{fmt}','-O',path],
                           capture_output=True,check=True); os.unlink(sdf_tmp)

def calc_energy_kcal(ff, topology, positions):
    system = ff.createSystem(topology, nonbondedMethod=NoCutoff)
    intg   = mm.VerletIntegrator(0.001*unit.picoseconds)
    ctx    = mm.Context(system, intg, mm.Platform.getPlatformByName('Reference'))
    ctx.setPositions(positions)
    e      = ctx.getState(getEnergy=True).getPotentialEnergy()
    del ctx, intg
    return e.value_in_unit(unit.kilojoules_per_mole)/4.184

def mol_to_pdb_block(mol, res_name='LIG', chain_id='Z', res_seq=1):
    conf=mol.GetConformer(); lines=[]; serial={}
    for i,atom in enumerate(mol.GetAtoms()):
        pos=conf.GetAtomPosition(atom.GetIdx()); elem=atom.GetSymbol()
        num=str(i+1)
        anm=(f" {elem}{num:<3s}" if len(elem)==1 else f"{elem}{num:<3s}")[:4]
        lines.append(f"HETATM{i+1:5d} {anm:<4s} {res_name:3s} {chain_id}{res_seq:4d}    "
                     f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}  1.00  0.00          {elem:>2s}\n")
        serial[atom.GetIdx()]=i+1
    seen=set()
    for bond in mol.GetBonds():
        a,b=bond.GetBeginAtomIdx(),bond.GetEndAtomIdx(); sa,sb=serial[a],serial[b]
        if (sa,sb) not in seen:
            lines+=[f"CONECT{sa:5d}{sb:5d}\n",f"CONECT{sb:5d}{sa:5d}\n"]; seen.add((sa,sb))
    lines.append("END\n"); return "".join(lines)

# ---- Quick probe: can the generator actually build a system? ---------------
lig0 = LIGANDS[0]  # 'EDS01357518_ent1'
supp = Chem.SDMolSupplier(f'poses_{lig0}.sdf', removeHs=False)
pose_h0 = Chem.AddHs(Chem.RemoveHs(next(iter(supp))), addCoords=True)
pdb0 = f'lig_pose_{lig0}.pdb'
with open(pdb0,'w') as fh: fh.write(mol_to_pdb_block(pose_h0))

lig_pdb0 = PDBFile(pdb0)
wrap0    = MinimalOFFMolecule(pose_h0)
ff_test  = ForceField('implicit/obc2.xml')
gaff_t   = GAFFTemplateGenerator(molecules=[wrap0], forcefield='gaff-2.11')
ff_test.registerTemplateGenerator(gaff_t.generator)
try:
    E_lig0 = calc_energy_kcal(ff_test, lig_pdb0.topology, lig_pdb0.positions)
    print(f"Ligand alone test: {E_lig0:.2f} kcal/mol  ✓  (MM-GBSA is feasible)")
    gaff_ok = True
except Exception as ex:
    print(f"Ligand energy FAILED: {ex}")
    gaff_ok = False
