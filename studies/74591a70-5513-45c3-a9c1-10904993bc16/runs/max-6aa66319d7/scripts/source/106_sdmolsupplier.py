
from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
from rdkit.Chem import AllChem, SDMolSupplier

V2000_SDF = f"{BASE}/CRBN_lig_results_2_v2000.sdf"

sup = SDMolSupplier(V2000_SDF, removeHs=False)
mols = [m for m in sup if m is not None]
print(f"Molecules read: {len(mols)}")

for m in mols:
    name = m.GetProp('_Name') if m.HasProp('_Name') else 'unnamed'
    # strip Hs for analysis
    m_noh = Chem.RemoveHs(m)
    chiral = Chem.FindMolChiralCenters(m_noh, includeUnassigned=True)
    assigned = Chem.FindMolChiralCenters(m_noh, includeUnassigned=False)
    print(f"  {name}: heavy atoms={m_noh.GetNumAtoms()}, "
          f"chiral centers (all)={len(chiral)}, assigned={len(assigned)}")
    print(f"    centers: {chiral}")
