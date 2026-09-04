
import json, gzip, io
from rdkit.Chem import SDWriter

def make_sdf(smiles_list):
    buf = io.StringIO()
    w = SDWriter(buf)
    for name, smi in smiles_list:
        mol = Chem.MolFromSmiles(smi)
        if mol is None: continue
        mol.SetProp("_Name", name)
        mol = Chem.AddHs(mol)
        params = AllChem.ETKDGv3(); params.randomSeed = 42
        if AllChem.EmbedMolecule(mol, params) != -1:
            AllChem.MMFFOptimizeMolecule(mol)
            w.write(mol)
    w.close()
    return buf.getvalue()

def run_gnina_batch(batch, label):
    sdf_content = make_sdf(batch)
    res = dispatch('gnina', {
        'proteinFile': 'protein.pdb', 'ligandFile': 'batch.sdf',
        'boxX': cx, 'boxY': cy, 'boxZ': cz,
        'width': 25, 'height': 25, 'depth': 25,
        'exhaustiveness': 8, 'numModes': 3, 'seed': 42
    }, files={'protein.pdb': pdb_clean_content, 'batch.sdf': sdf_content})
    
    sdf_gz = '/home/ubuntu/rayca-sessions/c29e716e-6774-4a9b-8ead-aba645849be4-01def6985d02/gnina_docked.sdf.gz'
    import os
    if not os.path.exists(sdf_gz):
        print(f"  {label}: no output SDF")
        return []
    with gzip.open(sdf_gz, 'rt') as f:
        data = f.read()
    suppl = Chem.SDMolSupplier(); suppl.SetData(data, removeHs=False)
    best = {}
    for mol in suppl:
        if mol is None: continue
        name = mol.GetProp("_Name") if mol.HasProp("_Name") else "?"
        aff = float(mol.GetProp("minimizedAffinity")) if mol.HasProp("minimizedAffinity") else None
        cnn = float(mol.GetProp("CNNaffinity")) if mol.HasProp("CNNaffinity") else None
        sc = float(mol.GetProp("CNNscore")) if mol.HasProp("CNNscore") else None
        if name not in best or (sc or 0) > (best[name]['cnn_score'] or 0):
            best[name] = {'name': name, 'affinity': aff, 'cnn_affinity': cnn, 'cnn_score': sc}
    results = list(best.values())
    for r in results:
        print(f"  {r['name']}: aff={r['affinity']:.3f}, CNN_aff={r['cnn_affinity']:.3f}, score={r['cnn_score']:.3f}")
    return results

# Batch 1: known actives 1-5
batch1 = [(n, s) for n,s,r in known_actives[:5]]
print("=== Batch 1 (known actives 1-5) ===")
results_b1 = run_gnina_batch(batch1, "B1")
