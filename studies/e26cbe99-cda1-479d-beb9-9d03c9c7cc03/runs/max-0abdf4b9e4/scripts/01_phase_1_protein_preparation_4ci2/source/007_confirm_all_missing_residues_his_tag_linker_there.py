
# Confirm: are ALL missing residues the His-tag/linker, or are there biological loop gaps too?
missing_by_chain = {}
for line in missing_res_lines[2:]:   # skip header lines
    parts = line.split()
    if len(parts) >= 4:
        res_name = parts[1] if len(parts[1]) == 3 else None
        chain    = parts[2] if res_name else None
        try:
            seq_num = int(parts[3]) if res_name else None
        except:
            seq_num = None
        if res_name and chain and seq_num is not None:
            missing_by_chain.setdefault(chain, []).append((seq_num, res_name))

for ch, lst in missing_by_chain.items():
    lst.sort()
    pos = [x[0] for x in lst]
    print(f"Chain {ch}: {len(lst)} missing residues  "
          f"range [{pos[0]}..{pos[-1]}]")
    # flag any positive-numbered (real biological) residues
    bio = [(n,r) for n,r in lst if n > 0]
    if bio:
        print(f"  Biological gaps: {bio[:30]}")
    else:
        print(f"  All are tag/linker (≤ 0) — no biological loop gaps")
