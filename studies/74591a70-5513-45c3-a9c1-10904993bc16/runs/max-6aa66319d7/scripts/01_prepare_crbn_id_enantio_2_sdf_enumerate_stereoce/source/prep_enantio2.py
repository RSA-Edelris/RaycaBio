#!/usr/bin/env python3
"""
Prepare CRBN_ID_enantio_2.sdf from CRBN_lig_results_2.sdf:
1. Read V2000 SDF (converted from V3000 by obabel)
2. Enumerate all stereoisomers (RDKit EnumerateStereoisomers)
3. Generate lowest-energy 3D conformer (ETKDG + MMFF94s)
4. Protonate at pH 7.4 (obabel -p 7.4)
5. Write CRBN_ID_enantio_2.sdf with all SD properties preserved
"""
import sys, subprocess, tempfile, json
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, SDMolSupplier, SDWriter
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers, StereoEnumerationOptions
)

BASE = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
V2000_SDF = BASE / "CRBN_lig_results_2_v2000.sdf"
OUT_SDF   = BASE / "CRBN_ID_enantio_2.sdf"
LOG       = []

def log(msg):
    print(msg, flush=True)
    LOG.append(msg)

# ── 1. Read input ──────────────────────────────────────────────────────────────
sup = SDMolSupplier(str(V2000_SDF), removeHs=False, sanitize=True)
input_mols = [m for m in sup if m is not None]
log(f"Read {len(input_mols)} molecules from {V2000_SDF.name}")

# ── 2. Enumerate stereocenters ─────────────────────────────────────────────────
opts = StereoEnumerationOptions(
    unique=True,          # deduplicate
    onlyUnassigned=True,  # only expand unassigned centers
    maxIsomers=32,        # safety cap
)

all_enumerated = []   # list of (base_name, isomer_idx, mol, props_dict)

for m in input_mols:
    base_name = m.GetProp('_Name') if m.HasProp('_Name') else 'Compound'
    base_name = base_name.strip().replace(' ', '_')

    # Collect original SD properties (excluding internal _ props)
    props = {}
    for pname in m.GetPropNames():
        if not pname.startswith('_'):
            props[pname] = m.GetProp(pname)

    # Strip H for enumeration, keep 2D coords
    m2d = Chem.RemoveHs(m)
    isomers = list(EnumerateStereoisomers(m2d, options=opts))

    chiral_all = Chem.FindMolChiralCenters(m2d, includeUnassigned=True)
    chiral_def = Chem.FindMolChiralCenters(m2d, includeUnassigned=False)
    n_undef = len(chiral_all) - len(chiral_def)
    log(f"  {base_name}: {len(chiral_all)} chiral centers, "
        f"{n_undef} undefined → {len(isomers)} stereoisomers")

    if len(isomers) <= 1:
        isomers = [m2d]  # no enumeration needed
        names = [base_name]
    elif len(isomers) == 2:
        names = [f"{base_name}_ent1", f"{base_name}_ent2"]
    else:
        names = [f"{base_name}_s{i+1}" for i in range(len(isomers))]

    for iso_name, iso in zip(names, isomers):
        all_enumerated.append((iso_name, iso, props))

log(f"\nTotal stereoisomers to process: {len(all_enumerated)}")

# ── 3. Generate 3D conformers (ETKDG v3 + MMFF94s minimisation) ───────────────
def embed_and_minimise(mol, name, n_conf=50):
    """Return best-energy conformer mol or None on failure."""
    mol_h = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    params.numThreads = 0   # use all CPUs

    cids = AllChem.EmbedMultipleConfs(mol_h, numConfs=n_conf, params=params)
    if not cids:
        # fallback: single embed
        cids = AllChem.EmbedMultipleConfs(mol_h, numConfs=1,
                                           params=AllChem.ETKDG())
    if not cids:
        log(f"    WARNING: embedding failed for {name}")
        return None

    # Minimise all conformers, keep lowest energy
    best_e = float('inf')
    best_cid = cids[0]
    ff_results = AllChem.MMFFOptimizeMoleculeConfs(mol_h, mmffVariant='MMFF94s',
                                                    numThreads=0, maxIters=2000)
    for cid, (conv, e) in enumerate(ff_results):
        if e < best_e:
            best_e = e
            best_cid = cid

    # Keep only best conformer
    conf_ids = list(mol_h.GetConformers())
    for c in conf_ids:
        if c.GetId() != best_cid:
            mol_h.RemoveConformer(c.GetId())

    return mol_h, best_e

# ── 4. Protonate with obabel at pH 7.4 ────────────────────────────────────────
def protonate_ph74(mol_h, name):
    """Write to tmp SDF, run obabel -p 7.4, read back."""
    with tempfile.NamedTemporaryFile(suffix='.sdf', delete=False) as f:
        tmp_in = f.name
    with tempfile.NamedTemporaryFile(suffix='.sdf', delete=False) as f:
        tmp_out = f.name

    w = SDWriter(tmp_in)
    mol_copy = Chem.RWMol(mol_h)
    mol_copy.SetProp('_Name', name)
    w.write(mol_copy)
    w.close()

    r = subprocess.run(
        ['obabel', tmp_in, '-O', tmp_out, '-p', '7.4', '--gen3d'],
        capture_output=True, text=True
    )
    if r.returncode != 0 or not Path(tmp_out).exists():
        log(f"    WARNING: obabel protonation failed for {name}, using original")
        Path(tmp_in).unlink(missing_ok=True)
        return mol_h

    sup2 = SDMolSupplier(tmp_out, removeHs=False, sanitize=False)
    prot = next((m for m in sup2 if m is not None), None)
    Path(tmp_in).unlink(missing_ok=True)
    Path(tmp_out).unlink(missing_ok=True)

    if prot is None:
        log(f"    WARNING: obabel produced no molecule for {name}")
        return mol_h
    return prot

# ── Main loop ──────────────────────────────────────────────────────────────────
output_mols = []
summary = []

for iso_name, iso_mol, props in all_enumerated:
    log(f"  Processing {iso_name}...")

    # 3D embed
    result = embed_and_minimise(iso_mol, iso_name)
    if result is None:
        log(f"    SKIPPED: 3D embedding failed")
        continue
    mol3d, energy = result
    log(f"    3D: MMFF94s energy = {energy:.2f} kcal/mol, "
        f"conformers = {mol3d.GetNumConformers()}")

    # Protonation at pH 7.4 (via obabel; keep 3D coords)
    mol_prot = protonate_ph74(mol3d, iso_name)

    # Re-attach name and properties
    mol_prot.SetProp('_Name', iso_name)
    for k, v in props.items():
        mol_prot.SetProp(k, str(v))
    mol_prot.SetProp('Parent_Compound', props.get('Molecule Name', iso_name))
    mol_prot.SetProp('MMFF94s_energy_kcal_mol', f"{energy:.3f}")
    mol_prot.SetProp('pH_protonation', '7.4')

    output_mols.append(mol_prot)
    summary.append({
        'name': iso_name,
        'parent': props.get('Molecule Name', iso_name),
        'n_atoms_noh': iso_mol.GetNumAtoms(),
        'mmff_energy': round(energy, 3),
        'ec50_um': props.get('EC50 (µM) (Excel)', 'N/A'),
    })

# ── 5. Write output SDF ────────────────────────────────────────────────────────
w = SDWriter(str(OUT_SDF))
w.SetKeepingHydrogens(True)
for m in output_mols:
    w.write(m)
w.close()

log(f"\nWritten {len(output_mols)} compounds to {OUT_SDF.name}")
log(f"File size: {OUT_SDF.stat().st_size/1024:.1f} KB")

# ── Summary table ──────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
print(f"{'Name':<30} {'Parent':<15} {'Atoms':>6} {'MMFF(kcal/mol)':>15} {'EC50(µM)':>10}")
print("-"*80)
for s in summary:
    print(f"{s['name']:<30} {s['parent']:<15} {s['n_atoms_noh']:>6} "
          f"{s['mmff_energy']:>15.2f} {s['ec50_um']:>10}")

# Save summary JSON
(BASE / "CRBN_enantio2_summary.json").write_text(
    json.dumps({'compounds': summary}, indent=2))
log(f"\nSummary JSON: CRBN_enantio2_summary.json")
