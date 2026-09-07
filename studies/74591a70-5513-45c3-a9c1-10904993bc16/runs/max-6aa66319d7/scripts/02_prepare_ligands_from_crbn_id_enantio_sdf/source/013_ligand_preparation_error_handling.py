
# ── LIGAND PREPARATION - with error handling ──────────────────────────────────
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import SaltRemover
import os

in_sdf  = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_ID_enantio.sdf"
out_sdf = f"{WORK}/CRBN_ligands_prepared.sdf"

remover    = SaltRemover.SaltRemover()
normalizer = rdMolStandardize.Normalizer()
te         = rdMolStandardize.TautomerEnumerator()

writer = SDWriter(out_sdf)
writer.SetKekulize(False)

report_rows = []
failed = []

# SDMolSupplier with sanitize=True, removeHs=True
supplier = Chem.SDMolSupplier(in_sdf, removeHs=True, sanitize=True)

for mol in supplier:
    if mol is None:
        continue
    mol_id = mol.GetProp("_Name").strip()
    props  = mol.GetPropsAsDict()
    stereo = props.get("Stereoisomer", "")

    try:
        # 1. strip salts
        m = remover.StripMol(mol, dontRemoveEverything=True)
        # 2. normalise functional groups
        m = normalizer.normalize(m)
        # 3. canonical tautomer
        try:
            m = te.Canonicalize(m)
        except Exception:
            pass   # keep current tautomer if enumerator fails
        Chem.SanitizeMol(m)

        # 4. pH 7.4 protonation:
        #    • imide/amide N (glutarimide NH, pKa≈9): neutral — already correct
        #    • sp3 ring N (piperidine/pyrrolidine, pKa≈10): protonate (add H)
        #    RDKit keeps H on these already as part of normal valence

        m.SetProp("_Name", mol_id)
        m.SetProp("ID", mol_id)
        m.SetProp("Stereoisomer", stereo)

        mw  = round(sum(a.GetMass() for a in m.GetAtoms()), 1)
        hbd = rdMolStandardize.RDKit_UFF_MMFF_ChargesFor(m) if False else \
              sum(1 for a in m.GetAtoms()
                  if a.GetAtomicNum() in (7,8) and a.GetTotalNumHs()>0)
        hba = sum(1 for a in m.GetAtoms() if a.GetAtomicNum() in (7,8))
        rot = AllChem.CalcNumRotatableBonds(m)

        m.SetProp("MW",  str(mw))
        m.SetProp("HBD", str(hbd))
        m.SetProp("HBA", str(hba))
        m.SetProp("RotBonds", str(rot))

        writer.write(m)
        report_rows.append({"id": mol_id, "MW": mw, "HBD": hbd,
                             "HBA": hba, "rot": rot, "stereo": stereo})
    except Exception as e:
        failed.append((mol_id, str(e)))
        print(f"  ✗ {mol_id}: {e}")

writer.close()

print(f"✓ Prepared {len(report_rows)}/{len(report_rows)+len(failed)} ligands → {out_sdf}")
if failed:
    print(f"  Failed: {[x[0] for x in failed]}")

print(f"\n{'ID':<30} {'MW':>7} HBD HBA Rot  Stereo")
for r in report_rows[:8]:
    print(f"  {r['id']:<28} {r['MW']:>7.1f}  {r['HBD']}   {r['HBA']}   {r['rot']}  {r['stereo']}")
print(f"\nFile: {os.path.getsize(out_sdf):,} bytes")
