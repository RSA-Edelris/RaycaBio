
from rdkit import Chem
from rdkit.Chem import Descriptors, SDWriter
import os

in_sdf  = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_ID_enantio.sdf"
out_sdf = f"{WORK}/CRBN_ligands_prepared.sdf"

def largest_fragment(mol):
    frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
    return max(frags, key=lambda m: m.GetNumHeavyAtoms()) if frags else mol

writer  = SDWriter(out_sdf)
writer.SetKekulize(False)

report_rows, failed = [], []
supplier = Chem.SDMolSupplier(in_sdf, removeHs=True, sanitize=True)

for mol in supplier:
    if mol is None:
        continue
    mol_id = mol.GetProp("_Name").strip()
    stereo  = mol.GetPropsAsDict().get("Stereoisomer", "")
    try:
        m = largest_fragment(mol)
        Chem.SanitizeMol(m)
        m.SetProp("_Name", mol_id)
        m.SetProp("ID",    mol_id)
        m.SetProp("Stereoisomer", stereo)
        mw   = round(Descriptors.ExactMolWt(m), 2)
        hbd  = Descriptors.NumHDonors(m)
        hba  = Descriptors.NumHAcceptors(m)
        rot  = Descriptors.NumRotatableBonds(m)
        logp = round(Descriptors.MolLogP(m), 2)
        for k,v in [("MW",mw),("HBD",hbd),("HBA",hba),("RotBonds",rot),("cLogP",logp)]:
            m.SetProp(k, str(v))
        writer.write(m)
        report_rows.append({"id":mol_id,"MW":mw,"HBD":hbd,"HBA":hba,"rot":rot,"logP":logp,"stereo":stereo})
    except Exception as e:
        failed.append((mol_id, str(e)[:60]))

writer.close()
print(f"✓ {len(report_rows)} ligands prepared  ({len(failed)} failed)  → {out_sdf}")
if failed: print(f"  Failures: {failed[:3]}")
print(f"\n{'ID':<30} {'MW':>8} HBD HBA Rot  logP  Stereo")
for r in report_rows[:10]:
    print(f"  {r['id']:<28} {r['MW']:>8.2f}  {r['HBD']}   {r['HBA']}   {r['rot']}  {r['logP']:>5}  {r['stereo']}")
print(f"\nFile: {os.path.getsize(out_sdf):,} bytes")
