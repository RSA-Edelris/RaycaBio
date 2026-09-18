
import sqlite3
import pandas as pd

db = "/data/chembl.sqlite"
con = sqlite3.connect(db)

# 1. Get CHEMBL3916849 SMILES and basic properties
q = """
SELECT
    md.chembl_id,
    cs.canonical_smiles,
    md.pref_name,
    cp.mw_freebase,
    cp.alogp,
    cp.hbd,
    cp.hba,
    cp.rtb,
    cp.psa
FROM molecule_dictionary md
JOIN compound_structures cs ON md.molregno = cs.molregno
LEFT JOIN compound_properties cp ON md.molregno = cp.molregno
WHERE md.chembl_id = 'CHEMBL3916849'
"""
compound = pd.read_sql(q, con)
print("=== COMPOUND ===")
print(compound.to_string())
