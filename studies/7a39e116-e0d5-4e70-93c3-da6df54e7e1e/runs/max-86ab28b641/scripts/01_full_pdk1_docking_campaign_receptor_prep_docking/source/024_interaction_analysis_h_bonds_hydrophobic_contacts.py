
# ── Interaction analysis: H-bonds, hydrophobic contacts, π-π ─────────────────
import numpy as np
from rdkit.Chem import MolFromMolBlock, MolToSmiles

# Load receptor atoms from prepared PDB (no hydrogens in receptor HETATM/ATOM section)
rec_lines = open(f"{WS}/1Z5M_receptor_pH7.4.pdb").readlines()

rec_atoms = []
for l in rec_lines:
    if l.startswith("ATOM") or l.startswith("HETATM"):
        rec_atoms.append({
            "resname": l[17:20].strip(),
            "chain":   l[21],
            "resnum":  int(l[22:26].strip()),
            "aname":   l[12:16].strip(),
            "elem":    l[76:78].strip() if len(l)>77 else l[13:14],
            "xyz":     np.array([float(l[30:38]), float(l[38:46]), float(l[46:54])])
        })

rec_xyz   = np.array([a["xyz"] for a in rec_atoms])
rec_aname = [a["aname"] for a in rec_atoms]
rec_elem  = [a.get("elem","C") for a in rec_atoms]

def get_interactions(mol, label="pose"):
    lig_conf  = mol.GetConformer()
    lig_pos   = np.array(lig_conf.GetPositions())
    
    # Residues within 4.5 Å of any ligand atom
    dmat = np.sqrt(((rec_xyz[:,None,:] - lig_pos[None,:,:])**2).sum(axis=2))  # Nrec × Nlig
    min_d = dmat.min(axis=1)   # per receptor atom, closest ligand atom
    
    close_mask = min_d < 4.5
    binding_res = sorted(set((a["resname"],a["resnum"]) for a,m in zip(rec_atoms,close_mask) if m))
    
    # H-bond donors / acceptors: N, O atoms
    hbond_donors    = [i for i,a in enumerate(rec_atoms) if close_mask[i] and a["aname"][0] in "NO"]
    lig_acceptors   = [i for i,at in enumerate(mol.GetAtoms()) 
                       if at.GetSymbol() in ("N","O","F")]
    
    hbonds = []
    for ri in hbond_donors:
        for li in lig_acceptors:
            d = np.linalg.norm(rec_xyz[ri] - lig_pos[li])
            if d < 3.2:
                hbonds.append((rec_atoms[ri]["resname"],
                               rec_atoms[ri]["resnum"],
                               rec_atoms[ri]["aname"],
                               round(float(d),2)))
    
    # Hydrophobic contacts: C–C within 4.5 Å
    hphob_rec = [i for i,a in enumerate(rec_atoms) if close_mask[i] and a["aname"][0] == "C"]
    lig_C = [i for i,at in enumerate(mol.GetAtoms()) if at.GetSymbol() == "C"]
    
    hphob = []
    seen_res = set()
    for ri in hphob_rec:
        for li in lig_C:
            d = np.linalg.norm(rec_xyz[ri] - lig_pos[li])
            if d < 4.5:
                key = (rec_atoms[ri]["resname"], rec_atoms[ri]["resnum"])
                if key not in seen_res:
                    hphob.append(key)
                    seen_res.add(key)
    
    return {
        "label": label,
        "binding_residues": binding_res[:20],
        "hbonds": hbonds[:15],
        "hydrophobic": list(seen_res)[:20]
    }

# Analyze all 5 poses
interaction_results = []
for i, mol in enumerate(pose_mols[:5]):
    r = get_interactions(mol, f"pose_{i+1}")
    interaction_results.append(r)
    print(f"\n{'='*60}")
    print(f"Pose {i+1} | Vina {pose_data[i]['minimizedAffinity']:.3f} kcal/mol | CNN {pose_data[i]['CNNscore']:.4f}")
    print(f"  H-bonds ({len(r['hbonds'])}):")
    for hb in r['hbonds']:
        print(f"    {hb[0]}{hb[1]} {hb[2]} d={hb[3]} Å")
    print(f"  Hydrophobic contacts ({len(r['hydrophobic'])}):")
    for hp in sorted(r['hydrophobic'])[:10]:
        print(f"    {hp[0]}{hp[1]}")
