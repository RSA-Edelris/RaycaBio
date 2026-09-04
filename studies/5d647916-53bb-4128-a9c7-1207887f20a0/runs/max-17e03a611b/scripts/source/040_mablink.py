
smiles_map = {
    'Mablink (full)': MABLINK_SMILES,
    'Exatecan': EXATECAN,
    'Ac-Val-Ala-COOH': AC_VAL_ALA,
    'PAB scaffold': PAB_SCAFFOLD,
    'Mal-PEG2-NHS': MAL_PEG2_NHS,
    'Sarcosine NCA': SAR_NCA,
    'Polysar stub (x4)': POLYSAR4_STUB,
    'Carbamate intermediate': CARBAMATE_INT,
}
for name, smi in smiles_map.items():
    mol = Chem.MolFromSmiles(smi)
    mw = round(Descriptors.MolWt(mol)) if mol else None
    status = 'OK' if mol else 'FAIL'
    print(f"  {status}  MW={mw}  {name}")
