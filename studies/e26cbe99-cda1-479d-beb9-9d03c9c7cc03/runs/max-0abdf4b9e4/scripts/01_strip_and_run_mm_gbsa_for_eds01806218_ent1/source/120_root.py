
import subprocess

SESSION = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Atom counts from all GRO files in the session root (the cluster outputs)
import glob, os
gros = sorted(glob.glob(f"{SESSION}/em.*.gro") + glob.glob(f"{SESSION}/npt_prod.*.gro") + glob.glob(f"{SESSION}/npt_prod_*.gro"))
print("=== Atom counts in session-root GRO files ===")
for g in gros:
    with open(g) as f:
        lines = f.readlines()
    print(f"  {os.path.basename(g)}: {lines[1].strip()} atoms")

# Also check the atom counts in all md_*/complex.gro
print("\n=== Atom counts in md_*/complex.gro ===")
for d in sorted(glob.glob(f"{SESSION}/md_*/complex.gro")):
    with open(d) as f:
        lines = f.readlines()
    name = os.path.basename(os.path.dirname(d))
    print(f"  {name}: {lines[1].strip()} atoms")
