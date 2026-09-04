
import json, gzip

# Write a docking helper function to file so it persists across cells
helper_code = '''
import json, gzip, io
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter

def dock_batch(dispatch_fn, pdb_content, smiles_list, cx, cy, cz, exhaustiveness=8, num_modes=3):
    """Dock a list of (name, smiles) pairs. Returns list of dicts with scores."""
    # Build SDF
    buf = io.StringIO()
    w = SDWriter(buf)
    valid = []
    for name, smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None: continue
        mol.SetProp("_Name", name)
        mol = Chem.AddHs(mol)
        params = AllChem.ETKDGv3(); params.randomSeed = 42
        if AllChem.EmbedMolecule(mol, params) != -1:
            AllChem.MMFFOptimizeMolecule(mol)
            w.write(mol)
            valid.append(name)
    w.close()
    sdf_content = buf.getvalue()

    result = dispatch_fn("gnina", {
        "proteinFile": "protein.pdb",
        "ligandFile": "batch.sdf",
        "boxX": cx, "boxY": cy, "boxZ": cz,
        "width": 25, "height": 25, "depth": 25,
        "exhaustiveness": exhaustiveness,
        "numModes": num_modes,
        "seed": 42
    }, files={"protein.pdb": pdb_content, "batch.sdf": sdf_content})

    # Parse output SDF
    out_file = result.get("output_file") or ""
    poses_out = []
    if out_file:
        try:
            data = gzip.decompress(out_file.encode("latin-1")).decode("utf-8") if out_file[:2] == "\\x1f\\x8b" else out_file
        except:
            data = out_file
    # Try from files written
    import os
    sdf_gz = "/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/gnina_docked.sdf.gz"
    if os.path.exists(sdf_gz):
        with gzip.open(sdf_gz, "rt") as f:
            data = f.read()
        suppl = Chem.SDMolSupplier()
        suppl.SetData(data, removeHs=False)
        for mol in suppl:
            if mol is None: continue
            name = mol.GetProp("_Name") if mol.HasProp("_Name") else "?"
            aff = float(mol.GetProp("minimizedAffinity")) if mol.HasProp("minimizedAffinity") else None
            cnn_aff = float(mol.GetProp("CNNaffinity")) if mol.HasProp("CNNaffinity") else None
            cnn_sc = float(mol.GetProp("CNNscore")) if mol.HasProp("CNNscore") else None
            poses_out.append({"name": name, "affinity": aff, "cnn_affinity": cnn_aff, "cnn_score": cnn_sc})
        # Keep only best pose per compound
        best = {}
        for p in poses_out:
            n = p["name"]
            if n not in best or (p["cnn_score"] or 0) > (best[n]["cnn_score"] or 0):
                best[n] = p
        return list(best.values())
    return []
'''

with open('/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/dock_helper.py', 'w') as f:
    f.write(helper_code)
print("Helper written")

# Load pdb content once
with open(pdb_clean_path) as f:
    pdb_clean_content = f.read()
print(f"PDB loaded: {len(pdb_clean_content)} bytes")
