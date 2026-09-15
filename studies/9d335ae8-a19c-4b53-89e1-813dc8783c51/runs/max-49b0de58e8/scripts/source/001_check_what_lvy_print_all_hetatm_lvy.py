
# Check what LVY is - print all HETATM for LVY
with open("/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb") as f:
    hetatm = [l for l in f if l.startswith("HETATM") and "LVY" in l]
print(f"LVY atom count: {len(hetatm)}")
print("First few atoms:")
for l in hetatm[:5]:
    print(l.strip())

# Also check ZN location
with open("/home/ubuntu/rayca-artifacts/c2db8d53fb710fe21c5fee43/files/CRBN.pdb") as f:
    zn = [l for l in f if l.startswith("HETATM") and " ZN " in l]
print("\nZn line:", zn[0].strip() if zn else "none")
