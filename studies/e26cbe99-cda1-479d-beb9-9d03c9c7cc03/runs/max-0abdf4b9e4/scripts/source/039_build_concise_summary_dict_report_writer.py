
# Build a concise summary dict for the report writer
import json

RT_KCAL = 0.5921;  LN10 = 2.30259

LIGANDS = ['EDS01357518_ent1','EDS01357518_ent2',
           'EDS01806218_ent1','EDS01806218_ent2','EDS01889984']

from rdkit import Chem

final_results = {}
for lig in LIGANDS:
    supp  = Chem.SDMolSupplier(f'poses_{lig}.sdf', removeHs=False)
    mols  = [m for m in supp if m is not None]
    pose  = mols[0]
    props = pose.GetPropsAsDict()
    vina     = float(props.get('minimizedAffinity', 0))
    cnn_pose = float(props.get('CNNscore', 0))
    cnn_aff  = float(props.get('CNNaffinity', 0))
    dG_cnn   = -RT_KCAL * LN10 * cnn_aff
    final_results[lig] = dict(vina=vina, cnn_pose=cnn_pose,
                               cnn_aff=cnn_aff, dG_cnn=dG_cnn)

print("Summary table:\n")
print(f"{'Compound':<30} {'Vina':>7}  {'CNN_pose':>8}  {'pKi':>6}  {'ΔG_CNN':>9}")
print("-"*68)
for lig,r in final_results.items():
    print(f"{lig:<30} {r['vina']:>7.2f}  {r['cnn_pose']:>8.4f}  "
          f"{r['cnn_aff']:>6.3f}  {r['dG_cnn']:>9.2f}")

# save for report
with open('final_results.json','w') as f:
    json.dump(final_results, f, indent=2)
print("\nfinal_results.json written")
