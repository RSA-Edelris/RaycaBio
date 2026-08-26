
from rdkit import Chem
from rdkit.Chem import inchi as rdInchi
from rdkit.Chem.MolStandardize import rdMolStandardize

p841_path = "/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/P841_proposed_actives.sdf"
cedilla_path = "/home/ubuntu/rayca-artifacts/01def6985d02e054243c1afc/files/Cedilla_list.sdf"

lfc = rdMolStandardize.LargestFragmentChooser()
te = rdMolStandardize.TautomerEnumerator()
uncharger = rdMolStandardize.Uncharger()

def standardize_ikey(mol):
    try:
        m = lfc.choose(mol)
        m = rdMolStandardize.Cleanup(m)
        m = uncharger.uncharge(m)
        m = te.Canonicalize(m)
        return rdInchi.MolToInchiKey(m) or ''
    except Exception:
        return ''

def load_sdf(path):
    records = {}  # ikey -> props dict
    fails = 0
    for mol in Chem.SDMolSupplier(path, sanitize=True, removeHs=True):
        if mol is None:
            fails += 1
            continue
        ikey = standardize_ikey(mol)
        if ikey:
            records[ikey] = mol.GetPropsAsDict()
    return records, fails

p841, p841_fail = load_sdf(p841_path)
cedilla, cedilla_fail = load_sdf(cedilla_path)

print(f"P841 proposed actives : {len(p841)} unique ({p841_fail} failed)")
print(f"Cedilla list          : {len(cedilla)} unique ({cedilla_fail} failed)")

overlap = set(p841.keys()) & set(cedilla.keys())
print(f"\nOverlap: {len(overlap)} structures in both files\n")

if overlap:
    # Print details for each match
    print(f"{'InChIKey':<30} {'P841 props':<40} {'Cedilla props'}")
    print("-"*100)
    for ikey in sorted(overlap):
        p_props = p841[ikey]
        c_props = cedilla[ikey]
        print(f"{ikey}")
        print(f"  P841:    {p_props}")
        print(f"  Cedilla: {c_props}")
        print()
else:
    print("No structures in common.")
    # Check if maybe SMILES comparison needed - peek at first few entries from each
    print("\n--- Sample P841 InChIKeys ---")
    for k in list(p841.keys())[:3]:
        print(f"  {k}: {p841[k]}")
    print("\n--- Sample Cedilla InChIKeys ---")
    for k in list(cedilla.keys())[:3]:
        print(f"  {k}: {cedilla[k]}")
