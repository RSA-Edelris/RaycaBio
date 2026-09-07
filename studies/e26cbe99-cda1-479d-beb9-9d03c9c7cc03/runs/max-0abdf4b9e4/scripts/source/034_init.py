
import os, io, subprocess, numpy as np
from pdbfixer import PDBFixer
from rdkit import Chem
from rdkit.Chem import AllChem
import openmm as mm
from openmm.app import PDBFile, ForceField, Modeller, NoCutoff
from openmm import unit
from openmmforcefields.generators import GAFFTemplateGenerator

RT_KCAL = 0.5921;  LN10 = 2.30259

# ====================================================================
# Helpers
# ====================================================================
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
    # OBC2 comes from the XML; do NOT pass implicitSolvent= to createSystem in OpenMM 8.x
    system = ff.createSystem(topology, nonbondedMethod=NoCutoff)
    intg = mm.VerletIntegrator(0.001*unit.picoseconds)
    ctx = mm.Context(system, intg, mm.Platform.getPlatformByName('Reference'))
    ctx.setPositions(positions)
    e = ctx.getState(getEnergy=True).getPotentialEnergy()
    del ctx, intg
    return e.value_in_unit(unit.kilojoules_per_mole) / 4.184

# ====================================================================
# Load capped receptor
# ====================================================================
rec_capped = PDBFile('PB-20260903-4CI2_receptor_trimmed_capped.pdb')
ff_base    = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')

E_rec = calc_energy_kcal(ff_base, rec_capped.topology, rec_capped.positions)
print(f"Receptor energy (ff14SB+OBC2): {E_rec:,.1f} kcal/mol  ✓")

# ====================================================================
# MM-GBSA single-point for each ligand
# ====================================================================
DOCKING_DATA = {
    'EDS01357518_ent1': {'vina':-7.52, 'cnn_aff':7.029, 'cnn_pose':0.5577},
    'EDS01357518_ent2': {'vina':-8.09, 'cnn_aff':6.979, 'cnn_pose':0.7692},
    'EDS01806218_ent1': {'vina':-6.81, 'cnn_aff':6.328, 'cnn_pose':0.3036},
    'EDS01806218_ent2': {'vina':-9.08, 'cnn_aff':7.431, 'cnn_pose':0.7395},
    'EDS01889984':      {'vina':-6.63, 'cnn_aff':6.990, 'cnn_pose':0.4955},
}
LIGANDS = list(DOCKING_DATA.keys())

results = {}
for lig in LIGANDS:
    # Load best pose (rank-1)
    supp = Chem.SDMolSupplier(f'poses_{lig}.sdf', removeHs=False)
    mols = [m for m in supp if m is not None]
    pose_noH = Chem.RemoveHs(mols[0])
    pose_h   = Chem.AddHs(pose_noH, addCoords=True)

    # Write ligand PDB to a tempfile
    pdb_block = mol_to_pdb_block(pose_h)
    lig_pdb_path = f'lig_pose_{lig}.pdb'
    with open(lig_pdb_path, 'w') as fh:
        fh.write(pdb_block)

    try:
        lig_pdb = PDBFile(lig_pdb_path)

        # Build ForceField with GAFF-2.11 for the ligand
        ff_cpx = ForceField('amber/ff14SB.xml', 'implicit/obc2.xml')
        lig_wrapper = MinimalOFFMolecule(pose_h)
        gaff_gen = GAFFTemplateGenerator(molecules=[lig_wrapper], forcefield='gaff-2.11')
        ff_cpx.registerTemplateGenerator(gaff_gen.generator)

        # ---- Complex energy ----
        mod_cpx = Modeller(rec_capped.topology, rec_capped.positions)
        mod_cpx.add(lig_pdb.topology, lig_pdb.positions)
        E_cpx = calc_energy_kcal(ff_cpx, mod_cpx.topology, mod_cpx.positions)

        # ---- Ligand-alone energy (same force field, same pose coords) ----
        ff_lig = ForceField('implicit/obc2.xml')
        ff_lig.registerTemplateGenerator(
            GAFFTemplateGenerator(molecules=[lig_wrapper], forcefield='gaff-2.11').generator)
        E_lig = calc_energy_kcal(ff_lig, lig_pdb.topology, lig_pdb.positions)

        dG_mmgbsa = E_cpx - E_rec - E_lig
        results[lig] = {'E_cpx': E_cpx, 'E_rec': E_rec, 'E_lig': E_lig,
                        'dG_mmgbsa': dG_mmgbsa, 'ok': True}
        print(f"{lig}: E_cpx={E_cpx:,.1f}  E_lig={E_lig:.1f}  "
              f"ΔG_MM-GBSA={dG_mmgbsa:.1f} kcal/mol")
    except Exception as ex:
        results[lig] = {'ok': False, 'error': str(ex)[:150]}
        print(f"{lig}: FAILED — {str(ex)[:100]}")

# CNN-based ΔG (primary free energy estimate from gnina)
print("\n--- CNN affinity → ΔG_bind ---")
for lig in LIGANDS:
    pKi = DOCKING_DATA[lig]['cnn_aff']
    dG_cnn = -RT_KCAL * LN10 * pKi
    DOCKING_DATA[lig]['dG_cnn'] = dG_cnn
    print(f"{lig}: pKi={pKi:.3f}  ΔG_CNN={dG_cnn:.2f} kcal/mol")
