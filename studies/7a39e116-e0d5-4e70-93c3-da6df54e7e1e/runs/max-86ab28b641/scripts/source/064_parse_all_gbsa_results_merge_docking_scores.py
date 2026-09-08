
import json

# Parse all GBSA results and merge with docking scores
full_table = []

for lig_name in ligand_names:
    gbsa_data = gbsa_all.get(lig_name, {})
    results   = gbsa_data.get('results', [])
    
    for rank in range(1, 6):
        dock_r = [r for r in pose_table if r['mol_name'] == lig_name and r['rank'] == rank][0]
        
        # Match GBSA result by index (results ordered same as ligandFiles)
        if results and rank-1 < len(results):
            gbr = results[rank-1]
            try: vdw  = float(gbr.get('Van der Waals', gbr.get('vdw','nan')))
            except: vdw = float('nan')
            try: elec = float(gbr.get('Electrostatic', gbr.get('ele','nan')))
            except: elec = float('nan')
            try: polar = float(gbr.get('Polar Solvation', gbr.get('polar_solv','nan')))
            except: polar = float('nan')
            try: nonpolar = float(gbr.get('Non-Polar Solvation', gbr.get('nonpolar_solv','nan')))
            except: nonpolar = float('nan')
            try: total_gb = float(gbr.get('TOTAL', gbr.get('total','nan')))
            except: total_gb = float('nan')
        else:
            vdw = elec = polar = nonpolar = total_gb = float('nan')
        
        full_table.append({
            'lig': lig_name, 'rank': rank,
            'affinity': dock_r['affinity'],
            'cnn_score': dock_r['cnn_score'],
            'cnn_aff': dock_r['cnn_aff'],
            'pic50': dock_r['pic50'],
            'vdw': vdw, 'elec': elec,
            'polar': polar, 'nonpolar': nonpolar,
            'mmgbsa': total_gb
        })

# Print consolidated table
print(f"{'Molecule':22s} {'Rank':>4} {'Affin':>7} {'CNN':>6} {'CNNaff':>7} "
      f"{'VdW':>8} {'Elec':>8} {'Polar':>8} {'NpSolv':>8} {'ΔG_GBSA':>10}")
print('-'*100)
for r in full_table:
    gb_s = f"{r['mmgbsa']:10.2f}" if r['mmgbsa'] == r['mmgbsa'] else "       nan"
    print(f"{r['lig']:22s} {r['rank']:>4} {r['affinity']:>7.3f} "
          f"{r['cnn_score']:>6.3f} {r['cnn_aff']:>7.3f} "
          f"{r['vdw']:>8.2f} {r['elec']:>8.2f} {r['polar']:>8.2f} "
          f"{r['nonpolar']:>8.2f}{gb_s}")
