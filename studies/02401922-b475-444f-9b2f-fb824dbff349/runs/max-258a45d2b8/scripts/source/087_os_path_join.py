
import os, re

wd = "/home/ubuntu/rayca-sessions/02401922-b475-444f-9b2f-fb824dbff349-fec3a540149a"
results_dir = os.path.join(wd, "docking_results")
ligands_dir = os.path.join(wd, "ligands_3d")

def sdf_num(f):
    m = re.search(r'lig(\d+)', f)
    return int(m.group(1)) if m else 0

# What's done
done_outs = sorted([f for f in os.listdir(results_dir) if f.endswith('_out.pdbqt')], key=sdf_num)
done_nums = {sdf_num(f) for f in done_outs}
print(f"Done: {len(done_outs)} compounds: {sorted(done_nums)}")

# What's missing
all_nums = set(range(1, 85))
missing_nums = sorted(all_nums - done_nums)
print(f"Missing: {len(missing_nums)}: {missing_nums}")

# Quick score sample from done files
def parse_scores(pdbqt_path):
    scores = []
    with open(pdbqt_path) as f:
        for line in f:
            m = re.match(r'REMARK VINA RESULT:\s+([-\d.]+)', line)
            if m:
                scores.append(float(m.group(1)))
    return scores

print("\nSample scores (first 5 done):")
for f in done_outs[:5]:
    scores = parse_scores(os.path.join(results_dir, f))
    name_f = f.replace('_out.pdbqt', '.pdbqt')
    # get compound name
    pdbqt = os.path.join(ligands_dir, name_f)
    cname = open(pdbqt).readline().split('=')[-1].strip() if os.path.exists(pdbqt) else '?'
    print(f"  {f:25s}  {cname:30s}  scores={scores}")
