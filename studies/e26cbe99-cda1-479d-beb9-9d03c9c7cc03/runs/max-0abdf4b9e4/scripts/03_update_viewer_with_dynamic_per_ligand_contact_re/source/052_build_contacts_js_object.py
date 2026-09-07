
import json

# Build the CONTACTS JS object
contact_data = {
    'EDS01357518_ent1':  [(307,'ASN'),(308,'PRO'),(311,'TYR'),(313,'HIS'),
                          (333,'GLU'),(334,'HIS'),(335,'SER'),(336,'TRP'),
                          (342,'TRP'),(344,'ILE'),(353,'HIS'),(356,'TRP'),
                          (358,'PHE'),(376,'SER')],
    'EDS01357518_ent2':  [(307,'ASN'),(308,'PRO'),(309,'HIS'),(311,'TYR'),
                          (313,'HIS'),(333,'GLU'),(334,'HIS'),(335,'SER'),
                          (336,'TRP'),(342,'TRP'),(344,'ILE'),(353,'HIS'),
                          (356,'TRP'),(358,'PHE')],
    'EDS01806218_ent1':  [(307,'ASN'),(308,'PRO'),(309,'HIS'),(311,'TYR'),
                          (313,'HIS'),(334,'HIS'),(336,'TRP'),(342,'TRP'),
                          (344,'ILE'),(346,'GLN'),(353,'HIS'),(356,'TRP')],
    'EDS01806218_ent2':  [(307,'ASN'),(308,'PRO'),(309,'HIS'),(311,'TYR'),
                          (313,'HIS'),(333,'GLU'),(334,'HIS'),(335,'SER'),
                          (336,'TRP'),(342,'TRP'),(344,'ILE'),(353,'HIS'),
                          (356,'TRP'),(358,'PHE')],
    'EDS01889984':       [(306,'VAL'),(307,'ASN'),(308,'PRO'),(309,'HIS'),
                          (333,'GLU'),(334,'HIS'),(335,'SER'),(336,'TRP'),
                          (342,'TRP'),(356,'TRP')],
    'crystal_lvy':       [(307,'ASN'),(308,'PRO'),(309,'HIS'),(313,'HIS'),
                          (334,'HIS'),(335,'SER'),(336,'TRP'),(337,'PHE'),
                          (342,'TRP'),(356,'TRP'),(358,'PHE')],
}

TRP_RESI = [336, 342, 356]

def make_contact_entry(pairs):
    resi = [r for r,_ in pairs]
    trp  = [r for r,_ in pairs if r in TRP_RESI]
    lbls = [[n, r] for r,n in pairs]
    return {'resi': resi, 'trp': trp, 'labels': lbls}

contacts_obj = {k: make_contact_entry(v) for k, v in contact_data.items()}
contacts_js  = json.dumps(contacts_obj, indent=2)
print("CONTACTS object keys:", list(contacts_obj.keys()))
print("EDS01806218_ent2 resi:", contacts_obj['EDS01806218_ent2']['resi'])
print("crystal_lvy trp:", contacts_obj['crystal_lvy']['trp'])
