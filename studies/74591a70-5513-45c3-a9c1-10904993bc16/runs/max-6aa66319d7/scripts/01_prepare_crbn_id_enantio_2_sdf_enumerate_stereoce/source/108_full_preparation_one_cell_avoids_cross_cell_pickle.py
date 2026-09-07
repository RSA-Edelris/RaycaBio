
# Full preparation in one cell — avoids cross-cell pickle issues
import json, subprocess, tempfile
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, SDMolSupplier, SDWriter
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers, StereoEnumerationOptions
)

BASE      = Path("/home/ubuntu/rayca-sessions/74591a70-5513-45c3-a9c1-10904993bc16-aa94c8cd626e")
V2000_SDF = BASE / "CRBN_lig_results_2_v2000.sdf"
OUT_SDF   = BASE / "CRBN_ID_enantio_2.sdf"

LOG = []
def log(msg):
    print(msg, flush=True)
    LOG.append(msg)

# ── 1. Read ────────────────────────────────────────────────────────────────────
sup = SDMolSupplier(str(V2000_SDF), removeHs=False, sanitize=True)
input_mols = [m for m in sup if m is not None]
log(f"Read {len(input_mols)} molecules")

# ── 2. Enumerate stereocenters ─────────────────────────────────────────────────
opts = StereoEnumerationOptions(unique=True, onlyUnassigned=True, maxIsomers=32)
all_items = []  # (iso_name, iso_mol_2d, props_dict)

for m in input_mols:
    base = (m.GetProp('_Name') if m.HasProp('_Name') else 'Compound').strip().replace(' ', '_')
    props = {p: m.GetProp(p) for p in m.GetPropNames() if not p.startswith('_')}
    m2d = Chem.RemoveHs(m)
    isomers = list(EnumerateStereoisomers(m2d, options=opts))
    chiral_all  = Chem.FindMolChiralCenters(m2d, includeUnassigned=True)
    chiral_def  = Chem.FindMolChiralCenters(m2d, includeUnassigned=False)
    n_undef = len(chiral_all) - len(chiral_def)
    log(f"  {base}: {len(chiral_all)} chiral centers, {n_undef} undefined → {len(isomers)} isomers")

    if len(isomers) <= 1:
        names = [base]
        isomers = [m2d]
    elif len(isomers) == 2:
        names = [f"{base}_ent1", f"{base}_ent2"]
    else:
        names = [f"{base}_s{i+1}" for i in range(len(isomers))]

    for n, iso in zip(names, isomers):
        all_items.append((n, iso, props))

log(f"\nTotal to embed: {len(all_items)}")

# ── 3. Embed + MMFF94s minimise ────────────────────────────────────────────────
def embed3d(mol, name, n_conf=50):
    mh = Chem.AddHs(mol)
    p = AllChem.ETKDGv3(); p.randomSeed = 42; p.numThreads = 0
    cids = AllChem.EmbedMultipleConfs(mh, numConfs=n_conf, params=p)
    if not cids:
        p2 = AllChem.ETKDG(); p2.randomSeed = 42
        cids = AllChem.EmbedMultipleConfs(mh, numConfs=1, params=p2)
    if not cids:
        return None, None
    res = AllChem.MMFFOptimizeMoleculeConfs(mh, mmffVariant='MMFF94s', numThreads=0, maxIters=2000)
    best_e, best_cid = min((e, cid) for cid,(conv,e) in enumerate(res))
    # Remove non-best conformers
    for c in list(mh.GetConformers()):
        if c.GetId() != best_cid:
            mh.RemoveConformer(c.GetId())
    return mh, best_e

# ── 4. Protonate at pH 7.4 with obabel ────────────────────────────────────────
def protonate(mol_h, name):
    """Write, call obabel -p 7.4, read back. Returns mol (possibly same)."""
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

# ── Main loop ──────────────────────────────────────────────────────────────────
output_mols = []
summary     = []

for iso_name, iso_mol, props in all_items:
    log(f"  {iso_name}...")
    mol3d, energy = embed3d(iso_mol, iso_name)
    if mol3d is None:
        log(f"    SKIP: embed failed"); continue
    mol_p = protonate(mol3d, iso_name)
    mol_p.SetProp('_Name', iso_name)
    for k, v in props.items(): mol_p.SetProp(k, str(v))
    mol_p.SetProp('Parent_Compound',       props.get('Molecule Name', iso_name))
    mol_p.SetProp('MMFF94s_energy_kcalmol', f"{energy:.3f}")
    mol_p.SetProp('pH_protonation',         '7.4')
    output_mols.append(mol_p)
    summary.append({'name': iso_name,
                    'parent': props.get('Molecule Name', iso_name),
                    'heavy_atoms': iso_mol.GetNumAtoms(),
                    'mmff_energy': round(energy, 3),
                    'ec50_um': props.get('EC50 (µM) (Excel)', 'N/A')})

# ── 5. Write SDF ───────────────────────────────────────────────────────────────
w = SDWriter(str(OUT_SDF))
w.SetKeepingHydrogens(True)
for m in output_mols: w.write(m)
w.close()

log(f"\nWritten {len(output_mols)} compounds → {OUT_SDF.name}  ({OUT_SDF.stat().st_size/1024:.1f} KB)")

print("\n=== SUMMARY TABLE ===")
print(f"{'Name':<32} {'Parent':<14} {'HeavyAtoms':>10} {'MMFF(kcal/mol)':>15} {'EC50(µM)':>10}")
print("─"*85)
for s in summary:
    print(f"{s['name']:<32} {s['parent']:<14} {s['heavy_atoms']:>10} "
          f"{s['mmff_energy']:>15.2f} {s['ec50_um']:>10}")

(BASE / "CRBN_enantio2_summary.json").write_text(json.dumps({'compounds': summary}, indent=2))
print("\nSummary JSON saved.")
