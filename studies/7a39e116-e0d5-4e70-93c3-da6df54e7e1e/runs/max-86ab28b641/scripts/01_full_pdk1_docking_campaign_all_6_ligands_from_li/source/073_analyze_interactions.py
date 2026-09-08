
from rdkit import Chem
import numpy as np

def analyze_interactions(lig_sdf, rec_atoms_local, rec_xyz_local, rec_elem_local,
                          rec_resid_local, rec_aname_local,
                          hbond_cutoff=3.5, hydro_cutoff=4.5, any_cutoff=5.0):
    """Return dict of interaction lists for one ligand pose."""
    mol = Chem.SDMolSupplier(lig_sdf, removeHs=False)[0]
    if mol is None:
        return {}
    conf = mol.GetConformer()
    lig_atoms = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 1:
            continue  # skip H
        pos = conf.GetAtomPosition(atom.GetIdx())
        lig_atoms.append({
            'idx': atom.GetIdx(),
            'sym': atom.GetSymbol(),
            'xyz': np.array([pos.x, pos.y, pos.z])
        })

    hbonds     = {}  # resid -> list of (dist, aname)
    hydrophob  = {}
    all_contact= {}

    lig_xyz_arr = np.array([a['xyz'] for a in lig_atoms])

    for la in lig_atoms:
        dists = np.linalg.norm(rec_xyz_local - la['xyz'], axis=1)
        for ri, d in enumerate(dists):
            if d > any_cutoff:
                continue
            resid  = rec_resid_local[ri]
            relem  = rec_elem_local[ri]
            raname = rec_aname_local[ri]
            # H-bond: both atoms polar (N/O/S)
            if d <= hbond_cutoff and la['sym'] in {'N','O','S'} and relem in {'N','O','S'}:
                hbonds.setdefault(resid, []).append((round(d,2), raname))
            # Hydrophobic: both C, apolar
            elif d <= hydro_cutoff and la['sym'] == 'C' and relem == 'C':
                hydrophob.setdefault(resid, []).append(round(d,2))
            # General contact (catch π-contacts and other)
            if d <= any_cutoff:
                all_contact.setdefault(resid, []).append(round(d,2))

    # Summarise hydrophobic to min distance per residue
    hydro_sum = {k: min(v) for k, v in hydrophob.items()}
    hbond_sum = {}
    for k, v in hbonds.items():
        v_sorted = sorted(v, key=lambda x: x[0])
        hbond_sum[k] = v_sorted

    return {'hbonds': hbond_sum, 'hydrophobic': hydro_sum, 'contacts': all_contact}

# Run for each best pose
interactions = {}
for lig, row in best_poses.items():
    fname = f"{ART}/all_poses/{lig}_pose{row['rank']}.sdf"
    result = analyze_interactions(fname, rec_atoms, rec_xyz, rec_elem, rec_resid, rec_aname)
    interactions[lig] = result
    print(f"\n=== {lig} (pose{row['rank']}, ΔG={row['mmgbsa']:.2f}) ===")
    print(f"  H-bonds ({len(result['hbonds'])} residues):")
    for res, pairs in sorted(result['hbonds'].items(), key=lambda x: x[1][0][0]):
        for d, an in pairs[:2]:
            print(f"    {res:12s} {an:4s}  {d:.2f} Å")
    print(f"  Hydrophobic ({len(result['hydrophobic'])} residues, top 8 by dist):")
    for res, d in sorted(result['hydrophobic'].items(), key=lambda x: x[1])[:8]:
        print(f"    {res:12s}  {d:.2f} Å")
