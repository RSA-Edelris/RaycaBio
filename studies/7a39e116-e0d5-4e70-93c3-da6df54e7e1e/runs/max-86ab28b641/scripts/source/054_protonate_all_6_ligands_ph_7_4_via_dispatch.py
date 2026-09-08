
# Protonate all 6 ligands at pH 7.4 via dispatch
protonated = []
for lig in ligand_data:
    print(f"Protonating {lig['name']}...", flush=True)
    res = dispatch("protonation-state", {
        "inputType": "smiles",
        "smiles": lig['smiles'],
        "pH": 7.4,
        "ph_range": 1.0,
        "precision": 1.0,
        "label_states": True
    })
    variants = res.get("protonated_smiles", [])
    # Pick the first (dominant) variant at pH 7.4
    chosen = variants[0] if variants else lig['smiles']
    protonated.append({**lig, 'protonated_smiles': chosen, 'num_variants': len(variants)})
    print(f"  rc={res.get('rc')}  variants={len(variants)}  chosen={chosen}")

print("\nAll protonations done.")
