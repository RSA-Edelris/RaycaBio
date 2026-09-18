
import requests, time, pandas as pd
BASE = "https://www.ebi.ac.uk/chembl/api/data"
UNIPROT_BASE = "https://rest.uniprot.org/uniprotkb"

# Fetch sequences for the 50 training targets
for cid, info in target_info2.items():
    acc = info.get('uniprot', '')
    if acc and acc not in seq_map:
        try:
            r = requests.get(f"{UNIPROT_BASE}/{acc}.fasta", timeout=12)
            if r.status_code == 200:
                lines = r.text.strip().split('\n')
                seq_map[acc] = ''.join(lines[1:])
        except:
            pass
        time.sleep(0.1)

print(f"Total sequences in seq_map: {len(seq_map)}")

# Filter training data to targets we have sequences for
training_targets = {cid: info for cid, info in target_info2.items() 
                    if info.get('uniprot') and info['uniprot'] in seq_map}
print(f"Training targets with sequences: {len(training_targets)}")

# Filter df_raw to those targets, drop bad pchembl
df_train = df_raw[df_raw['target_chembl_id'].isin(training_targets.keys())].copy()
df_train = df_train[df_train['pchembl_value'].notna()].copy()
df_train['pchembl_value'] = df_train['pchembl_value'].astype(float)
print(f"Training activity rows: {len(df_train)}")
print(f"Unique compounds in training: {df_train['molecule_chembl_id'].nunique()}")
