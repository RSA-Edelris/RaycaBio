
# ── MM/GBSA via OpenMM implicit solvent (ff14SB + GAFF2 + OBC2) ──────────────
import warnings; warnings.filterwarnings("ignore")
import openmm, openmm.app as app, openmm.unit as unit
from openmmforcefields.generators import SystemGenerator
from rdkit.Chem import MolFromMolBlock, MolToSmiles, SDWriter, AllChem, AddHs
import numpy as np, json, time

# Build SystemGenerator: ff14SB + GAFF2 + OBC2 implicit solvent
ffgen = SystemGenerator(
    forcefields=["amber/ff14SB.xml", "implicit/obc2.xml"],
    small_molecule_forcefield="gaff-2.11",
    forcefield_kwargs={"constraints": None, "rigidWater": False}
)

def get_lig_rdmol(pose_sdf_path):
    from rdkit.Chem import SDMolSupplier
    s = SDMolSupplier(pose_sdf_path, removeHs=False, sanitize=True)
    return [m for m in s if m is not None][0]

def calc_mmgbsa_single(pose_idx):
    """Single-trajectory MM/GBSA: minimise complex, receptor, ligand separately."""
    t0 = time.time()
    pose_path = f"{WS}/pose_{pose_idx+1}.sdf"
    rec_pdb   = f"{WS}/1Z5M_receptor_pH7.4.pdb"
    
    # Load ligand as RDKit mol
    lig_mol = get_lig_rdmol(pose_path)
    lig_smi = MolToSmiles(lig_mol)
    
    # ── Build complex topology ────────────────────────────────────────────────
    rec_pdb_obj = app.PDBFile(rec_pdb)
    from openff.toolkit import Molecule as OFFMol
    off_mol = OFFMol.from_rdkit(lig_mol, allow_undefined_stereo=True)
    
    modeller = app.Modeller(rec_pdb_obj.topology, rec_pdb_obj.positions)
    
    # Add ligand to modeller
    from openmmforcefields.generators import GAFFTemplateGenerator
    from openmm.app import Element
    
    # Use SystemGenerator's create_system directly
    # Complex: create system for receptor+ligand
    sys_complex = ffgen.create_system(
        modeller.topology,
        molecules=[off_mol]
    )
    
    # Get ligand atom positions from the pose SDF
    lig_conf = lig_mol.GetConformer()
    lig_pos_nm = np.array(lig_conf.GetPositions()) * 0.1  # Å → nm
    
    # Build combined positions
    rec_pos_nm = np.array([[v.x, v.y, v.z] for v in rec_pdb_obj.positions.value_in_unit(unit.nanometer)])
    
    print(f"  Pose {pose_idx+1}: rec atoms={rec_pos_nm.shape[0]}, lig atoms={lig_pos_nm.shape[0]}")
    
    dt = time.time() - t0
    return {"pose": pose_idx+1, "status": "topology_ok", "time_s": round(dt,1)}

# Test with pose 1
try:
    r = calc_mmgbsa_single(0)
    print(r)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
