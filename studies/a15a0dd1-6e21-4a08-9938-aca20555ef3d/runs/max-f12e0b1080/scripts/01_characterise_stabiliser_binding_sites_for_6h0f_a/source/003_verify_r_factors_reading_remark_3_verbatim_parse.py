
# ── Verify R-factors by reading REMARK 3 verbatim, and parse ligand B/occ ──

def get_remark3_rfactors(path):
    """Return raw REMARK 3 lines mentioning R VALUE."""
    out = []
    with open(path) as f:
        for line in f:
            if line.startswith("REMARK   3") and (
                "R VALUE" in line or "R-VALUE" in line or "RFREE" in line.upper()):
                out.append(line.rstrip())
    return out

def get_ligand_atoms(path, resnames):
    """Extract all HETATM records for named ligands."""
    atoms = []
    with open(path) as f:
        for line in f:
            if not line.startswith("HETATM"):
                continue
            rn = line[17:20].strip()
            if rn in resnames:
                atoms.append({
                    "name": line[12:16].strip(),
                    "resn": rn,
                    "chain": line[21],
                    "resi": line[22:26].strip(),
                    "x": float(line[30:38]),
                    "y": float(line[38:46]),
                    "z": float(line[46:54]),
                    "occ": float(line[54:60]),
                    "bfac": float(line[60:66]),
                    "alt": line[16].strip(),
                })
    return atoms

print("=== 6H0F REMARK 3 R-factors ===")
for l in get_remark3_rfactors(p6h0f):
    print(l)

print("\n=== 2O98 REMARK 3 R-factors ===")
for l in get_remark3_rfactors(p2o98):
    print(l)

print("\n=== 6H0F ligand Y70 atoms (pomalidomide) ===")
poma = get_ligand_atoms(p6h0f, {"Y70"})
if poma:
    occs = [a["occ"] for a in poma]
    bfacs = [a["bfac"] for a in poma]
    print(f"  Total atoms across all copies: {len(poma)}")
    # per chain
    from collections import defaultdict
    by_chain = defaultdict(list)
    for a in poma:
        by_chain[a["chain"]].append(a)
    for ch, ats in sorted(by_chain.items()):
        occs_c = [a["occ"] for a in ats]
        bfacs_c = [a["bfac"] for a in ats]
        print(f"  Chain {ch}: {len(ats)} atoms | occ {min(occs_c):.2f}–{max(occs_c):.2f} "
              f"| B {min(bfacs_c):.1f}–{max(bfacs_c):.1f} Å² (mean {sum(bfacs_c)/len(bfacs_c):.1f})")

print("\n=== 2O98 ligand FSC atoms (fusicoccin) ===")
fusc = get_ligand_atoms(p2o98, {"FSC"})
if fusc:
    by_chain = defaultdict(list)
    for a in fusc:
        by_chain[a["chain"]].append(a)
    for ch, ats in sorted(by_chain.items()):
        occs_c = [a["occ"] for a in ats]
        bfacs_c = [a["bfac"] for a in ats]
        print(f"  Chain {ch}: {len(ats)} atoms | occ {min(occs_c):.2f}–{max(occs_c):.2f} "
              f"| B {min(bfacs_c):.1f}–{max(bfacs_c):.1f} Å² (mean {sum(bfacs_c)/len(bfacs_c):.1f})")
