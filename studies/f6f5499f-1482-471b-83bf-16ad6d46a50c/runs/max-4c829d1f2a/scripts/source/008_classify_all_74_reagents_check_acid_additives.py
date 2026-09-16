
# Classify all 74 reagents and check for acid additives (critical for Minisci)
classifications2 = {
    # Photocatalysts - Ir
    12: ('Ir[F-tBupy]₃ (fac)',          'Photocatalyst-Ir'),
    31: ('Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆', 'Photocatalyst-Ir'),
    35: ('Ir(ppy)₂(dtbbpy)·PF₆',         'Photocatalyst-Ir'),
    58: ('fac-Ir(ppy)₃',                 'Photocatalyst-Ir'),
    # Photocatalysts - Ru
    13: ('[Ru(bpym)₃]Cl₂',              'Photocatalyst-Ru'),
    15: ('[Ru(bpy)₃]Cl₂·6H₂O',          'Photocatalyst-Ru'),
    33: ('[Ru(bpz)₃](PF₆)₂',            'Photocatalyst-Ru'),
    # Organic photocatalysts
    5:  ('3DPAFIPN',                     'Photocatalyst-Org'),
    6:  ('3DPA2FBN',                     'Photocatalyst-Org'),
    32: ('Mes-Acr⁺·BF₄',               'Photocatalyst-Org'),
    38: ('4CzIPN',                       'Photocatalyst-Org'),
    60: ('Acridinium-tBu·BF₄',          'Photocatalyst-Org'),
    # Ni catalysts (not needed for Minisci)
    10: ('Ni(cod)₂',   'Ni-cat'),
    21: ('NiBr₂·dme',  'Ni-cat'),
    34: ('NiCl₂·dme',  'Ni-cat'),
    55: ('Ni(acac)₂',  'Ni-cat'),
    # Pd catalysts
    **{i: (f'Pd-cat-{i}', 'Pd-cat') for i in [0,2,3,7,8,9,14,16,17,18,19,30,36,39,40,47,56,59,61,63]},
    # N-ligands
    1:  ("4,4'-dMe-bpy",    'N-Ligand'),
    4:  ("5,5'-dMe-bpy",    'N-Ligand'),
    11: ("4,4'-dCF₃-bpy",  'N-Ligand'),
    22: ('4,7-dOMe-phen',   'N-Ligand'),
    26: ("4,4'-dOMe-bpy",  'N-Ligand'),
    27: ('dtbbpy',          'N-Ligand'),
    44: ('2,6-lutidine',    'Ligand-mono'),
    46: ('1,10-phen',       'N-Ligand'),
    54: ('Pyridine',        'Ligand-mono'),
    57: ("6,6'-dMe-bpy",   'N-Ligand'),
    62: ('DACH-Schiff',     'N-Ligand-chiral'),
    # Bases
    23: ('NaOTMS',   'Base'),
    29: ('tBu-TMG',  'Base'),
    37: ('DBU',      'Base'),
    41: ('TMG',      'Base'),
    42: ('LiHMDS',   'Base'),
    43: ('NaOtBu',   'Base'),
    48: ('DIPEA',    'Base'),
    50: ('K₂CO₃',   'Base'),
    51: ('CsF',      'Base'),
    52: ('Cs₂CO₃',  'Base'),
    53: ('K₃PO₄',   'Base'),
    71: ('DBU(dup)', 'Base'),
    # Solvents
    24: ('DMSO',     'Solvent'),
    25: ('Toluene',  'Solvent'),
    64: ('MeOH',     'Solvent'),
    65: ('DMF',      'Solvent'),
    66: ('DMA',      'Solvent'),
    67: ('NMP',      'Solvent'),
    68: ('DCE',      'Solvent'),
    69: ('t-AmylOH', 'Solvent'),
    70: ('Dioxane',  'Solvent'),
    72: ('MeCN',     'Solvent'),   # ← NEW vs kit 1
    73: ('Water',    'Solvent'),   # ← NEW vs kit 1
    # Other
    20: ('VPhos',       'P-Ligand'),
    45: ('DPEPhos',     'P-Ligand'),
    28: ('Quinuclidine','HAT-additive'),
    49: ('CuI',         'Cu-cat'),
}

from collections import defaultdict
by_class2 = defaultdict(list)
for idx, (name, cls) in classifications2.items():
    by_class2[cls].append((idx, name))

print("=== HTE_Edelris_2.sdf — REAGENT INVENTORY ===\n")
for cls in sorted(by_class2):
    items = by_class2[cls]
    if 'Pd' in cls:
        print(f"--- {cls} ({len(items)} entries, not relevant — skipped) ---")
        continue
    print(f"--- {cls} ---")
    for idx, name in items:
        print(f"  [{idx:2d}] {name}")
    print()

# Check for Brønsted acids (TFA, H2SO4, AcOH, p-TsOH, etc.)
print("\n=== BRØNSTED ACID CHECK (critical for Minisci) ===")
acid_found = []
for idx, (name, cls) in classifications2.items():
    smi = df2.loc[idx, 'smiles']
    # Look for free COOH, SO3H, simple organic acids
    if 'C(=O)O' in smi and 'N' not in smi and '[O-]' not in smi:
        acid_found.append((idx, name, smi))
    if 'S(=O)(=O)O' in smi and '[' not in smi:
        acid_found.append((idx, name, smi))

if acid_found:
    for idx, name, smi in acid_found:
        print(f"  Found acid: [{idx}] {name}  SMILES={smi}")
else:
    print("  *** NO BRØNSTED ACID FOUND IN KIT ***")
    print("  TFA (trifluoroacetic acid) is ABSENT — must be purchased.")
    print("  This is absolutely necessary for Minisci radical addition to quinoline.")
    print("  Without protonation of the quinoline N, radical addition rate drops >10x.")
