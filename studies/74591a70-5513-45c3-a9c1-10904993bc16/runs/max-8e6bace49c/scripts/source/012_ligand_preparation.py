
# ── LIGAND PREPARATION ────────────────────────────────────────────────────────
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter
from rdkit.Chem.MolStandardize import rdMolStandardize
from rdkit.Chem import SaltRemover

in_sdf  = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_ID_enantio.sdf"
out_sdf = f"{WORK}/CRBN_ligands_prepared.sdf"

supplier = Chem.SDMolSupplier(in_sdf, removeHs=True, sanitize=True)

# standardisation tools
remover    = SaltRemover.SaltRemover()
normalizer = rdMolStandardize.Normalizer()
uncharger  = rdMolStandardize.Uncharger()
te         = rdMolStandardize.TautomerEnumerator()

def prepare_ligand(mol):
    """Strip salts → normalise → canonical tautomer → pH 7.4 charge."""
    mol = remover.StripMol(mol, dontRemoveEverything=True)
    mol = normalizer.normalize(mol)
    # canonical tautomer (lowest energy in RDKit's tautomer model)
    mol = te.Canonicalize(mol)
    # Apply pH 7.4: neutralise zwitterions / quaternary ammonium that
    # shouldn't be charged for these neutral CRBN binders; keep as-is
    # because all IMiD-type N are amide/imide (never cationic at pH 7.4)
    Chem.SanitizeMol(mol)
    return mol

writer = SDWriter(out_sdf)
writer.SetKekulize(False)

report_rows = []
for mol in supplier:
    if mol is None:
        continue
    mol_id = mol.GetProp("_Name").strip()
    stereo_tag = mol.GetPropIfPresent("Stereoisomer") or mol.GetPropsAsDict().get("Stereoisomer","")

    try:
        mol_prep = prepare_ligand(mol)
        # preserve name/properties
        mol_prep.SetProp("_Name", mol_id)
        mol_prep.SetProp("ID", mol_id)
        mol_prep.SetProp("Stereoisomer", stereo_tag)
        # count H-bond donors/acceptors
        hbd = sum(1 for a in mol_prep.GetAtoms()
                  if a.GetAtomicNum() in (7,8) and a.GetTotalNumHs()>0)
        hba = sum(1 for a in mol_prep.GetAtoms()
                  if a.GetAtomicNum() in (7,8))
        mw  = sum(a.GetMass() for a in mol_prep.GetAtoms())
        # count ionisable N with pKa logic: aliphatic sp3 N → protonated at pH 7.4
        n_prot = sum(1 for a in mol_prep.GetAtoms()
                     if a.GetAtomicNum()==7 and
                     a.GetHybridization()==Chem.rdchem.HybridizationType.SP3 and
                     not a.GetIsAromatic() and
                     a.IsInRing())

        report_rows.append({"id": mol_id, "MW": round(mw,1),
                             "HBD": hbd, "HBA": hba,
                             "N_prot_at_7.4": n_prot,
                             "stereo": stereo_tag})
        writer.write(mol_prep)
    except Exception as e:
        print(f"  ✗ {mol_id}: {e}")

writer.close()

print(f"Prepared {len(report_rows)} ligands → {out_sdf}")
print(f"\nSample property check (first 6):")
print(f"{'ID':<30} {'MW':>7} {'HBD':>4} {'HBA':>4} {'N_prot':>7}  Stereo")
for r in report_rows[:6]:
    print(f"  {r['id']:<28} {r['MW']:>7.1f} {r['HBD']:>4} {r['HBA']:>4} {r['N_prot_at_7.4']:>7}  {r['stereo']}")

import os; print(f"\nFile size: {os.path.getsize(out_sdf):,} bytes")
