
sdf_out = '/home/ubuntu/rayca-sessions/887d5686-be84-4f6b-9a05-ec8460ca348a-70045e3ed201/ASMS_P841_actives_clustered.sdf'

writer = Chem.SDWriter(sdf_out)

for r in results:
    mol  = r['mol']
    eds  = r['EDS_Number']
    cl_id, cl_name, cl_size = CLUSTER_MAP[eds]

    mol.SetProp('EDS_Number',          eds)
    mol.SetProp('Smiles_std',          r['std_smi'])
    mol.SetProp('Smiles_original',     r['Smiles'])
    mol.SetProp('InChIKey',            r['inchi_key'])
    mol.SetProp('Stereo_Configuration',r['Stereo  Configuration'])
    mol.SetProp('HIT_P841',            'Active')
    mol.SetProp('AS_ratio',            r['AS ratio'])
    mol.SetProp('AS_ratio_2',          r['AS ratio 2'])
    mol.SetProp('Avg_BR',              r['Avg BR'])
    mol.SetProp('Hit_rank',            r['Hit_rank'])
    mol.SetProp('RTmin',               r['RTmin'])
    mol.SetProp('RT_check_manual',     r['RT check manual'])
    mol.SetProp('MW',                  str(r['pc']['MW']))
    mol.SetProp('cLogP',               str(r['pc']['cLogP']))
    mol.SetProp('HBD',                 str(r['pc']['HBD']))
    mol.SetProp('HBA',                 str(r['pc']['HBA']))
    mol.SetProp('TPSA',                str(r['pc']['TPSA']))
    mol.SetProp('RotBonds',            str(r['pc']['RotBonds']))
    mol.SetProp('Cluster_ID',          cl_id)
    mol.SetProp('Cluster_Name',        cl_name)
    mol.SetProp('Cluster_Size',        str(cl_size))
    mol.SetProp('PAINS_flag',          r['pains'])
    mol.SetProp('BRENK_flag',          r['brenk'])
    mol.SetProp('Recommendation',      CARRY_FORWARD.get(eds, 'unknown'))
    mol.SetProp('Assay',               'ASMS_P841')
    mol.SetProp('Clustering_method',   'ECFP4_Butina_Tc0.50')

    writer.write(mol)

writer.close()

# Verify
import os
suppl = Chem.SDMolSupplier(sdf_out, removeHs=False)
mols  = [m for m in suppl if m is not None]
print(f"Records written : {len(mols)}")
print(f"File size       : {os.path.getsize(sdf_out):,} bytes")
from collections import Counter
print("Cluster counts  :", dict(sorted(Counter(m.GetProp('Cluster_ID') for m in mols).items())))
print("Fields on mol 1 :", list(mols[0].GetPropsAsDict().keys()))
