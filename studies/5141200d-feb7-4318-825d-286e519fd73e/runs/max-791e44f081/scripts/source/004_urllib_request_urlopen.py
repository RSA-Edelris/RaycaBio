
import urllib.request

pdb_url = entry["pdbUrl"]   # https://alphafold.ebi.ac.uk/files/AF-Q9NXF7-F1-model_v6.pdb
with urllib.request.urlopen(pdb_url) as r:
    af_text = r.read().decode()

with open("/tmp/DCAF16_AF.pdb", "w") as f:
    f.write(af_text)

# Also grab the PAE JSON for confidence assessment
pae_url = entry["paeDocUrl"]
with urllib.request.urlopen(pae_url) as r:
    pae_raw = r.read().decode()
with open("/tmp/DCAF16_pae.json", "w") as f:
    f.write(pae_raw)

print(f"DCAF16 AF v6 downloaded: {len(af_text.splitlines())} lines")

# Quick stats
seq = entry.get("sequence","")
print(f"Sequence length: {len(seq)} aa")
print(f"pLDDT very high: {entry['fractionPlddtVeryHigh']:.2%}")
print(f"pLDDT confident: {entry['fractionPlddtConfident']:.2%}")
print(f"pLDDT low:       {entry['fractionPlddtLow']:.2%}")

# Find all cysteines in the AF model
cys_records = []
for line in af_text.splitlines():
    if line.startswith("ATOM") and line[17:20].strip() == "CYS" and line[12:16].strip() == "CA":
        resseq = int(line[22:26])
        x = float(line[30:38])
        y = float(line[38:46])
        z = float(line[46:54])
        bfac = float(line[60:66])   # pLDDT in AF models
        cys_records.append({"resseq": resseq, "x": x, "y": y, "z": z, "plddt": bfac})

print(f"\nTotal cysteines in DCAF16: {len(cys_records)}")
for c in cys_records:
    print(f"  CYS {c['resseq']:4d}  pLDDT={c['plddt']:.1f}")
