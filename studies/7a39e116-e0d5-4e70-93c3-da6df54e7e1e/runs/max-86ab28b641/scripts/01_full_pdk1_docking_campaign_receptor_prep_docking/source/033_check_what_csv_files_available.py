
import os, glob

# Check what CSV files are available
for fname in ["BindingEnergy.csv", "Energy.csv", "Dec.csv"]:
    path = f"{WS}/{fname}"
    if os.path.exists(path):
        with open(path) as f:
            print(f"=== {fname} ===")
            print(f.read()[:2000])
        print()

# Also check ART
for fname in ["BindingEnergy.csv", "Energy.csv"]:
    path = f"{ART}/{fname}"
    if os.path.exists(path):
        with open(path) as f:
            print(f"=== ART/{fname} ===")
            print(f.read()[:1000])
        print()
