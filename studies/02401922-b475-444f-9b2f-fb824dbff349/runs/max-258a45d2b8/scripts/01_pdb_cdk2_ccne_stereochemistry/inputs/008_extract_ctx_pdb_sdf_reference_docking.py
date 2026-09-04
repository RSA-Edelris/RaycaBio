
# Extract CTX from PDB as SDF for reference docking
import subprocess

# First extract CTX HETATM lines to a mini-PDB
ctx_lines = []
with open(PDB_IN) as f:
    for line in f:
        if line.startswith('HETATM') and ' CTX ' in line:
            ctx_lines.append(line)

with open('ctx_ref.pdb','w') as f:
    f.writelines(ctx_lines)
    f.write('END\n')

# Convert CTX PDB → SDF with obabel (preserves 3D coords from crystal)
r = subprocess.run(
    ['obabel', 'ctx_ref.pdb', '-O', 'ctx_ref.sdf', '-p', '7.4'],
    capture_output=True, text=True
)
print("CTX extract:", r.stderr.strip())

# Verify
suppl_ctx = Chem.SDMolSupplier('ctx_ref.sdf', removeHs=False)
ctx_mol = [m for m in suppl_ctx if m is not None]
print(f"CTX atoms: {ctx_mol[0].GetNumAtoms() if ctx_mol else 'FAILED'}")
if ctx_mol:
    print(f"CTX SMILES: {Chem.MolToSmiles(Chem.RemoveHs(ctx_mol[0]))}")
    print(f"CTX MW: {rdMolDescriptors.CalcExactMolWt(Chem.RemoveHs(ctx_mol[0])):.2f}")
