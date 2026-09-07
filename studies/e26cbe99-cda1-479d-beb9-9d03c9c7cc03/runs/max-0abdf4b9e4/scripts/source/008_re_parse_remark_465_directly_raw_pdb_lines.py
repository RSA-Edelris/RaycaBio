
# Re-parse REMARK 465 directly from raw PDB lines
missing_res = []
in_missing = False
for line in lines:
    if 'REMARK 465' not in line[:12]:
        continue
    rest = line[11:].strip()
    # data lines look like: "    MET A   -17  " after the header block
    parts = rest.split()
    # skip header lines (no 3-letter residue code in expected position)
    if len(parts) >= 3 and len(parts[0]) == 3 and parts[0].isalpha() and len(parts[1]) == 1:
        try:
            seq = int(parts[2])
            missing_res.append((parts[1], seq, parts[0]))  # (chain, seqnum, resname)
        except ValueError:
            pass
    # also handle lines with model number prefix
    elif len(parts) >= 4 and len(parts[1]) == 3 and parts[1].isalpha() and len(parts[2]) == 1:
        try:
            seq = int(parts[3])
            missing_res.append((parts[2], seq, parts[1]))
        except ValueError:
            pass

print(f"Parsed {len(missing_res)} missing residues")
chains_m = {}
for ch, seq, res in missing_res:
    chains_m.setdefault(ch, []).append(seq)

for ch, seqs in chains_m.items():
    seqs_sorted = sorted(seqs)
    bio = [s for s in seqs_sorted if s > 0]
    tag = [s for s in seqs_sorted if s <= 0]
    print(f"  Chain {ch}: {len(seqs_sorted)} missing  "
          f"tag/linker(≤0): {len(tag)}  biological(>0): {len(bio)}")
    if bio:
        print(f"    Biological gaps: {bio[:40]}")
