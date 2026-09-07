
import os
from rdkit import Chem

in_sdf  = "/home/ubuntu/rayca-artifacts/aa94c8cd626e84050ef1e8e8/files/CRBN_ID_enantio.sdf"
out_sdf = f"{WORK}/CRBN_ligands_prepared.sdf"

# ── read SDF as raw text, split on $$$$ ───────────────────────────────────────
with open(in_sdf) as fh:
    raw = fh.read()

blocks = [b.strip() for b in raw.split("$$$$") if b.strip()]
print(f"SDF blocks found: {len(blocks)}")
print(f"First block header:\n{blocks[0][:120]}")

# ── parse each block individually ─────────────────────────────────────────────
parsed, failed = [], []
for blk in blocks:
    try:
        mol = Chem.MolFromMolBlock(blk, removeHs=True, sanitize=True)
        if mol is None:
            failed.append(("None", "MolFromMolBlock returned None"))
            continue
        # extract name from first line
        name = blk.split("\n")[0].strip()
        # keep largest fragment (salt removal without SaltRemover)
        frags = Chem.GetMolFrags(mol, asMols=True, sanitizeFrags=True)
        mol   = max(frags, key=lambda m: m.GetNumHeavyAtoms()) if frags else mol
        mol.SetProp("_Name", name)
        parsed.append(mol)
    except Exception as e:
        failed.append(("?", str(e)[:80]))

print(f"Parsed: {len(parsed)}  Failed: {len(failed)}")
if failed:
    print("Failures:", failed[:5])
