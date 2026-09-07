
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter, ChiralType

def create_enantiomer(mol):
    rw = Chem.RWMol(Chem.Mol(mol))
    for atom in rw.GetAtoms():
        ct = atom.GetChiralTag()
        if ct == ChiralType.CHI_TETRAHEDRAL_CW:
            atom.SetChiralTag(ChiralType.CHI_TETRAHEDRAL_CCW)
        elif ct == ChiralType.CHI_TETRAHEDRAL_CCW:
            atom.SetChiralTag(ChiralType.CHI_TETRAHEDRAL_CW)
    return rw.GetMol()

# Rebuild flat_mols (functions don't cross the boundary)
from rdkit.Chem import SDMolSupplier
input_file = '/home/ubuntu/rayca-artifacts/d43a861c8a85cf7cfd38dce9/files/enantio.sdf'
supplier = SDMolSupplier(input_file, removeHs=True, sanitize=True)

flat_mols = []
for mol in supplier:
    if mol is None:
        continue
    name  = mol.GetProp('_Name')
    chiral = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
    if chiral:
        enant = create_enantiomer(mol)
        flat_mols.append((mol,   f"{name}_ent1"))
        flat_mols.append((enant, f"{name}_ent2"))
    else:
        flat_mols.append((mol, name))

# ── verify enantiomer configs ─────────────────────────────────────────────────
print("Stereocenters before 3D embedding:")
for m, label in flat_mols:
    Chem.AssignStereochemistry(m, cleanIt=True, force=True)
    ci = Chem.FindMolChiralCenters(m, includeUnassigned=True)
    print(f"  {label}: {ci}")

# ── 3D conformer generation ───────────────────────────────────────────────────
print("\nGenerating 3D conformers (ETKDGv3 + MMFF94):")
output_mols = []
params = AllChem.ETKDGv3()
params.randomSeed = 42

for mol2d, label in flat_mols:
    mol3d = Chem.AddHs(mol2d)
    embed_res = AllChem.EmbedMolecule(mol3d, params)
    if embed_res != 0:
        print(f"  {label}: EMBED FAILED — trying distance geometry fallback")
        embed_res = AllChem.EmbedMolecule(mol3d, AllChem.ETKDGv3())
    if embed_res == 0:
        ff_res = AllChem.MMFFOptimizeMolecule(mol3d, maxIters=2000)
        # Compute MMFF energy for reporting
        ff = AllChem.MMFFGetMoleculeForceField(mol3d, AllChem.MMFFGetMoleculeProperties(mol3d))
        energy = ff.CalcEnergy() if ff else float('nan')
        mol3d.SetProp('_Name', label)
        mol3d.SetProp('MMFF94_energy_kcal_mol', f"{energy:.3f}")
        output_mols.append(mol3d)
        status = "converged" if ff_res == 0 else ("not converged" if ff_res == 1 else "no FF")
        print(f"  {label}: OK  E={energy:.2f} kcal/mol  ({status})")
    else:
        print(f"  {label}: FAILED")

# ── write SDF ─────────────────────────────────────────────────────────────────
output_path = '/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/enantio_structure.sdf'
writer = SDWriter(output_path)
writer.SetKekulize(False)
for m in output_mols:
    writer.write(m)
writer.close()

print(f"\nWrote {len(output_mols)} structures to enantio_structure.sdf")
