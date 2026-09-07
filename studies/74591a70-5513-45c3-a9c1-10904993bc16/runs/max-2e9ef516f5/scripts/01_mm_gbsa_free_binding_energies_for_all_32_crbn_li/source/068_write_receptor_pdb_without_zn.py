
import subprocess
from pathlib import Path

# Write receptor PDB without ZN
rec_noh  = f"{WORK}/4CI2_receptor_noh.pdb"
rec_nozn = f"{MMDIR}/receptor_nozn.pdb"

kept, dropped = [], []
with open(rec_noh) as f:
    for line in f:
        if line.startswith(("ATOM","HETATM")):
            resname = line[17:20].strip()
            if resname in ("ZN","ZN2"):
                dropped.append(line.rstrip())
            else:
                kept.append(line)
        else:
            kept.append(line)

with open(rec_nozn, "w") as f:
    f.writelines(kept)

print(f"Wrote {rec_nozn} ({Path(rec_nozn).stat().st_size} B)")
print(f"Dropped {len(dropped)} ZN line(s):", dropped)

# Re-run tleap with ZN-free receptor
# Also delete stale rec.prmtop (was zero-byte from previous attempt)
for stale in [f"{lig_dir}/rec.prmtop", f"{lig_dir}/complex.prmtop",
              f"{lig_dir}/rec.inpcrd", f"{lig_dir}/complex.inpcrd"]:
    Path(stale).unlink(missing_ok=True)

tleap_in = f"""\
source leaprc.protein.ff14SB
source leaprc.gaff2
LIG = loadmol2 {lig_dir}/lig.mol2
loadamberparams {lig_dir}/lig.frcmod
REC = loadpdb {rec_nozn}
COMPLEX = combine {{REC LIG}}
check COMPLEX
saveamberparm LIG {lig_dir}/lig.prmtop {lig_dir}/lig.inpcrd
saveamberparm REC {lig_dir}/rec.prmtop {lig_dir}/rec.inpcrd
saveamberparm COMPLEX {lig_dir}/complex.prmtop {lig_dir}/complex.inpcrd
quit
"""
Path(f"{lig_dir}/tleap.in").write_text(tleap_in)

r = subprocess.run(
    [f"{AMBER}/tleap", "-f", f"{lig_dir}/tleap.in"],
    cwd=lig_dir, capture_output=True, text=True, timeout=120
)
print("tleap rc:", r.returncode)
lines = (r.stdout + r.stderr).split("\n")
# Show errors/fatals and last 20 lines
for l in lines:
    if any(k in l.upper() for k in ("FATAL","ERROR","WARN","MISSING")):
        print("  >>", l)
print("--- last 15 lines ---")
print("\n".join(lines[-15:]))

for fname in ["complex.prmtop","rec.prmtop","lig.prmtop"]:
    p = Path(f"{lig_dir}/{fname}")
    print(f"{fname}: {'OK ' + str(p.stat().st_size) + 'B' if p.exists() and p.stat().st_size > 0 else 'MISSING/EMPTY'}")
