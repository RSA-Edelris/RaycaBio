
# Build annotated SDF via subprocess (needs venv Python / RDKit)
annot_script = """
import json, sys
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem

BASE     = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
BEST_DIR = BASE / "best_poses2_top1"

dock_list = json.loads((BASE/"docking2_ranked.json").read_text())['ranked']
mmgbsa    = json.loads((BASE/"mmgbsa2_results.json").read_text())
ints_data = json.loads((BASE/"interaction_fingerprints.json").read_text())

dock_map  = {r['name']: r for r in dock_list}
names     = sorted(dock_map.keys())

writer = Chem.SDWriter(str(BASE/"CRBN_ID_enantio2_docking_GBSA.sdf"))

for name in names:
    sdf = BEST_DIR / f"{name}_pose1.sdf"
    mol = Chem.SDMolSupplier(str(sdf), removeHs=False, sanitize=True)[0]
    if mol is None:
        print(f"  WARN: {name} pose1 not loadable", flush=True)
        continue
    d = dock_map[name]
    gb = mmgbsa.get(name, {})
    ifs = ints_data['fingerprints'].get(name, [])

    mol.SetProp('_Name', name)
    mol.SetProp('Parent_Compound', d.get('parent',''))
    mol.SetProp('Docking_Affinity_kcal_mol', f"{d['affinity']:.2f}")
    mol.SetProp('CNN_Affinity',              f"{d['cnn']:.3f}")
    mol.SetProp('CNN_Pose_Score',            f"{d.get('pose_score',0):.3f}")
    mol.SetProp('MMGBSA_dG_kcal_mol',       f"{gb.get('DELTA_TOTAL','N/A')}")
    mol.SetProp('MMGBSA_VdW_kcal_mol',      f"{gb.get('VDWAALS','N/A')}")
    mol.SetProp('MMGBSA_EEL_kcal_mol',      f"{gb.get('EEL','N/A')}")
    mol.SetProp('MMGBSA_EGB_kcal_mol',      f"{gb.get('EGB','N/A')}")
    res_list = sorted(set(i['protein_residue'] for i in ifs))
    mol.SetProp('Interacting_Residues',      ','.join(res_list))
    mol.SetProp('N_Interactions',            str(len(ifs)))
    mol.SetProp('HBond_Residues', ','.join(sorted(set(
        i['protein_residue'] for i in ifs
        if i['interaction'] in ('HBDonor','HBAcceptor')
    ))))
    writer.write(mol)

writer.close()
out = BASE/"CRBN_ID_enantio2_docking_GBSA.sdf"
print(f"Written {out} ({out.stat().st_size:,} bytes), {len(names)} poses")
"""

import subprocess
r = subprocess.run(
    ["/home/ubuntu/rayca-runtime/.venv/bin/python3", "-c", annot_script],
    capture_output=True, text=True,
    cwd="/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e"
)
print(r.stdout)
if r.stderr:
    print("STDERR:", r.stderr[:500])
