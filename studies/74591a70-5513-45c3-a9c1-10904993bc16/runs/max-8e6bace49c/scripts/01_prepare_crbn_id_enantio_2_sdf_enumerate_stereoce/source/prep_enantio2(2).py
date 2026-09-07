#!/usr/bin/env python3
"""Enumerate stereocenters, embed 3D, protonate at pH 7.4 → CRBN_ID_enantio_2.sdf"""
import json, subprocess, sys, tempfile
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, SDMolSupplier, SDWriter
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers, StereoEnumerationOptions
)

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
V2000_SDF = BASE / "CRBN_lig_results_2_v2000.sdf"
OUT_SDF   = BASE / "CRBN_ID_enantio_2.sdf"

def embed3d(mol, name, n_conf=50):
    mh = Chem.AddHs(mol)
    p = AllChem.ETKDGv3(); p.randomSeed = 42; p.numThreads = 0
    cids = AllChem.EmbedMultipleConfs(mh, numConfs=n_conf, params=p)
    if not cids:
        p2 = AllChem.ETKDG(); p2.randomSeed = 42
        cids = AllChem.EmbedMultipleConfs(mh, numConfs=1, params=p2)
    if not cids:
        print(f"  SKIP {name}: embed failed", flush=True)
        return None, None
    res = AllChem.MMFFOptimizeMoleculeConfs(mh, mmffVariant='MMFF94s', numThreads=0, maxIters=2000)
    if not res:
        return mh, 9999.0
    best_e, best_cid = min((e, cid) for cid, (conv, e) in enumerate(res))
    for c in list(mh.GetConformers()):
        if c.GetId() != best_cid:
            mh.RemoveConformer(c.GetId())
    return mh, best_e

def protonate_obabel(sdf_in, sdf_out, ph=7.4):
    r = subprocess.run(
        ['obabel', str(sdf_in), '-O', str(sdf_out), '-p', str(ph)],
        capture_output=True, text=True
    )
    return r.returncode == 0

opts   = StereoEnumerationOptions(unique=True, onlyUnassigned=True, maxIsomers=32)
sup    = SDMolSupplier(str(V2000_SDF), removeHs=False, sanitize=True)
summary = []

# Stage 1: embed all isomers into a temp SDF
tmp_stage1 = BASE / "CRBN_enantio2_stage1.sdf"
writer = SDWriter(str(tmp_stage1))
n_stage1 = 0

for raw_mol in sup:
    if raw_mol is None:
        continue
    base  = (raw_mol.GetProp('_Name') if raw_mol.HasProp('_Name') else 'Compound').strip().replace(' ', '_')
    props = {p: raw_mol.GetProp(p) for p in raw_mol.GetPropNames() if not p.startswith('_')}
    m2d   = Chem.RemoveHs(raw_mol)

    isomers = list(EnumerateStereoisomers(m2d, options=opts))
    chiral_all = Chem.FindMolChiralCenters(m2d, includeUnassigned=True)
    print(f"{base}: {len(chiral_all)} chiral centers → {len(isomers)} isomers", flush=True)

    if   len(isomers) <= 1: pairs = [(base, m2d)]
    elif len(isomers) == 2: pairs = [(f"{base}_ent1", isomers[0]), (f"{base}_ent2", isomers[1])]
    else:                   pairs = [(f"{base}_s{i+1}", iso) for i, iso in enumerate(isomers)]

    for iso_name, iso in pairs:
        mol3d, energy = embed3d(iso, iso_name)
        if mol3d is None:
            continue
        mol3d.SetProp('_Name', iso_name)
        for k, v in props.items():
            mol3d.SetProp(k, str(v))
        mol3d.SetProp('Parent_Compound',        props.get('Molecule Name', iso_name))
        mol3d.SetProp('MMFF94s_energy_kcalmol', f"{energy:.3f}")
        writer.write(mol3d)
        n_stage1 += 1
        summary.append({
            'name': iso_name,
            'parent': props.get('Molecule Name', iso_name),
            'heavy_atoms': iso.GetNumAtoms(),
            'mmff_energy': round(energy, 3),
            'ec50_um': props.get('EC50 (µM) (Excel)', 'N/A'),
        })
        print(f"  {iso_name}: MMFF={energy:.2f} kcal/mol, nHA={iso.GetNumAtoms()}", flush=True)

writer.close()
print(f"\nStage 1: {n_stage1} compounds in {tmp_stage1.name} ({tmp_stage1.stat().st_size/1024:.1f} KB)", flush=True)

# Stage 2: protonate at pH 7.4 with obabel
ok = protonate_obabel(tmp_stage1, OUT_SDF)
if ok and OUT_SDF.exists() and OUT_SDF.stat().st_size > 0:
    # Re-read to restore SD properties (obabel strips them by default without -d flag)
    # Use the stage1 file instead (obabel -p only adjusts protonation, keeps properties when using the same format)
    # Check if properties were kept
    test = SDMolSupplier(str(OUT_SDF), removeHs=False, sanitize=False)
    m0 = next((m for m in test if m is not None), None)
    if m0 is not None and m0.HasProp('Parent_Compound'):
        print(f"obabel protonation OK, properties preserved → {OUT_SDF.name}", flush=True)
    else:
        # obabel dropped SD tags — merge back from stage1
        print("obabel dropped SD tags — merging properties from stage1", flush=True)
        sup1 = SDMolSupplier(str(tmp_stage1), removeHs=False, sanitize=False)
        sup2 = SDMolSupplier(str(OUT_SDF),    removeHs=False, sanitize=False)
        mols1 = [m for m in sup1 if m is not None]
        mols2 = [m for m in sup2 if m is not None]
        final_writer = SDWriter(str(OUT_SDF))
        for m1, m2 in zip(mols1, mols2):
            # copy 3D coords from m2 (protonated) but keep props from m1
            for pname in m1.GetPropNames():
                m2.SetProp(pname, m1.GetProp(pname))
            m2.SetProp('pH_protonation', '7.4')
            final_writer.write(m2)
        final_writer.close()
        print(f"Merged → {OUT_SDF.name}", flush=True)
else:
    print("obabel protonation failed — copying stage1 as final output", flush=True)
    import shutil
    shutil.copy(tmp_stage1, OUT_SDF)

print(f"\nFinal: {OUT_SDF.stat().st_size/1024:.1f} KB", flush=True)

# Verify final count
sup_final = SDMolSupplier(str(OUT_SDF), removeHs=False, sanitize=False)
n_final = sum(1 for m in sup_final if m is not None)
print(f"Final compound count: {n_final}", flush=True)

# Save summary
for s in summary:
    s['n_final'] = n_final
(BASE / "CRBN_enantio2_summary.json").write_text(json.dumps({'compounds': summary}, indent=2))

print("\n=== SUMMARY ===")
print(f"{'Name':<30} {'Parent':<14} {'nHA':>4} {'MMFF(kcal/mol)':>15} {'EC50(µM)':>10}")
print("─"*77)
for s in summary:
    print(f"{s['name']:<30} {s['parent']:<14} {s['heavy_atoms']:>4} "
          f"{s['mmff_energy']:>15.2f} {s['ec50_um']:>10}")
print(f"\nTotal: {len(summary)} compounds → {OUT_SDF.name}")
