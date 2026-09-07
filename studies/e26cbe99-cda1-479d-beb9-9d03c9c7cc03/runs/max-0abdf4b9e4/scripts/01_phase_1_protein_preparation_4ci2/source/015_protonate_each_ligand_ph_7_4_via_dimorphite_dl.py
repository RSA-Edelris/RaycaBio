
from rdkit import Chem
from rdkit.Chem import AllChem, SDWriter

# ── Protonate each ligand at pH 7.4 via Dimorphite-DL ─────────────────────────
protonated_ligands = []   # list of dicts

for lig in ligand_info:
    name = lig['name']
    smi  = lig['smiles']
    print(f"\n{name}")
    print(f"  Input SMILES: {smi}")

    result = dispatch('protonation-state', {
        'inputType':   'smiles',
        'smiles':      smi,
        'pH':          7.4,
        'ph_range':    1.0,
        'max_variants': 4,
    })

    if result.get('rc') != 0:
        print(f"  protonation-state FAILED — using input SMILES as fallback")
        prot_smiles_list = [smi]
    else:
        prot_smiles_list = result.get('protonated_smiles', [smi])

    # Pick the first protonation variant as the dominant state
    dominant = prot_smiles_list[0]
    print(f"  pH 7.4 dominant: {dominant}")
    if len(prot_smiles_list) > 1:
        print(f"  ({len(prot_smiles_list)} variants, using first)")

    protonated_ligands.append({'name': name, 'smiles': dominant})

print(f"\n✓ Protonation done for {len(protonated_ligands)} ligands")
