import parmed as pmd
import sys

amber_sys = pmd.load_file("/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/md_EDS01806218_ent2/complex.prmtop", "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/md_EDS01806218_ent2/complex.inpcrd")
n = len(amber_sys.atoms)
r = len(amber_sys.residues)
b = amber_sys.box
print(f"atoms={n} residues={r} box={b[0]:.2f}x{b[1]:.2f}x{b[2]:.2f}")

amber_sys.save("/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/md_EDS01806218_ent2/complex.top", overwrite=True)
amber_sys.save("/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85/md_EDS01806218_ent2/complex.gro", overwrite=True)
print("DONE")
