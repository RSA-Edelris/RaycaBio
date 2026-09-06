#!/usr/bin/env python3
"""
Build a single PDB containing:
  - CDK2-CyclinE1 receptor (chains A + B)
  - Crystal reference ligand CTX-1017233 (chain X, residue LIG 900)
  - All 10 NC-001..NC-010 best docked poses (chain X, residues LG1..LGA, 901..910)

Output: cdk2_campaign/CDK2_CyclinE1_NC_complex.pdb

Uses MDAnalysis to merge structures and assign chain/residue IDs.
If MDAnalysis is unavailable, falls back to raw PDB text concatenation.
"""
import sys
sys.path.insert(0, "/home/ubuntu/rayca-modulon/src")

from pathlib import Path
import tempfile, gzip

WDIR   = Path("/home/ubuntu/rayca-sessions/31fad337-0958-45c1-a0cd-572f9cf727b6-0505c6de016f/cdk2_campaign")
REC    = WDIR / "receptor_raw.pdb"
XTAL   = WDIR / "ctx_reference_ligand.sdf"   # crystal ligand SDF (with 3D coords)
POSES  = WDIR / "poses_all"
OUT    = WDIR / "CDK2_CyclinE1_NC_complex.pdb"

NC_NAMES = [f"NC-{i:03d}" for i in range(1, 11)]

# ── Helper: convert SDF molecule to minimal PDB HETATM block ────────────────
def sdf_to_pdb_block(sdf_path, chain_id, res_name, res_seq):
    """Read first molecule from SDF, return PDB HETATM lines as string."""
    from rdkit import Chem
    suppl = Chem.SDMolSupplier(str(sdf_path), removeHs=True, sanitize=False)
    mol = next((m for m in suppl if m is not None), None)
    if mol is None:
        return ""
    conf = mol.GetConformer()
    lines = []
    for i, atom in enumerate(mol.GetAtoms()):
        sym = atom.GetSymbol()
        pos = conf.GetAtomPosition(i)
        serial = i + 1
        lines.append(
            f"HETATM{serial:5d}  {sym:<3s} {res_name:3s} {chain_id}{res_seq:4d}    "
            f"{pos.x:8.3f}{pos.y:8.3f}{pos.z:8.3f}  1.00  0.00          {sym:>2s}\n"
        )
    lines.append(f"TER   {serial+1:5d}      {res_name:3s} {chain_id}{res_seq:4d}\n")
    return "".join(lines)

# ── Build combined PDB ───────────────────────────────────────────────────────
sections = []

# 1. Receptor
print(f"Reading receptor: {REC.name}")
rec_lines = REC.read_text().splitlines(keepends=True)
# Keep ATOM/HETATM/TER/MODEL records, skip END
sections.append("REMARK  CDK2-CyclinE1 receptor (chains A=CDK2, B=CyclinE1)\n")
for line in rec_lines:
    if line.startswith(("ATOM", "HETATM", "TER", "MODEL", "ENDMDL")):
        sections.append(line)
# Strip trailing TER/END
while sections and sections[-1].strip() in ("TER", "END", ""):
    sections.pop()
sections.append("TER\n")

# 2. Crystal reference ligand (chain X, resSeq 900, resName LIG)
print(f"Reading crystal ligand: {XTAL.name}")
xtal_block = sdf_to_pdb_block(XTAL, chain_id="X", res_name="LIG", res_seq=900)
if xtal_block:
    sections.append("REMARK  Crystal reference ligand CTX-1017233 (chain X, LIG 900)\n")
    sections.append(xtal_block)
    print(f"  Crystal ligand: {xtal_block.count('HETATM')} atoms")
else:
    print("  WARN: crystal ligand SDF unreadable")

# 3. NC compound poses (chain X, resSeq 901-910, resName LG1..LGA)
present = []
missing = []
for i, name in enumerate(NC_NAMES):
    sdf_path = POSES / f"{name}_best_pose.sdf"
    res_seq  = 901 + i
    res_name = f"L{i+1:02X}"[:3]   # L01..L0A
    if not sdf_path.exists():
        print(f"  WARN: {name} — best_pose.sdf missing, skipping")
        missing.append(name)
        continue
    block = sdf_to_pdb_block(sdf_path, chain_id="X", res_name=res_name, res_seq=res_seq)
    if not block:
        print(f"  WARN: {name} — SDF unreadable")
        missing.append(name)
        continue
    natoms = block.count("HETATM")
    sections.append(f"REMARK  {name} docked pose (chain X, {res_name} {res_seq})\n")
    sections.append(block)
    present.append(name)
    print(f"  {name}: {natoms} atoms → chain X resSeq {res_seq} resName {res_name}")

# 4. END
sections.append("END\n")

OUT.write_text("".join(sections))
size_kb = OUT.stat().st_size / 1024
print(f"\nWritten: {OUT.name}  ({size_kb:.1f} KB)")
print(f"Ligands included: {len(present)}/10  {present}")
if missing:
    print(f"Ligands missing:  {missing}")
