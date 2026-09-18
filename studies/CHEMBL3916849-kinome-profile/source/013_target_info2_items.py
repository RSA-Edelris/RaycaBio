
import requests, time
BASE = "https://www.ebi.ac.uk/chembl/api/data"

# target_info2 has 50 targets — extract UniProt accessions
uniprots_from_training = {cid: info['uniprot'] for cid, info in target_info2.items() if info.get('uniprot')}
print(f"Training targets with UniProt: {len(uniprots_from_training)}")

# Separately fetch key kinase targets by individual REST call (Aurora A + known clinical kinases)
key_kinases = {
    'CHEMBL4722': 'Aurora kinase A',
    'CHEMBL2185': 'Aurora kinase B', 
    'CHEMBL1907': 'CDK1',
    'CHEMBL1974': 'CDK2',
    'CHEMBL406': 'EGFR',
    'CHEMBL4536': 'ALK',
    'CHEMBL3234': 'RET',
    'CHEMBL2179': 'PLK1',
    'CHEMBL2996': 'HASPIN',
    'CHEMBL5600': 'MARK3',
    'CHEMBL5754': 'MARK4',
    'CHEMBL5408': 'TBK1',
    'CHEMBL2111367': 'NUAK1',
    'CHEMBL3045': 'BRD4',  # not kinase but for negative ctrl
}

key_uniprot = {}
for cid in key_kinases:
    try:
        r = requests.get(f"{BASE}/target/{cid}.json", timeout=15)
        t = r.json()
        comps = t.get('target_components', [])
        acc = comps[0].get('accession', '') if comps else ''
        key_uniprot[cid] = {'name': t.get('pref_name',''), 'uniprot': acc}
        time.sleep(0.1)
    except Exception as e:
        key_uniprot[cid] = {'name': key_kinases[cid], 'uniprot': '', 'err': str(e)}

print("\nKey kinase UniProt accessions:")
for cid, info in key_uniprot.items():
    print(f"  {cid} {info['name']:40s} {info['uniprot']}")
