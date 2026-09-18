
# Scan 5EU1 that is already in memory (pdb_text is intact)
chains = set()
ligands = {}
for line in pdb_text.splitlines():
    if line.startswith("ATOM") or line.startswith("HETATM"):
        chain   = line[21]
        resname = line[17:20].strip()
        resseq  = line[22:26].strip()
        chains.add(chain)
        if line.startswith("HETATM") and resname not in (
            "HOH","EDO","PEG","GOL","MES","SO4","PO4","CL","NA","EPE","BME"):
            key = (resname, chain, resseq)
            ligands[key] = ligands.get(key, 0) + 1

print("5EU1 chains:", sorted(chains))
print("Non-solvent ligands (resname, chain, resseq, atom_count):")
for k, v in sorted(ligands.items()):
    print(f"  {k[0]:6s}  chain={k[1]}  seq={k[2]:4s}  atoms={v}")

# Also print REMARK/TITLE lines for context
for line in pdb_text.splitlines()[:30]:
    if line.startswith(("TITLE","REMARK  2 ","COMPND","SOURCE","EXPDTA")):
        print(line)
