
# Build the clustered SDF using stored data (results list is still in session namespace)
# Cluster assignments from Butina at Tc >= 0.50
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.MolStandardize import rdMolStandardize
import io

# Cluster map (from Butina output, Tc >= 0.50)
CLUSTER_MAP = {
    'EDS00490706': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00480994': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00490594': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00481762': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00470458': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00474254': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00474362': ('A', 'Aryl_Nacyl_THN_diamide',   7),
    'EDS00459442': ('B', 'Dimethylpyrazole_Nacyl_THN_diamide', 3),
    'EDS00459346': ('B', 'Dimethylpyrazole_Nacyl_THN_diamide', 3),
    'EDS00459274': ('B', 'Dimethylpyrazole_Nacyl_THN_diamide', 3),
    'EDS00492874': ('C', 'Glutaryl_anilide_THN_diamide', 2),
    'EDS00492986': ('C', 'Glutaryl_anilide_THN_diamide', 2),
    'EDS00495858': ('D', 'Top_hit_CF3ether_pyridyl_THN_diamide', 1),
    'EDS00444974': ('E', 'Minimal_isobutyryl_THN_diamide', 1),
    'EDS00469766': ('F', 'GemDiF_cyclohexyl_THN_diamide', 1),
}

CARRY_FORWARD = {
    'EDS00495858': 'carry_forward_priority1',
    'EDS00490706': 'carry_forward',
    'EDS00480994': 'carry_forward_conditional_PAINS',
    'EDS00459346': 'carry_forward',
    'EDS00444974': 'carry_forward_minimal_scaffold',
    'EDS00469766': 'carry_forward',
    'EDS00490594': 'conditional_deprioritise',
    'EDS00481762': 'conditional_deprioritise',
    'EDS00459274': 'conditional',
    'EDS00459442': 'conditional',
    'EDS00474254': 'SAR_point',
    'EDS00474362': 'SAR_point',
    'EDS00470458': 'conditional',
    'EDS00492874': 'set_aside',
    'EDS00492986': 'set_aside',
}

# Write SDF
sdf_out = '/home/ubuntu/rayca-sessions/887d5686-be84-4f6b-9a05-ec8460ca348a-70045e3ed201/ASMS_P841_actives_clustered.sdf'

writer = Chem.SDWriter(sdf_out)

for r in results:
    mol = r['mol']
    eds = r['EDS_Number']
    cl_id, cl_name, cl_size = CLUSTER_MAP[eds]
    
    # Set all properties
    mol.SetProp('EDS_Number',           eds)
    mol.SetProp('Smiles_std',           r['std_smi'])
    mol.SetProp('Smiles_original',      r['Smiles'])
    mol.SetProp('InChIKey',             r['inchi_key'])
    mol.SetProp('Stereo_Configuration', r['Stereo  Configuration'])
    mol.SetProp('HIT_P841',             'Active')
    mol.SetProp('AS_ratio',             r['AS ratio'])
    mol.SetProp('AS_ratio_2',           r['AS ratio 2'])
    mol.SetProp('Avg_BR',               r['Avg BR'])
    mol.SetProp('Hit_rank',             r['Hit_rank'])
    mol.SetProp('RTmin',                r['RTmin'])
    mol.SetProp('RT_check_manual',      r['RT check manual'])
    mol.SetProp('MW',                   str(round(r['pc']['MW'], 2)))
    mol.SetProp('cLogP',                str(r['pc']['cLogP']))
    mol.SetProp('HBD',                  str(r['pc']['HBD']))
    mol.SetProp('HBA',                  str(r['pc']['HBA']))
    mol.SetProp('TPSA',                 str(r['pc']['TPSA']))
    mol.SetProp('RotBonds',             str(r['pc']['RotBonds']))
    mol.SetProp('Cluster_ID',           cl_id)
    mol.SetProp('Cluster_Name',         cl_name)
    mol.SetProp('Cluster_Size',         str(cl_size))
    mol.SetProp('PAINS_flag',           r['pains'])
    mol.SetProp('BRENK_flag',           r['brenk'])
    mol.SetProp('Reactive_flag',        r['react'])
    mol.SetProp('Recommendation',       CARRY_FORWARD.get(eds, 'unknown'))
    mol.SetProp('Assay',                'ASMS_P841')
    mol.SetProp('Clustering_method',    'ECFP4_Butina_Tc0.50')
    
    writer.write(mol)

writer.close()

# Verify
suppl = Chem.SDMolSupplier(sdf_out, removeHs=False)
mols = [m for m in suppl if m is not None]
print(f"Wrote {len(mols)} records to {sdf_out}")
print(f"File size: {__import__('os').path.getsize(sdf_out):,} bytes")

# Quick cluster count check
from collections import Counter
cl_counts = Counter(m.GetProp('Cluster_ID') for m in mols)
print("Cluster counts:", dict(sorted(cl_counts.items())))
