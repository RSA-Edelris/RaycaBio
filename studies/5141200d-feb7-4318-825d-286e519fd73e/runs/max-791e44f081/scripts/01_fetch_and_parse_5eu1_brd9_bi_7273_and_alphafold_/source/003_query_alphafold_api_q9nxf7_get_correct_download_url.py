
import urllib.request, json

# Query AlphaFold API for Q9NXF7 to get the correct download URL
af_api = "https://alphafold.ebi.ac.uk/api/prediction/Q9NXF7"
with urllib.request.urlopen(af_api) as r:
    af_meta = json.loads(r.read().decode())

print("AlphaFold API response keys:", list(af_meta[0].keys()) if isinstance(af_meta, list) else list(af_meta.keys()))
if isinstance(af_meta, list):
    entry = af_meta[0]
else:
    entry = af_meta

for k in ("uniprotAccession","uniprotId","gene","entryId","pdbUrl","cifUrl","paeDocUrl"):
    print(f"  {k}: {entry.get(k,'—')}")
