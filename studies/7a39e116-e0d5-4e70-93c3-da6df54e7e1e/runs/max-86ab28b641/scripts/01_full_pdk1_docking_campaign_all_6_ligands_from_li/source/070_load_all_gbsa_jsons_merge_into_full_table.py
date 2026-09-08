
# Load all GBSA JSONs and merge into full_table
gbsa_by_lig = {}
for jpath in gbsa_jsons:
    lig = os.path.basename(jpath).replace('gbsa_', '').replace('.json', '')
    with open(jpath) as fh:
        gbsa_by_lig[lig] = json.load(fh)

full_table = []
for row in pose_table:
    lig = row['mol_name']
    rank = row['rank']
    gbsa_results = gbsa_by_lig.get(lig, {}).get('results', [])
    gb = gbsa_results[rank-1] if rank-1 < len(gbsa_results) else {}
    full_table.append({
        **row,
        'vdw':      float(gb.get('Van der Waals', 'nan')),
        'elec':     float(gb.get('Electrostatic', 'nan')),
        'polar':    float(gb.get('Polar Solvation', 'nan')),
        'nonpolar': float(gb.get('Non-Polar Solvation', 'nan')),
        'gas':      float(gb.get('Gas', 'nan')),
        'mmgbsa':   float(gb.get('TOTAL', 'nan')),
    })

# Print merged table
hdr = f"{'Molecule':22s} {'R':>2} {'pIC50':>5} {'Affin':>7} {'CNN':>6} {'CNNaff':>7} {'VdW':>8} {'Elec':>8} {'Polar':>8} {'NpSolv':>8} {'ΔG_GBSA':>9}"
print(hdr)
print('-'*105)
for r in full_table:
    print(f"{r['mol_name']:22s} {r['rank']:>2} {r['pic50']:>5.1f} {r['affinity']:>7.3f} "
          f"{r['cnn_score']:>6.4f} {r['cnn_aff']:>7.4f} "
          f"{r['vdw']:>8.2f} {r['elec']:>8.2f} {r['polar']:>8.2f} "
          f"{r['nonpolar']:>8.3f} {r['mmgbsa']:>9.3f}")
