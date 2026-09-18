
# ── BCL6-BTB (5MW2) surface-residue analysis ─────────────────────────────────
sr = ShrakeRupley()
sr.compute(bcl6, level="R")

bcl6_model  = bcl6[0]
bcl6_chain  = bcl6_model["A"]

# ligand U52 centre-of-mass (BCL6 anchor / BI-3802 binding site)
u52 = next(r for r in bcl6_chain if r.resname == "U52")
u52_com = np.mean([a.coord for a in u52.get_atoms()], axis=0)
print(f"BCL6 ligand (U52 / BI-3802) CoM: {u52_com.round(2)}")

# ── all protein residues sorted by residue number ─────────────────────────────
prot_res = sorted([r for r in bcl6_chain if r.id[0]==' '], key=lambda r: r.id[1])

print(f"\n{'Res':>8}  {'SASA(A2)':>9}  {'Key-atom':>8}  {'Dist-to-ligand':>14}")
print("-"*55)

surface_lys = []
surface_serthr = []

for res in prot_res:
    sasa = res.sasa
    rn   = res.resname

    if rn == "LYS" and "NZ" in res:
        nz = res["NZ"].coord
        d  = np.linalg.norm(nz - u52_com)
        if sasa > 30:                       # surface-exposed
            entry = dict(chain="A", resnum=res.id[1], resname="LYS",
                         sasa=sasa, atom="NZ", coord=nz, dist_to_lig=d)
            surface_lys.append(entry)
            print(f"LYS {res.id[1]:>4}  {sasa:9.1f}  NZ        {d:>14.1f}")

    elif rn in ("SER","THR") and sasa > 20:
        ak = "OG" if rn=="SER" else "OG1"
        if ak in res:
            og = res[ak].coord
            d  = np.linalg.norm(og - u52_com)
            entry = dict(chain="A", resnum=res.id[1], resname=rn,
                         sasa=sasa, atom=ak, coord=og, dist_to_lig=d)
            surface_serthr.append(entry)

print(f"\nSurface LYS (SASA>30 Å²): {len(surface_lys)}")
print(f"Surface SER/THR (SASA>20 Å²): {len(surface_serthr)}")
for e in sorted(surface_serthr, key=lambda x: x['dist_to_lig'])[:6]:
    print(f"  {e['resname']}{e['resnum']} SASA={e['sasa']:.1f}  dist={e['dist_to_lig']:.1f}")
