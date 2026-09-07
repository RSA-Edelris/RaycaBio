
import subprocess, os

session = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"

# Check atom counts in prmtop files for ent1 vs ent2
for comp in ["EDS01357518_ent1", "EDS01806218_ent2"]:
    md_dir = f"{session}/md_{comp}"
    for prmtop in ["complex_nowater.prmtop", "ligand.prmtop", "receptor.prmtop"]:
        path = f"{md_dir}/{prmtop}"
        if not os.path.exists(path):
            print(f"  MISSING: {comp}/{prmtop}")
            continue
        # NATOM is on the line after %FLAG POINTERS
        r = subprocess.run(["grep", "-A2", "FLAG POINTERS", path], capture_output=True, text=True)
        natom_line = r.stdout.split("\n")
        # NATOM is the first number on the FORMAT line after POINTERS
        for i, ln in enumerate(natom_line):
            if "FORMAT" in ln and i+1 < len(natom_line):
                vals = natom_line[i+1].split()
                if vals:
                    print(f"  {comp}/{prmtop}: NATOM={vals[0]}")
                break
