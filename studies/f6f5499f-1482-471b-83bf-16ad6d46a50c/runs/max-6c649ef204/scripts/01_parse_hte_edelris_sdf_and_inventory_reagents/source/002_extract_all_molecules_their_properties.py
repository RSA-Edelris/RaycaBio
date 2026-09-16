
# Extract all molecules with their properties
records = []
for m in mols:
    props = m.GetPropsAsDict()
    smi = Chem.MolToSmiles(m)
    records.append({
        'name': props.get('MOL_NAME', ''),
        'cas': props.get('CAS_NUMBER', ''),
        'role': props.get('Role', ''),
        'smiles': smi,
        'mw': round(Descriptors.MolWt(m), 1)
    })

df = pd.DataFrame(records)
print(df.to_string())
