
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, DataStructs

SDF_PATH = '/home/ubuntu/rayca-artifacts/58e70b8d6c265c53a41c3467/files/ASMS.sdf'

actives2, inactives2 = [], []
supp = Chem.SDMolSupplier(SDF_PATH, removeHs=True, sanitize=True)
for m in supp:
    if m is None:
        continue
    cid = m.GetProp('EDS_Number')
    hit = m.GetProp('HIT P841')
    smi = Chem.MolToSmiles(m)
    try:
        asr = float(m.GetProp('AS ratio'))
    except (ValueError, KeyError):
        asr = 0.0
    fp = AllChem.GetMorganFingerprintAsBitVect(m, radius=2, nBits=2048)
    rec = {'cid': cid, 'smi': smi, 'as_ratio': asr, 'fp': fp, 'mol': m}
    if hit == 'Active':
        actives2.append(rec)
    else:
        inactives2.append(rec)

actives2.sort(key=lambda x: -x['as_ratio'])
print(f"Actives: {len(actives2)}, Inactives: {len(inactives2)}")

sel_ids = ['EDS00495858', 'EDS00480994', 'EDS00444974']
sel_act = [a for a in actives2 if a['cid'] in sel_ids]
print("\n=== Selected actives ===")
for a in sel_act:
    print(f"  {a['cid']}  AS={a['as_ratio']:.4f}  MW={Descriptors.ExactMolWt(a['mol']):.0f}")

# Tanimoto of each inactive vs selected actives
act_fps = [a['fp'] for a in sel_act]
sim_rows = []
for ina in inactives2:
    sims = DataStructs.BulkTanimotoSimilarity(ina['fp'], act_fps)
    sim_rows.append((max(sims), ina['cid'], ina['smi'], ina['mol']))
sim_rows.sort(reverse=True)

print("\nTop 10 most-similar inactives:")
for sim, cid, smi, mol in sim_rows[:10]:
    mw = Descriptors.ExactMolWt(mol)
    print(f"  {cid}  Tanimoto={sim:.3f}  MW={mw:.0f}  {smi[:70]}")

# Select top 3 with MW within range and Tanimoto > 0.3
sel_ina = [(sim, cid, smi, mol) for sim, cid, smi, mol in sim_rows
           if sim > 0.25 and 300 < Descriptors.ExactMolWt(mol) < 600][:3]
print("\n=== Selected inactives ===")
for sim, cid, smi, mol in sel_ina:
    print(f"  {cid}  Tanimoto={sim:.3f}  MW={Descriptors.ExactMolWt(mol):.0f}")
    print(f"    {smi}")
