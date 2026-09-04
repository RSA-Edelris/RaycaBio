
import zipfile, os

with zipfile.ZipFile("compound_A_biovia.zip", "w", zipfile.ZIP_DEFLATED) as z:
    # Per-step RXN files
    for fn in sorted(os.listdir("biovia_rxn")):
        z.write(f"biovia_rxn/{fn}", f"biovia_rxn/{fn}")
    # SDF (all structures)
    z.write("route_structures.sdf", "route_structures.sdf")
    # PNG schemes
    for fn in ["retrosynthesis_compound_A.png","route_A.png","route_B.png","route_C.png","panel_SM.png"]:
        if os.path.exists(fn):
            z.write(fn, f"png_schemes/{fn}")

print("ZIP contents:")
with zipfile.ZipFile("compound_A_biovia.zip") as z:
    for info in z.infolist():
        print(f"  {info.filename:50s}  {info.file_size:>8,} B")
