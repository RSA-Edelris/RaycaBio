
import subprocess, os
from rdkit import Chem

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
ligands_dir = os.path.join(wd, "ligands_3d")
prot_sdf = os.path.join(wd, "all_protonated_3d.sdf")

# Check protonation: any piperazine-N should be +1 at pH 7.4
suppl = Chem.SDMolSupplier(prot_sdf, removeHs=True, sanitize=True)
prot_mols = [(m.GetProp('_Name'), Chem.GetFormalCharge(m)) for m in suppl if m is not None]
charged = [(n, q) for n, q in prot_mols if q != 0]
print(f"Total: {len(prot_mols)}, with non-zero charge: {len(charged)}")
# Show first 10
for n, q in charged[:10]:
    print(f"  {n}: q={q:+d}")
print("...")

# Check a specific one - CTX-1017233 should be +1 (has piperazine)
suppl2 = Chem.SDMolSupplier(prot_sdf, removeHs=False, sanitize=True)
mols_h = [m for m in suppl2 if m is not None]
for m in mols_h:
    if m.GetProp('_Name') == 'CTX-1017233':
        q = Chem.GetFormalCharge(m)
        smi = Chem.MolToSmiles(Chem.RemoveHs(m))
        print(f"\nCTX-1017233 formal charge: {q:+d}")
        print(f"SMILES: {smi}")
        break
