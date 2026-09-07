
def write_annotated_sdf(rows, out_path, pic50_map_local):
    """Write annotated SDF from full_table rows that include mol_lines."""
    with open(out_path, 'w') as fh:
        for row in rows:
            mol_lines = row['mol_lines']
            # Rebuild record: keep molblock (up to first property or $$$$),
            # then append our curated properties, then $$$$
            # Find end of molblock (first blank line after counts, or M  END)
            block = []
            props_start = None
            for i, ln in enumerate(mol_lines):
                if ln.strip() == '$$$$':
                    break
                if ln.startswith('> ') or (ln.strip().startswith('>') and '<' in ln):
                    if props_start is None:
                        props_start = i
                    break
                block.append(ln)

            # Write molblock
            fh.writelines(block)

            # Append standardised properties
            lig = row['mol_name']
            props = {
                'Molecule_Name':  lig,
                'Pose_Rank':      str(row['rank']),
                'pIC50_PDK1':     f"{pic50_map_local.get(lig, '')}",
                'GNINA_Affinity_kcal_mol': f"{row['affinity']:.4f}",
                'CNN_Score':      f"{row['cnn_score']:.4f}",
                'CNN_Affinity':   f"{row['cnn_aff']:.4f}",
                'MMGBSA_dG_kcal_mol': f"{row['mmgbsa']:.3f}",
                'MMGBSA_VdW':     f"{row['vdw']:.3f}",
                'MMGBSA_Elec':    f"{row['elec']:.3f}",
                'MMGBSA_PolarSolv': f"{row['polar']:.3f}",
                'MMGBSA_NonPolarSolv': f"{row['npsolv']:.3f}",
            }
            for k, v in props.items():
                fh.write(f">  <{k}>\n{v}\n\n")
            fh.write('$$$$\n')

    size = os.path.getsize(out_path)
    print(f"  Written: {out_path}  ({size:,} bytes, {len(rows)} records)")

pic50_map_local = {'EL2003A-A2U1': 7.6, 'EL2003A': 7.5, 'EL2003A-A4U1': 7.5,
                   'BX912': 6.0, 'EL5001A': 6.5, 'EL5003A': 6.8}

# --- docking_PDK1.sdf: all 30 poses in ligand/rank order ---
ordered_all = sorted(full_table, key=lambda r: (ligand_names.index(r['mol_name']), r['rank']))
dock_path = f"{ART}/docking_PDK1.sdf"
write_annotated_sdf(ordered_all, dock_path, pic50_map_local)

# --- MD_PDK1.sdf: best GBSA pose per ligand (EM-refined selection), ligand order ---
best_rows = [best_poses[lig] for lig in ligand_names]
md_path = f"{ART}/MD_PDK1.sdf"
write_annotated_sdf(best_rows, md_path, pic50_map_local)

print("\nVerification — record counts:")
for path in [dock_path, md_path]:
    with open(path) as fh:
        n = sum(1 for ln in fh if ln.strip() == '$$$$')
    print(f"  {os.path.basename(path)}: {n} records")
