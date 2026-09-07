
compounds = ['EDS01357518_ent1','EDS01357518_ent2','EDS01806218_ent1','EDS01806218_ent2','EDS01889984']

def ring_centroid_and_normal(mol, ring_atom_indices):
    conf = mol.GetConformer()
    pts = np.array([[conf.GetAtomPosition(i).x,
                     conf.GetAtomPosition(i).y,
                     conf.GetAtomPosition(i).z] for i in ring_atom_indices])
    c = pts.mean(axis=0)
    centered = pts - c
    _, _, Vt = np.linalg.svd(centered)
    return c, Vt[-1]  # centroid, normal

interactions = {}

for cid in compounds:
    with open(f'{WD}/poses_{cid}.sdf') as f:
        content = f.read()
    blocks = [b.strip() for b in content.split('$$$$') if b.strip()]
    mol = Chem.MolFromMolBlock(blocks[0], removeHs=False)
    if mol is None:
        interactions[cid] = {'hbonds': [], 'pistack': []}
        continue
    conf = mol.GetConformer()

    # ── H-bond donors & acceptors in ligand ────────────────────────────────
    lig_hb = []   # (elem, x, y, z)
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() in (7, 8):   # N or O
            pos = conf.GetAtomPosition(atom.GetIdx())
            lig_hb.append((atom.GetSymbol(), pos.x, pos.y, pos.z))
    lig_hb_arr = np.array([[x,y,z] for _,x,y,z in lig_hb])

    # distance matrix lig H-bond atoms vs prot H-bond atoms
    hbonds = []
    seen = set()
    for li, (le, lx, ly, lz) in enumerate(lig_hb):
        dists = np.linalg.norm(prot_hb_arr - np.array([lx, ly, lz]), axis=1)
        for pi in np.where(dists <= 3.5)[0]:
            resi, resn, aname, pelem, px, py, pz = prot_hb[pi]
            key = (resi, aname)
            if key in seen: continue
            seen.add(key)
            hbonds.append({
                'start': [round(lx,3), round(ly,3), round(lz,3)],
                'end':   [round(px,3), round(py,3), round(pz,3)],
                'label': f'{resn} {resi} ({aname})',
                'type':  'hbond'
            })

    # ── π-stacking with TRP residues ───────────────────────────────────────
    ri = mol.GetRingInfo()
    lig_rings = [list(r) for r in ri.AtomRings() if len(r) >= 5]
    # filter aromatic rings only
    lig_arom_rings = [r for r in lig_rings
                      if all(mol.GetAtomWithIdx(i).GetIsAromatic() for i in r)]

    pistack = []
    for ring_idx in lig_arom_rings:
        lc, ln = ring_centroid_and_normal(mol, ring_idx)
        for trp_r, (tc, tn) in trp_centroids.items():
            d = np.linalg.norm(lc - tc)
            if d > 5.5: continue
            # angle between normals
            cos_ang = abs(np.dot(ln, tn))
            angle_deg = np.degrees(np.arccos(np.clip(cos_ang, 0, 1)))
            stack_type = 'face-face' if angle_deg < 40 else ('T-shape' if angle_deg > 65 else 'offset')
            pistack.append({
                'start': [round(float(lc[0]),3), round(float(lc[1]),3), round(float(lc[2]),3)],
                'end':   [round(float(tc[0]),3), round(float(tc[1]),3), round(float(tc[2]),3)],
                'label': f'π-stack TRP {trp_r} ({stack_type}, d={d:.1f}Å)',
                'type':  'pistack'
            })

    interactions[cid] = {'hbonds': hbonds, 'pistack': pistack}
    print(f"{cid}: {len(hbonds)} H-bonds, {len(pistack)} π-stacks")
    for hb in hbonds:
        print(f"  HB: {hb['label']}")
    for ps in pistack:
        print(f"  PI: {ps['label']}")
