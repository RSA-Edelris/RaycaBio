
SESSION = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Check GROMACS complex.gro atom count for EDS01357518_ent2
with open(f"{SESSION}/md_EDS01357518_ent2/complex.gro") as f:
    lines = f.readlines()
print("complex.gro atom count line:", lines[1].strip())

# Check run_parmed.py
with open(f"{SESSION}/md_EDS01357518_ent2/run_parmed.py") as f:
    print("\n--- run_parmed.py ---")
    print(f.read())
