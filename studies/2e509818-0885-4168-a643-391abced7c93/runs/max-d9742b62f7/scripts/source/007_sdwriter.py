
from rdkit.Chem import SDWriter, AllChem

top96 = shortlist[:96]

out_path = '/home/ubuntu/rayca-sessions/2e509818-0885-4168-a643-391abced7c93-8c1a5f76c087/results.sdf'
writer = SDWriter(out_path)

for rank, row in enumerate(top96, 1):
    mol = Chem.RWMol(row['mol'])
    AllChem.Compute2DCoords(mol)

    def sp(k, v):
        mol.SetProp(k, str(v))

    sp('Rank',            rank)
    sp('CR_ID',           row['cr_id'])
    sp('Acid_Name',       row['acid_name'])
    sp('SMILES',          row['smiles'])
    sp('MPO_Score',       f"{row['mpo_score']:.4f}")

    # Physicochemical
    sp('MW',              f"{row['mw']:.2f}")
    sp('cLogP',           f"{row['clogp']:.2f} ± 0.40")
    sp('TPSA',            f"{row['tpsa']:.1f}")
    sp('HBD',             str(row['hbd']))
    sp('HBA',             str(row['hba']))
    sp('RotBonds',        str(row['rb']))
    sp('Fsp3',            f"{row['fsp3']:.3f}")
    sp('NumArRings',      str(row['n_ar_rings']))

    # Solubility
    sp('logS_ESOL',       f"{row['sol_logS']:.2f} ± {row['sol_logS_sd']:.2f} log(mol/L)")
    sp('logS_AD',         'In' if row['sol_sol_ad'] else 'Out')
    sp('logS_model',      row['sol_sol_model'])

    # Permeability
    sp('logPapp_PAMPA',   f"{row['pampa_logPapp']:.2f} ± {row['pampa_logPapp_sd']:.2f} log(cm/s)")
    sp('logPapp_class',   row['pampa_pampa_cat'])
    sp('logPapp_AD',      'In' if row['pampa_pampa_ad'] else 'Out')
    sp('logPapp_model',   row['pampa_pampa_model'])

    # Metabolic stability
    sp('MetStab_score',   f"{row['met_met_score']:.3f} (0-1 scale)")
    sp('MetStab_t12',     row['met_t12_class'])
    sp('Clearance_route', row['met_clearance_route'])
    sp('Met_alerts',      row['met_met_flags'])
    sp('MetStab_model',   row['met_met_model'])

    # CYP
    sp('CYP_risk',        row['cyp_cyp_risk'])
    sp('CYP_alerts',      row['cyp_cyp_alerts'])
    sp('CYP2D6_flag',     str(row['cyp_cyp2d6']))
    sp('CYP3A4_flag',     str(row['cyp_cyp3a4']))
    sp('CYP2C9_flag',     str(row['cyp_cyp2c9']))
    sp('CYP_model',       row['cyp_cyp_model'])

    # PPB
    sp('PPB_pct',         f"{row['ppb_ppb_pct']:.1f} ± 10 %")
    sp('PPB_fu',          f"{row['ppb_ppb_fu']:.4f}")
    sp('PPB_class',       row['ppb_ppb_class'])
    sp('PPB_AD',          'In' if row['ppb_ppb_ad'] else 'Out')
    sp('PPB_model',       row['ppb_ppb_model'])

    # hERG
    sp('hERG_risk',       row['herg_herg_risk'])
    sp('hERG_model',      row['herg_herg_model'])

    # Desirability breakdown
    db = row['des_breakdown']
    sp('des_sol',  f"{db['sol']:.3f}")
    sp('des_logp', f"{db['logp']:.3f}")
    sp('des_perm', f"{db['perm']:.3f}")
    sp('des_met',  f"{db['met']:.3f}")
    sp('des_cyp',  f"{db['cyp']:.3f}")
    sp('des_ppb',  f"{db['ppb']:.3f}")
    sp('des_herg', f"{db['herg']:.3f}")
    sp('des_mw',   f"{db['mw']:.3f}")

    writer.write(mol)

writer.close()
print(f"Wrote {len(top96)} compounds to {out_path}")
import os
print(f"File size: {os.path.getsize(out_path):,} bytes")
