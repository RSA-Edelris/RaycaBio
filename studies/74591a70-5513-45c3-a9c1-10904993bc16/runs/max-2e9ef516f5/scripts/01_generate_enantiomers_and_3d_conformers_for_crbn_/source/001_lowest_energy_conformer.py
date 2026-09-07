
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
import copy

def lowest_energy_conformer(mol, seed=42):
    mol_h = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    params.enforceChirality = True
    rc = AllChem.EmbedMolecule(mol_h, params)
    if rc == -1:
        params2 = AllChem.ETKDG()
        params2.randomSeed = seed
        rc = AllChem.EmbedMolecule(mol_h, params2)
    if rc == -1:
        return None
    mp = AllChem.MMFFGetMoleculeProperties(mol_h)
    ff = AllChem.MMFFGetMoleculeForceField(mol_h, mp) if mp else None
    if ff:
        ff.Minimize(maxIts=2000)
    else:
        AllChem.UFFOptimizeMolecule(mol_h, maxIters=2000)
    return Chem.RemoveHs(mol_h)

def invert_all_stereocenters(mol):
    enantiomer = copy.deepcopy(mol)
    for atom in enantiomer.GetAtoms():
        chi = atom.GetChiralTag()
        if chi == Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW:
            atom.SetChiralTag(Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW)
        elif chi == Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW:
            atom.SetChiralTag(Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW)
    return enantiomer

in_path  = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_ID.sdf"
out_path = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_ID_enantio.sdf"

supplier = Chem.SDMolSupplier(in_path, removeHs=False, sanitize=True)
output_rows = []

for mol in supplier:
    if mol is None:
        print("WARNING: skipped None molecule")
        continue

    mol_id = mol.GetProp("_Name").strip()
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)

    chiral_centers = [(a.GetIdx(), str(a.GetChiralTag()))
                      for a in mol.GetAtoms()
                      if a.GetChiralTag() != Chem.rdchem.ChiralType.CHI_UNSPECIFIED]

    print(f"\n{mol_id}: {len(chiral_centers)} chiral centre(s): {chiral_centers}")

    mol_3d = lowest_energy_conformer(mol)
    if mol_3d is None:
        print(f"  ✗ 3D embedding FAILED for {mol_id}")
        continue
    mol_3d.SetProp("_Name", mol_id)
    mol_3d.SetProp("ID", mol_id)
    mol_3d.SetProp("Stereoisomer", "original")
    output_rows.append(mol_3d)
    print(f"  ✓ original conformer ok")

    if chiral_centers:
        enant = invert_all_stereocenters(mol)
        enant_id = mol_id + "_ent"
        enant_3d = lowest_energy_conformer(enant)
        if enant_3d is None:
            print(f"  ✗ 3D embedding FAILED for enantiomer of {mol_id}")
        else:
            enant_3d.SetProp("_Name", enant_id)
            enant_3d.SetProp("ID", enant_id)
            enant_3d.SetProp("Stereoisomer", "enantiomer")
            output_rows.append(enant_3d)
            print(f"  ✓ enantiomer conformer ok → {enant_id}")
    else:
        print(f"  — no defined stereocenters; skipping enantiomer")

writer = SDWriter(out_path)
for m in output_rows:
    writer.write(m)
writer.close()

print(f"\n{'='*60}")
print(f"Total structures written: {len(output_rows)}")
print(f"Output: {out_path}")
