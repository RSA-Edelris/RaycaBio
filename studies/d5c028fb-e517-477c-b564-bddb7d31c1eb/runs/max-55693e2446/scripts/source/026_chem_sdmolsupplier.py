
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors, AllChem, Descriptors, DataStructs
import numpy as np

SDF_PATH = '/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf'

actives2, inactives2 = [], []
supp = Chem.SDMolSupplier(SDF_PATH, removeHs=True, sanitize=True)
for m in supp:
    if m is None:
        continue
    cid  = m.GetProp('EDS_Number')
    hit  = m.GetProp('HIT P841')
    smi  = Chem.MolToSmiles(m)
    asr  = float(m.GetProp('AS ratio'))
    fp   = AllChem.GetMorganFingerprintAsBitVect(m, radius=2, nBits=2048)
    if hit == 'Active':
        actives2.append({'cid': cid, 'smi': smi, 'as_ratio': asr, 'fp': fp, 'mol': m})
    else:
        inactives2.append({'cid': cid, 'smi': smi, 'fp': fp, 'mol': m})

actives2.sort(key=lambda x: -x['as_ratio'])
print(f"Actives: {len(actives2)}, Inactives: {len(inactives2)}")

# Selected actives
sel_ids = ['EDS00495858', 'EDS00480994', 'EDS00444974']
sel_act  = [a for a in actives2 if a['cid'] in sel_ids]
print("\n=== Selected actives ===")
for a in sel_act:
    mw = Descriptors.ExactMolWt(a['mol'])
    print(f"  {a['cid']}  AS={a['as_ratio']:.4f}  MW={mw:.0f}")

# Compute Tanimoto of every inactive vs each selected active; keep max
act_fps = [a['fp'] for a in sel_act]
print("\nComputing Tanimoto similarities to inactives …")
sim_rows = []
for ina in inactives2:
    sims = DataStructs.BulkTanimotoSimilarity(ina['fp'], act_fps)
    sim_rows.append((max(sims), ina['cid'], ina['smi'], ina['mol']))

sim_rows.sort(reverse=True)
print("Top 10 most-similar inactives to selected actives (ECFP4 Tanimoto):")
for sim, cid, smi, mol in sim_rows[:10]:
    mw = Descriptors.ExactMolWt(mol)
    print(f"  {cid}  Tanimoto={sim:.3f}  MW={mw:.0f}  {smi[:70]}")
