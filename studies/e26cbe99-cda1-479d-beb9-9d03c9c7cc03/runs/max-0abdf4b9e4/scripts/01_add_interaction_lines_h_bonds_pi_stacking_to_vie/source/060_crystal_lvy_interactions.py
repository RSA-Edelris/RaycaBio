
import re

# ── Crystal LVY interactions ───────────────────────────────────────────────
def ring_centroid_and_normal(mol, ring_atom_indices):
    conf = mol.GetConformer()
    pts = np.array([[conf.GetAtomPosition(i).x,
                     conf.GetAtomPosition(i).y,
                     conf.GetAtomPosition(i).z] for i in ring_atom_indices])
    c = pts.mean(axis=0)
    centered = pts - c
    _, _, Vt = np.linalg.svd(centered)
    return c, Vt[-1]

with open(f'{WD}/crystal_lvy.pdb') as f:
    lvy_pdb_txt = f.read()

lvy_mol = Chem.MolFromPDBBlock(lvy_pdb_txt, removeHs=False)
if lvy_mol is None:
    print("ERROR: couldn't parse crystal LVY")
else:
    conf = lvy_mol.GetConformer()
    lig_hb_c = []
    for atom in lvy_mol.GetAtoms():
        if atom.GetAtomicNum() in (7, 8):
            pos = conf.GetAtomPosition(atom.GetIdx())
            lig_hb_c.append((atom.GetSymbol(), pos.x, pos.y, pos.z))

    hbonds_c = []
    seen = set()
    lig_hb_arr_c = np.array([[x,y,z] for _,x,y,z in lig_hb_c])
    for li, (le, lx, ly, lz) in enumerate(lig_hb_c):
        dists = np.linalg.norm(prot_hb_arr - np.array([lx, ly, lz]), axis=1)
        for pi in np.where(dists <= 3.5)[0]:
            resi, resn, aname, pelem, px, py, pz = prot_hb[pi]
            key = (resi, aname)
            if key in seen: continue
            seen.add(key)
            hbonds_c.append({
                'start': [round(lx,3), round(ly,3), round(lz,3)],
                'end':   [round(px,3), round(py,3), round(pz,3)],
                'label': f'{resn} {resi} ({aname})',
                'type':  'hbond'
            })

    ri_c = lvy_mol.GetRingInfo()
    lig_arom_rings_c = [list(r) for r in ri_c.AtomRings()
                        if len(r) >= 5 and all(lvy_mol.GetAtomWithIdx(i).GetIsAromatic() for i in list(r))]
    pistack_c = []
    for ring_idx in lig_arom_rings_c:
        lc, ln = ring_centroid_and_normal(lvy_mol, ring_idx)
        for trp_r, (tc, tn) in trp_centroids.items():
            d = np.linalg.norm(lc - tc)
            if d > 5.5: continue
            cos_ang = abs(np.dot(ln, tn))
            angle_deg = np.degrees(np.arccos(np.clip(cos_ang, 0, 1)))
            stack_type = 'face-face' if angle_deg < 40 else ('T-shape' if angle_deg > 65 else 'offset')
            pistack_c.append({
                'start': [round(float(lc[0]),3), round(float(lc[1]),3), round(float(lc[2]),3)],
                'end':   [round(float(tc[0]),3), round(float(tc[1]),3), round(float(tc[2]),3)],
                'label': f'π-stack TRP {trp_r} ({stack_type}, d={d:.1f}Å)',
                'type':  'pistack'
            })

    interactions['crystal_lvy'] = {'hbonds': hbonds_c, 'pistack': pistack_c}
    print(f"crystal_lvy: {len(hbonds_c)} H-bonds, {len(pistack_c)} π-stacks")
    for hb in hbonds_c:
        print(f"  HB: {hb['label']}")
    for ps in pistack_c:
        print(f"  PI: {ps['label']}")
