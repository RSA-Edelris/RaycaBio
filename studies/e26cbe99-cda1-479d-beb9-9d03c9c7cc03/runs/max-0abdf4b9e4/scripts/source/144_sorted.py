
import os, shutil, glob

BASE = "/home/ubuntu/rayca-sessions/e26cbe99-cda1-479d-beb9-9d03c9c7cc03-d43a861c8a85"
STAGE = f"{BASE}/abfe_stage"

# Copy all staged files from abfe_stage/ to the session root
copied = []
for src in sorted(glob.glob(f"{STAGE}/*")):
    fname = os.path.basename(src)
    dst = f"{BASE}/{fname}"
    shutil.copy2(src, dst)
    copied.append(fname)

print(f"Copied {len(copied)} files from abfe_stage/ to session root:")
for f in copied[:10]:
    print(f"  {f}")
print(f"  ... and {len(copied)-10} more")

# Also copy EDS01357518_ent2 MD files to root with prefixed names
ent2_files = {
    "EDS01357518_ent2_complex.gro":  f"{BASE}/md_EDS01357518_ent2/complex.gro",
    "EDS01357518_ent2_complex.top":  f"{BASE}/md_EDS01357518_ent2/complex.top",
    "EDS01357518_ent2_index.ndx":    f"{BASE}/md_EDS01357518_ent2/index.ndx",
    "EDS01357518_ent2_em.mdp":       f"{BASE}/md_EDS01357518_ent2/em.mdp",
    "EDS01357518_ent2_npt_eq.mdp":   f"{BASE}/md_EDS01357518_ent2/npt_eq.mdp",
    "EDS01357518_ent2_prod.mdp":     f"{BASE}/md_EDS01357518_ent2/prod.mdp",
}
for dst_name, src in ent2_files.items():
    shutil.copy2(src, f"{BASE}/{dst_name}")
    print(f"  {dst_name}")

print(f"\nAll files at session root. Ready to resubmit.")
