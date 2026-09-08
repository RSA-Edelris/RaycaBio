
import os, glob

# Check if pdbfixer-prepared receptor landed in the artifact dir
art_dir = "/home/ubuntu/rayca-artifacts/cacaa3ede77705c5b065320a/files"
print("Artifact dir contents (recent):")
files = sorted(glob.glob(f"{art_dir}/**/*", recursive=True), key=os.path.getmtime)
for f in files[-15:]:
    print(f"  {f}  ({os.path.getsize(f)} bytes)")

# Also check what the dispatch tool exposes
print("\nSession workspace:", WS)
ws_files = sorted(glob.glob(f"{WS}/**/*", recursive=False))
print("Session workspace files (molecules/pdb):")
for f in ws_files:
    if any(f.endswith(ext) for ext in ['.pdb','.sdf','.mol2']):
        print(f"  {os.path.basename(f)}  ({os.path.getsize(f)} b)")
