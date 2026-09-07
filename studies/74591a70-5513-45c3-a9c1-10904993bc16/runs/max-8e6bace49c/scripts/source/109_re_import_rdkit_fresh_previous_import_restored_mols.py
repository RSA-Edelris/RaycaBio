
import json, subprocess, tempfile
from pathlib import Path

# Re-import rdkit fresh (previous import is restored but mols/compounds may linger)
from rdkit import Chem
from rdkit.Chem import AllChem, SDMolSupplier, SDWriter
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers, StereoEnumerationOptions
)

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
V2000_SDF = str(BASE / "CRBN_lig_results_2_v2000.sdf")
OUT_SDF   = str(BASE / "CRBN_ID_enantio_2.sdf")

def embed3d(mol, n_conf=50):
    mh = Chem.AddHs(mol)
    p = AllChem.ETKDGv3(); p.randomSeed = 42; p.numThreads = 0
    cids = AllChem.EmbedMultipleConfs(mh, numConfs=n_conf, params=p)
    if not cids:
        p2 = AllChem.ETKDG(); p2.randomSeed = 42
        cids = AllChem.EmbedMultipleConfs(mh, numConfs=1, params=p2)
    if not cids:
        return None, None
    res = AllChem.MMFFOptimizeMoleculeConfs(mh, mmffVariant='MMFF94s', numThreads=0, maxIters=2000)
    if not res:
        return mh, 9999.0
    best_e, best_cid = min((e, cid) for cid, (conv, e) in enumerate(res))
    for c in list(mh.GetConformers()):
        if c.GetId() != best_cid:
            mh.RemoveConformer(c.GetId())
    return mh, best_e

def protonate(mol_h, name):
    ti = tempfile.NamedTemporaryFile(suffix='.sdf', delete=False)
    to = tempfile.NamedTemporaryFile(suffix='.sdf', delete=False)
    ti.close(); to.close()
    w = SDWriter(ti.name); mol_h.SetProp('_Name', name); w.write(mol_h); w.close()
    r = subprocess.run(['obabel', ti.name, '-O', to.name, '-p', '7.4'],
                       capture_output=True, text=True)
    prot = None
    if r.returncode == 0 and Path(to.name).exists():
        sup2 = SDMolSupplier(to.name, removeHs=False, sanitize=False)
        prot = next((x for x in sup2 if x is not None), None)
    Path(ti.name).unlink(missing_ok=True); Path(to.name).unlink(missing_ok=True)
    return prot if prot is not None else mol_h

opts = StereoEnumerationOptions(unique=True, onlyUnassigned=True, maxIsomers=32)
sup  = SDMolSupplier(V2000_SDF, removeHs=False, sanitize=True)

writer   = SDWriter(OUT_SDF)
writer.SetKeepingHydrogens(True)
summary  = []
n_out    = 0

for raw_mol in sup:
    if raw_mol is None:
        continue
    base  = (raw_mol.GetProp('_Name') if raw_mol.HasProp('_Name') else 'Compound').strip().replace(' ', '_')
    props = {p: raw_mol.GetProp(p) for p in raw_mol.GetPropNames() if not p.startswith('_')}
    m2d   = Chem.RemoveHs(raw_mol)

    isomers = list(EnumerateStereoisomers(m2d, options=opts))
    chiral_all = Chem.FindMolChiralCenters(m2d, includeUnassigned=True)
    print(f"{base}: {len(chiral_all)} chiral centers → {len(isomers)} isomers")

    if len(isomers) <= 1:
        pairs = [(base, m2d)]
    elif len(isomers) == 2:
        pairs = [(f"{base}_ent1", isomers[0]), (f"{base}_ent2", isomers[1])]
    else:
        pairs = [(f"{base}_s{i+1}", iso) for i, iso in enumerate(isomers)]

    for iso_name, iso in pairs:
        mol3d, energy = embed3d(iso)
        if mol3d is None:
            print(f"  SKIP {iso_name}: embed failed"); continue
        mol_p = protonate(mol3d, iso_name)
        mol_p.SetProp('_Name', iso_name)
        for k, v in props.items(): mol_p.SetProp(k, str(v))
        mol_p.SetProp('Parent_Compound',        props.get('Molecule Name', iso_name))
        mol_p.SetProp('MMFF94s_energy_kcalmol',  f"{energy:.3f}")
        mol_p.SetProp('pH_protonation',          '7.4')
        writer.write(mol_p)
        n_out += 1
        summary.append({'name': iso_name,
                        'parent': props.get('Molecule Name', iso_name),
                        'heavy_atoms': iso.GetNumAtoms(),
                        'mmff_energy': round(energy, 3),
                        'ec50_um': props.get('EC50 (µM) (Excel)', 'N/A')})
        print(f"  {iso_name}: MMFF={energy:.2f} kcal/mol, atoms={iso.GetNumAtoms()}")
        # Immediately delete mol objects to keep namespace picklable
        del mol3d, mol_p, iso
    del pairs, isomers, m2d, raw_mol

writer.close()
del writer, sup, opts

sz = Path(OUT_SDF).stat().st_size / 1024
print(f"\nWrote {n_out} compounds → CRBN_ID_enantio_2.sdf ({sz:.1f} KB)")
(BASE / "CRBN_enantio2_summary.json").write_text(json.dumps({'compounds': summary}, indent=2))
print("Summary JSON saved.")
