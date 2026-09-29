
import pathlib, os, glob

session_root = pathlib.Path("/home/ubuntu/rayca-sessions/318e1560-3d55-4b84-bafd-39c623c8d42c-c53814dd4ebb")
print("Session root contents:")
for p in sorted(session_root.iterdir()):
    print(f"  {p.name}  ({p.stat().st_size if p.is_file() else 'dir'})")

# Look for transcript / journal files
print("\nJSONL / transcript files:")
for p in session_root.rglob("*.jsonl"):
    print(f"  {p.relative_to(session_root)}  {p.stat().st_size:,} bytes")
