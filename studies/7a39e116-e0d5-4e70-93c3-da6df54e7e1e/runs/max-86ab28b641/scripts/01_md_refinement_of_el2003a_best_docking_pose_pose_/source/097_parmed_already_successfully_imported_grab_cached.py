
import sys

# ParmEd was already successfully imported; grab the cached module
pmd = sys.modules.get("parmed")
if pmd is None:
    print("parmed not cached — aborting")
else:
    print(f"parmed loaded from cache: {pmd.__version__}")

# MDTraj and OpenMM similarly
mdt  = sys.modules.get("mdtraj")
omm  = sys.modules.get("openmm")
ommapp = sys.modules.get("openmm.app")
ommunit = sys.modules.get("openmm.unit")
print(f"mdtraj  : {mdt.__version__ if mdt else 'MISSING'}")
print(f"openmm  : {omm.__version__ if omm else 'MISSING'}")

work = "gbsa_run/EL2003A_pose2"

# Load GROMACS topology + water-stripped complex PDB
print("\nLoading GROMACS topology...")
gmx = pmd.load_file(f"{work}/complex.top", xyz=f"{work}/complex_reres.pdb")
print(f"  Atoms: {len(gmx.atoms)}, Residues: {len(gmx.residues)}")

res_names = set(r.name for r in gmx.residues)
print(f"  Residue types: {sorted(res_names)}")

for i, r in enumerate(gmx.residues):
    if r.name == "MOL":
        print(f"  Ligand 'MOL' residue index {i}, first atom idx {gmx.residues[i].atoms[0].idx}")
        break
