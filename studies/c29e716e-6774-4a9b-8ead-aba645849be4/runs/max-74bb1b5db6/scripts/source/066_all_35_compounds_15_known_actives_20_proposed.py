
from rdkit.Chem import AllChem, SDWriter
import io

# All 35 compounds: 15 known actives + 20 proposed
known_actives = [
    ('EDS00495858', 'O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2', 0.172),
    ('EDS00480994', 'Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)oc2ccccc12', 0.089),
    ('EDS00490594', 'COc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(N5CCN(C)CC5)cc4)nc3C2)ccc2ccccc12', 0.030),
    ('EDS00481762', 'CN1CCN(c2ccc(CNC(=O)c3ccc4c(n3)CN(C(=O)c3cc5ccccc5s3)CC4)cc2)CC1', 0.018),
    ('EDS00469766', 'O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ncccc1Cl)CC2', 0.033),
    ('EDS00459346', 'Cc1cc(C(=O)N2CCc3ccc(C(=O)NCc4cccc(N5CCOCC5)n4)nc3C2)nn1C', 0.021),
    ('EDS00459274', 'Cc1cc(C(=O)N2CCc3ccc(C(=O)NCc4c(F)ccc(F)c4Cl)nc3C2)nn1C', 0.007),
    ('EDS00444974', 'Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C(C)C)CC3)cn1', 0.016),
    ('EDS00492986', 'CCOC(=O)N1CCC(NC(=O)c2ccc3c(n2)CN(C(=O)CCCC(=O)Nc2ccccc2)CC3)CC1', 0.010),
    ('EDS00459442', 'Cc1cc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2cc(C)n(C)n2)CC3)c(C(F)(F)F)o1', 0.008),
    ('EDS00490706', 'COc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccccc4)nc3C2)ccc2ccccc12', 0.001),
    ('EDS00492874', 'CC(C)(CNC(=O)c1ccc2c(n1)CN(C(=O)CCCC(=O)Nc1ccccc1)CC2)c1ccncc1', 0.011),
    ('EDS00470458', 'COc1cscc1C(=O)N1CCc2ccc(C(=O)NCC3(c4ccccc4)CCOCC3)nc2C1', 0.001),
    ('EDS00474254', 'COc1ccc(C)cc1C(=O)N1CCc2ccc(C(=O)NCc3ccsc3)nc2C1', 0.004),
    ('EDS00474362', 'COc1ccc(C)cc1C(=O)N1CCc2ccc(C(=O)NCc3cccc(S(C)(=O)=O)c3)nc2C1', 0.003),
]

proposed = [
    ('A1','O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2'),
    ('A2','O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1cnc(OC(F)(F)F)cc1)CC2'),
    ('A3','O=C(NCc1ccccc1-n1cccc1)c1ccc2c(n1)CN(C(=O)c1ccc(C(F)(F)F)nc1)CC2'),
    ('B1','Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccncc4)nc3C2)oc2ccccc12'),
    ('B2','Cc1c(C(=O)N2CCc3ccc(C(=O)NCC4CCOCC4)nc3C2)oc2ccccc12'),
    ('B3','Cc1c(C(=O)N2CCc3ccc(C(=O)NCc4ccc(F)cc4)nc3C2)oc2ccccc12'),
    ('C1','O=C(NCc1ccc(N2CCOCC2)nc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('C2','O=C(NCc1cccc(F)c1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('C3','O=C(NCc1cnc(C)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('C4','O=C(NCc1ccc(-n2ccnc2)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('D1','O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('D2','O=C(NC1CCC(F)(F)CC1)c1ccc2c(n1)CN(C(=O)c1ccc(F)cc1)CC2'),
    ('E1','Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(F)cc2)CC3)cn1'),
    ('E2','Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)c2ccc(OCC(F)(F)F)nc2)CC3)cn1'),
    ('E3','Cc1cnc(CNC(=O)c2ccc3c(n2)CN(C(=O)C4(F)CC4)CC3)cn1'),
    ('F1','O=C(NCC1(c2ccccc2)CCOCC1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('F2','O=C(NCc1ccsc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('F3','O=C(NCc1cc(F)ccc1F)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('F4','O=C(NCc1ccc(S(C)(=O)=O)cc1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
    ('F5','O=C(NCc1cccc(N2CCOCC2)n1)c1ccc2c(n1)CN(C(=O)c1ccc(OCC(F)(F)F)nc1)CC2'),
]

# Build combined SDF with 3D conformers
def smi_to_3d(name, smi):
    mol = Chem.MolFromSmiles(smi)
    if mol is None: return None
    mol.SetProp('_Name', name)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    if AllChem.EmbedMolecule(mol, params) == -1:
        return None
    AllChem.MMFFOptimizeMolecule(mol)
    return mol

all_compounds = [(n, s, r) for n,s,r in known_actives] + [(n, s, None) for n,s in proposed]

sdf_buf = io.StringIO()
writer = SDWriter(sdf_buf)
n_ok, n_fail = 0, 0
for name, smi, *_ in all_compounds:
    mol = smi_to_3d(name, smi)
    if mol:
        writer.write(mol)
        n_ok += 1
    else:
        print(f"  EMBED FAIL: {name}")
        n_fail += 1
writer.close()
combined_sdf = sdf_buf.getvalue()
print(f"Generated 3D conformers: {n_ok} ok, {n_fail} failed, SDF size: {len(combined_sdf)} bytes")

# Save combined SDF to disk
combined_sdf_path = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/all_35_ligands.sdf'
with open(combined_sdf_path, 'w') as f:
    f.write(combined_sdf)
print(f"Saved to {combined_sdf_path}")
