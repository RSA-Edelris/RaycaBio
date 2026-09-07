
import sys, parmed as pmd
name, base = sys.argv[1], sys.argv[2]
sv_dir  = f"{base}/md_{name}/abfe_solv"
prmtop  = f"{sv_dir}/lig_solv.prmtop"
inpcrd  = f"{sv_dir}/lig_solv.inpcrd"
struct = pmd.load_file(prmtop, inpcrd)
struct.save(f"{sv_dir}/lig_solv.top", overwrite=True)
struct.save(f"{sv_dir}/lig_solv.gro", overwrite=True)
print(f"OK {len(struct.atoms)} atoms")
