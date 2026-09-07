
import os, subprocess, tempfile, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import openmm as mm
from openmm.app import PDBFile, ForceField, Modeller, NoCutoff
from openmm import unit
from openmmforcefields.generators import GAFFTemplateGenerator

# --- Redefine wrapper (cannot persist across calls) ---
class MinimalOFFMolecule:
    def __init__(self, rdmol):
        self._rdmol = rdmol
        self.name   = 'LIG'
    def to_smiles(self, mapped=False, **kw):
        return Chem.MolToSmiles(Chem.RemoveHs(self._rdmol))
    def to_rdkit(self):
        return self._rdmol
    def to_file(self, path, file_format):
        fmt = file_format.lower().lstrip('.')
        if fmt in ('sdf', 'mol'):
            w = Chem.SDWriter(path); w.write(self._rdmol); w.close()
        else:
            sdf_tmp = path + '.tmp.sdf'
            w = Chem.SDWriter(sdf_tmp); w.write(self._rdmol); w.close()
            subprocess.run(['obabel', '-isdf', sdf_tmp,
                            f'-o{fmt}', '-O', path], capture_output=True, check=True)
            os.unlink(sdf_tmp)
    @property
    def n_atoms(self):
        return self._rdmol.GetNumAtoms()

def mol_to_pdb_block(mol, res_name='LIG', chain_id='Z', res_seq=1):
    """Write RDKit mol (3D, with H) to PDB-format string with CONECT records."""
    conf  = mol.GetConformer()
    lines = []
    serial = {}
    for i, atom in enumerate(mol.GetAtoms()):
        idx   = atom.GetIdx()
        pos   = conf.GetAtomPosition(idx)
        elem  = atom.GetSymbol()
        # 4-char atom name: right-pad element + index
        aname = f"{elem}{i+1}"
        aname = (f" {aname:<3s}" if len(elem)==1 else f"{aname:<4s}")
        line  = (f"HETATM{i+1:5d} {aname} {res_name:3s} {chain_id}{res_seq:4d}    "
                 f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}  1.00  0.00          {elem:>2s}\n")
        lines.append(line)
        serial[idx] = i + 1
    seen = set()
    for bond in mol.GetBonds():
        a, b = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        sa, sb = serial[a], serial[b]
        if (sa, sb) not in seen:
            lines.append(f"CONECT{sa:5d}{sb:5d}\n")
            lines.append(f"CONECT{sb:5d}{sa:5d}\n")
            seen.add((sa, sb))
    lines.append("END\n")
    return "".join(lines)

def single_point_energy(ff, topology, positions):
    """Return potential energy in kcal/mol for the given topology+positions."""
    try:
        system = ff.createSystem(topology, nonbondedMethod=NoCutoff,
                                 implicitSolvent=mm.app.OBC2,
                                 soluteDielectric=1.0,
                                 solventDielectric=78.5)
    except Exception as e:
        return None, str(e)
    integrator = mm.VerletIntegrator(0.001 * unit.picoseconds)
    platform   = mm.Platform.getPlatformByName('Reference')
    ctx = mm.Context(system, integrator, platform)
    ctx.setPositions(positions)
    state = ctx.getState(getEnergy=True)
    e_kj  = state.getPotentialEnergy().value_in_unit(unit.kilojoules_per_mole)
    del ctx, integrator
    return e_kj / 4.184, None   # kcal/mol

# ---- Step 1: Test receptor loading ----------------------------------------
print("Loading receptor with ff14SB + OBC2 ...")
try:
    rec_pdb  = PDBFile('PB-20260903-4CI2_receptor_trimmed.pdb')
    ff_rec   = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
    e_rec_kcal, err = single_point_energy(ff_rec, rec_pdb.topology, rec_pdb.positions)
    if err:
        print(f"  Receptor energy FAILED: {err[:120]}")
        rec_ok = False
    else:
        print(f"  Receptor energy: {e_rec_kcal:.2f} kcal/mol  OK")
        rec_ok = True
except Exception as ex:
    print(f"  Receptor load FAILED: {ex}")
    rec_ok = False
