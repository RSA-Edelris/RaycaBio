
import os, gzip, subprocess, tempfile, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import openmm as mm
from openmm.app import PDBFile, ForceField, Modeller, NoCutoff, OBC2
from openmm import unit
from openmmforcefields.generators import GAFFTemplateGenerator

RT_KCAL = 0.5921   # kcal/mol at 298K
LN10    = 2.30259

# ---- Redefine the wrapper (functions don't cross cell boundary) ----------
class MinimalOFFMolecule:
    """Thin wrapper so GAFFTemplateGenerator accepts an RDKit mol."""
    def __init__(self, rdmol):
        self._rdmol = rdmol
        self.name   = 'LIG'
    def to_smiles(self, mapped=False, **kw):
        return Chem.MolToSmiles(Chem.RemoveHs(self._rdmol))
    def to_rdkit(self):
        return self._rdmol
    def to_file(self, path, file_format):
        """Write to SDF or mol2 (mol2 via obabel)."""
        fmt = file_format.lower().lstrip('.')
        if fmt in ('sdf', 'mol'):
            w = Chem.SDWriter(path)
            w.write(self._rdmol)
            w.close()
        else:                                      # mol2, pdbqt, ...
            sdf_tmp = path + '.tmp.sdf'
            w = Chem.SDWriter(sdf_tmp)
            w.write(self._rdmol)
            w.close()
            subprocess.run(['obabel', '-isdf', sdf_tmp,
                            f'-o{fmt}', '-O', path],
                           capture_output=True, check=True)
            os.unlink(sdf_tmp)
    @property
    def n_atoms(self):
        return self._rdmol.GetNumAtoms()

# ---- Docking results (Phase 3) -------------------------------------------
DOCKING_DATA = {
    'EDS01357518_ent1': {'vina': -7.52, 'cnn_aff': 7.029, 'cnn_pose': 0.5577},
    'EDS01357518_ent2': {'vina': -8.09, 'cnn_aff': 6.979, 'cnn_pose': 0.7692},
    'EDS01806218_ent1': {'vina': -6.81, 'cnn_aff': 6.328, 'cnn_pose': 0.3036},
    'EDS01806218_ent2': {'vina': -9.08, 'cnn_aff': 7.431, 'cnn_pose': 0.7395},
    'EDS01889984':       {'vina': -6.63, 'cnn_aff': 6.990, 'cnn_pose': 0.4955},
}
LIGANDS = list(DOCKING_DATA.keys())

# ---- Load best poses from docked SDF files --------------------------------
best_poses_h = {}   # rdkit mol with H and 3D coords
best_poses_props = {}

for lig in LIGANDS:
    sdf_path = f'poses_{lig}.sdf'
    supp = Chem.SDMolSupplier(sdf_path, removeHs=False)
    mols = [m for m in supp if m is not None]
    pose_raw = mols[0]                          # rank-1 pose
    props    = pose_raw.GetPropsAsDict()
    pose_noH = Chem.RemoveHs(pose_raw)
    pose_h   = Chem.AddHs(pose_noH, addCoords=True)
    best_poses_h[lig]    = pose_h
    best_poses_props[lig] = props
    print(f"{lig}: Vina={props.get('minimizedAffinity','?'):.3f}  "
          f"CNN={props.get('CNNaffinity','?'):.3f}  "
          f"atoms(+H)={pose_h.GetNumAtoms()}")
