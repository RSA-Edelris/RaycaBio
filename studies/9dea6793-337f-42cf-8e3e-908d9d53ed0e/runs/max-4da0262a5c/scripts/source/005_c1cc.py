
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import Image
import os

workspace = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4"

# Key intermediates to draw for test_001 through test_004
intermediates = {
    # test_001 intermediates
    "t001_SM1_isoquinolinone": "O=c1cc(-c2ccccc2OC)[nH]c2ccccc12",  # 3-(2-methoxyphenyl)-1(2H)-isoquinolinone
    "t001_SM2_chloroisoquinoline": "Clc1nc(c2ccccc2OC)cc2ccccc12",   # 1-chloro-3-(2-MeO-Ph)isoquinoline
    "t001_SM3_piperidinone": "O=C1CCN(C(=O)c2ccccc2OC)CC1",          # N-(2-methoxybenzoyl)-4-piperidone
    "t001_INT1": "OC1(c2nc(c3ccccc3OC)cc3ccccc23)CCN(C(=O)c2ccccc2OC)CC1",  # tertiary alcohol intermediate
    
    # test_002 intermediates
    "t002_SM1_dichloropurine": "Clc1nc(Cl)c2[nH]cnc2n1",             # 2,6-dichloro-9H-purine
    "t002_SM2_aniline": "Nc1ccc(C(F)(F)F)cc1N",                       # 4-CF3-1,2-phenylenediamine
    "t002_SM3_histamine": "NCCc1c[nH]cn1",                            # histamine
    
    # test_003 intermediates  
    "t003_SM1_glutarimide": "O=C1CCC(N)C(=O)N1",                     # 3-amino glutarimide
    "t003_SM2_THIQ": "O=C(O)[C@@H]1c2ccc(O)cc2CC[C@@H]1c1ccccc1",   # THIQ carboxylic acid
    "t003_SM3_piperazine_linker": "O=C1CN(Cc2ccc(N3CCN(CC4CCN(Cl)CC4)CC3)cc2)Cc3ccccc31",  # isoindolinone-piperazine
    
    # test_004 intermediates
    "t004_GlcNAc_allyl": "C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O",         # allyl GlcNAc
    "t004_glucose_donor": "OCC1OC(O)C(O)C(O)C1O",                    # glucose (simplified, no leaving group)
    "t004_fucose_donor": "OC1OC(C)C(O)C(O)C1O",                      # L-fucose (simplified)
}

drawn = []
for name, smi in intermediates.items():
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        print(f"  PARSE FAILED: {name} ({smi})")
        continue
    AllChem.Compute2DCoords(mol)
    drawer = rdMolDraw2D.MolDraw2DCairo(400, 300)
    drawer.drawOptions().addStereoAnnotation = True
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    path = os.path.join(workspace, f"int_{name}.png")
    with open(path, 'wb') as f:
        f.write(drawer.GetDrawingText())
    drawn.append(name)
    print(f"  OK: {name}")

print(f"\nDrawn {len(drawn)} intermediates")
