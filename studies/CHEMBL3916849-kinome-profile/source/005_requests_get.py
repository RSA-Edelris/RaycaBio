
import requests, json

BASE = "https://www.ebi.ac.uk/chembl/api/data"

# 1. Compound data
r = requests.get(f"{BASE}/molecule/CHEMBL3916849.json", timeout=30)
mol = r.json()
print("=== CHEMBL3916849 ===")
print("Pref name:", mol.get('pref_name'))
print("SMILES:", mol['molecule_structures']['canonical_smiles'])
print("MW:", mol['molecule_properties']['mw_freebase'])
print("AlogP:", mol['molecule_properties']['alogp'])
print("HBD:", mol['molecule_properties']['hbd'])
print("HBA:", mol['molecule_properties']['hba'])
print("PSA:", mol['molecule_properties']['psa'])
print("Max phase:", mol.get('max_phase'))
print("Indication class:", mol.get('indication_class'))
