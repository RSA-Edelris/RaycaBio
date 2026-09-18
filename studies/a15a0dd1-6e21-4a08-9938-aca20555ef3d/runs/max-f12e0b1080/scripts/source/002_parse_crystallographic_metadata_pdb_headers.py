
# Parse crystallographic metadata from PDB headers
def parse_pdb_header(path):
    info = {
        "resolution": None, "space_group": None, "r_work": None, "r_free": None,
        "missing_residues": [], "alt_locs": set(), "chains": set(),
        "ligands": [], "waters": 0, "title": "", "method": ""
    }
    with open(path) as f:
        for line in f:
            rec = line[:6].strip()
            if rec == "REMARK":
                rnum = line[6:10].strip()
                body = line[10:].strip()
                if rnum == "2" and "RESOLUTION" in body:
                    for tok in body.split():
                        try:
                            v = float(tok)
                            if 0.5 < v < 10:
                                info["resolution"] = v
                        except ValueError:
                            pass
                elif rnum == "3":
                    if "R VALUE" in body and "WORK" in body and "FREE" not in body:
                        for tok in body.split():
                            try:
                                v = float(tok)
                                if 0 < v < 1:
                                    info["r_work"] = v; break
                            except ValueError:
                                pass
                    elif "FREE R VALUE" in body and "ERROR" not in body and ":" in body:
                        parts = body.split(":")
                        if len(parts) > 1:
                            for tok in parts[-1].split():
                                try:
                                    v = float(tok)
                                    if 0 < v < 1:
                                        info["r_free"] = v; break
                                except ValueError:
                                    pass
                    elif "SPACE GROUP" in body and ":" in body:
                        info["space_group"] = body.split(":",1)[1].strip()
                elif rnum == "465":
                    # Missing residues
                    parts = line[10:].split()
                    if len(parts) >= 4:
                        try:
                            int(parts[2])
                            info["missing_residues"].append({
                                "res": parts[1], "chain": parts[2] if len(parts[2])==1 else parts[3],
                                "seq": parts[3] if len(parts[2])==1 else parts[4]
                            })
                        except:
                            pass
            elif rec == "TITLE":
                info["title"] += line[10:].strip() + " "
            elif rec == "EXPDTA":
                info["method"] = line[10:].strip()
            elif rec == "CRYST1":
                sg_raw = line[55:66].strip()
                if sg_raw:
                    info["space_group"] = sg_raw
            elif rec == "ATOM" or rec == "HETATM":
                chain = line[21]
                info["chains"].add(chain)
                alt = line[16].strip()
                if alt and alt not in (' ', ''):
                    info["alt_locs"].add(f"{line[17:20].strip()}{line[22:26].strip()}{chain}{alt}")
                if rec == "HETATM":
                    resn = line[17:20].strip()
                    if resn == "HOH" or resn == "WAT":
                        info["waters"] += 1
                    elif resn not in ("SO4","GOL","EDO","PEG","CIT","ACT","DMS","MPD"):
                        resi = line[22:26].strip()
                        key = (resn, chain, resi)
                        if key not in info["ligands"]:
                            info["ligands"].append(key)
    return info

h6 = parse_pdb_header(p6h0f)
h2 = parse_pdb_header(p2o98)

for label, h in [("6H0F", h6), ("2O98", h2)]:
    print(f"\n{'='*60}")
    print(f"PDB: {label}")
    print(f"  Title:       {h['title'][:90]}")
    print(f"  Method:      {h['method']}")
    print(f"  Resolution:  {h['resolution']} Å")
    print(f"  Space group: {h['space_group']}")
    print(f"  R-work:      {h['r_work']}")
    print(f"  R-free:      {h['r_free']}")
    print(f"  Chains:      {sorted(h['chains'])}")
    print(f"  Ligands:     {h['ligands']}")
    print(f"  Waters:      {h['waters']}")
    print(f"  Missing res: {len(h['missing_residues'])} recorded")
    if h['missing_residues']:
        print(f"    First 10:  {h['missing_residues'][:10]}")
    print(f"  Alt locs:    {len(h['alt_locs'])} sites")
    if h['alt_locs']:
        print(f"    Examples:  {list(h['alt_locs'])[:8]}")
