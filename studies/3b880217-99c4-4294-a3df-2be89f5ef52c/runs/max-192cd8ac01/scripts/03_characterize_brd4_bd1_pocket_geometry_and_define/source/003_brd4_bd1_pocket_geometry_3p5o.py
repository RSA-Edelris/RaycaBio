
# ── BRD4 BD1 pocket geometry (3P5O) ─────────────────────────────────────────
brd4_chain = brd4[0]["A"]
brd4_res   = {r.id[1]: r for r in brd4_chain if r.id[0]==' '}

# Key pocket-lining residues (BRD4 full-length numbering carried in 3P5O)
pocket_keys = {
    "Trp81":  (81,  "NE1"),   # WPF shelf, H-bond donor
    "Phe83":  (83,  "CZ"),    # WPF shelf
    "Val87":  (87,  "CB"),    # hydrophobic floor
    "Tyr97":  (97,  "OH"),    # ZA loop, gatekeeper
    "Cys136": (136, "SG"),    # near Asn
    "Asn140": (140, "ND2"),   # critical H-bond to acetyl-C=O
    "Pro82":  (82,  "CD"),    # caps one side
}

print("BRD4 BD1 pocket-lining residues (3P5O numbering):")
pocket_coords = {}
for name, (rnum, atom) in pocket_keys.items():
    if rnum in brd4_res:
        r = brd4_res[rnum]
        if atom in r:
            coord = r[atom].coord
            pocket_coords[name] = coord
            print(f"  {name:8s} r{rnum} {atom:4s}  {coord.round(2)}")
        else:
            avail = [a.name for a in r.get_atoms()]
            print(f"  {name:8s} r{rnum} – atom {atom} not found; available: {avail}")
    else:
        print(f"  {name:8s} r{rnum} – residue not found in 3P5O chain A")

# EAM ligand (occupies the Kac pocket)
eam = next((r for r in brd4_chain if r.resname=="EAM"), None)
eam_com = np.mean([a.coord for a in eam.get_atoms()], axis=0) if eam else None
print(f"\nEAM (pocket inhibitor) CoM: {eam_com.round(2) if eam_com is not None else 'not found'}")

# ── Pocket geometry ──────────────────────────────────────────────────────────
# Asn140 ND2 is the deepest anchor; define pocket axis as Asn140→entrance
# Use Tyr97 OH as the approximate entrance marker (sits at the pocket mouth)
asn140 = pocket_coords.get("Asn140")
tyr97  = pocket_coords.get("Tyr97")
trp81  = pocket_coords.get("Trp81")

if asn140 is not None and eam_com is not None:
    # Pocket depth: distance from Asn140 ND2 to EAM CoM (proxy for entrance depth)
    depth = np.linalg.norm(eam_com - asn140)
    print(f"\nAsn140 ND2 to EAM CoM (≈ insertion depth):  {depth:.1f} Å")

    # Pocket axis direction: from Asn140 toward EAM CoM (= toward entrance)
    pocket_axis = eam_com - asn140
    pocket_axis_norm = pocket_axis / np.linalg.norm(pocket_axis)
    print(f"Pocket axis (Asn140→entrance): {pocket_axis_norm.round(3)}")

if tyr97 is not None and trp81 is not None:
    # Entrance width: Tyr97 OH to Trp81 NE1 (span of the rim)
    width = np.linalg.norm(tyr97 - trp81)
    print(f"Pocket entrance span (Tyr97–Trp81):          {width:.1f} Å")

# Distance Asn140 ND2 to EAM atom closest to Asn – represents Kac acetyl reach
if eam is not None and asn140 is not None:
    min_d = min(np.linalg.norm(a.coord - asn140) for a in eam.get_atoms())
    print(f"Closest EAM atom to Asn140 ND2:              {min_d:.1f} Å")

# Save key coords for later
import pickle
geom = dict(
    u52_com      = u52_com,
    eam_com      = eam_com,
    asn140       = asn140,
    tyr97        = tyr97,
    trp81        = trp81,
    pocket_axis  = pocket_axis_norm if asn140 is not None and eam_com is not None else None,
    surface_lys  = surface_lys,
    surface_serthr = surface_serthr,
)
with open("geom.pkl","wb") as f:
    pickle.dump(geom, f)
print("\nGeometry saved to geom.pkl")
