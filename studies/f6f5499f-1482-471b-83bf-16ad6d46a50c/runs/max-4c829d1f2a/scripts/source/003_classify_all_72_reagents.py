
# Classify all 72 reagents
classifications = {
    # Photocatalysts - Ir
    12: ('Ir[dF(4-tBupy)]₂(dtbbpy)', 'Photocatalyst-Ir'),
    31: ('Ir[dF(CF₃)ppy]₂(dtbbpy)·PF₆', 'Photocatalyst-Ir'),    # MacMillan Ir PC
    35: ('Ir(ppy)₂(dtbbpy)·PF₆', 'Photocatalyst-Ir'),
    58: ('Ir(ppy)₃', 'Photocatalyst-Ir'),
    # Photocatalysts - Ru
    13: ('[Ru(bpz)₃]Cl₂', 'Photocatalyst-Ru'),
    15: ('[Ru(bpy)₃]Cl₂·6H₂O', 'Photocatalyst-Ru'),
    33: ('[Ru(bpz)₃](PF₆)₂', 'Photocatalyst-Ru'),
    # Organic photocatalysts
    5:  ('4DPAIPN-F', 'Photocatalyst-Org'),
    6:  ('4DPAIPN-2F', 'Photocatalyst-Org'),
    32: ('Mes-Acr⁺·BF₄', 'Photocatalyst-Org'),    # Fukuzumi acridinium
    38: ('4CzIPN', 'Photocatalyst-Org'),
    60: ('Acridinium-tBu·BF₄', 'Photocatalyst-Org'),
    # Ni catalysts
    10: ('Ni(cod)₂', 'Ni-cat'),
    21: ('NiBr₂·dme', 'Ni-cat'),
    34: ('NiCl₂·dme', 'Ni-cat'),
    55: ('Ni(acac)₂', 'Ni-cat'),
    # Pd catalysts (not relevant)
    0:  ('Pd-BrettPhos', 'Pd-cat'), 2:  ('Pd-RuPhos', 'Pd-cat'), 3:  ('Pd-XPhos', 'Pd-cat'),
    7:  ('Pd-BINAP', 'Pd-cat'), 8:  ('Pd-MandPhos', 'Pd-cat'), 9:  ('Pd-PCy₃·OMs', 'Pd-cat'),
    14: ('Pd-DPEPhos', 'Pd-cat'), 16: ('Pd-DavePhos', 'Pd-cat'), 17: ('Pd-tBuXPhos', 'Pd-cat'),
    18: ('Pd-BippyPhos', 'Pd-cat'), 19: ('Pd-AdBrettPhos', 'Pd-cat'), 30: ('Pd-BDMPhos', 'Pd-cat'),
    36: ('Pd-XantPhos', 'Pd-cat'), 39: ('Pd-DTBP-Binap', 'Pd-cat'), 40: ('Pd(OAc)₂', 'Pd-cat'),
    47: ('Pd₂(dba)₃', 'Pd-cat'), 56: ('Pd-CyJohnPhos', 'Pd-cat'), 59: ('Pd-AdBrettPhos II', 'Pd-cat'),
    61: ('Pd-NHC-Cl₂', 'Pd-cat'), 63: ('Pd-iPrBrettPhos', 'Pd-cat'),
    # Ligands for Ni
    1:  ('4,4\'-dMe-bpy', 'N-Ligand'),
    4:  ('5,5\'-dMe-bpy', 'N-Ligand'),
    11: ('5,5\'-dCF₃-bpy', 'N-Ligand'),
    22: ('4,7-dOMe-phen', 'N-Ligand'),
    26: ('4,4\'-dOMe-bpy', 'N-Ligand'),
    27: ('dtbbpy', 'N-Ligand'),              # MacMillan standard Ni ligand
    44: ('2,6-lutidine', 'Ligand-mono'),
    45: ('DPEPhos', 'P-Ligand'),
    46: ('1,10-phen', 'N-Ligand'),
    54: ('Pyridine', 'Ligand-mono'),
    57: ('6,6\'-dMe-bpy', 'N-Ligand'),
    62: ('DACH-Schiff', 'N-Ligand-chiral'),
    # Bases
    23: ('NaOTMS', 'Base-Si'),
    29: ('tBu-TMG', 'Base-amidine'),
    41: ('TMG', 'Base-amidine'),
    42: ('LiHMDS', 'Base-Si'),
    43: ('NaOtBu', 'Base-alkoxide'),
    48: ('DIPEA', 'Base-amine'),
    50: ('K₂CO₃', 'Base-inorg'),
    51: ('CsF', 'Base-inorg'),
    52: ('Cs₂CO₃', 'Base-inorg'),
    53: ('K₃PO₄', 'Base-inorg'),
    # Solvents
    24: ('DMSO', 'Solvent'),
    25: ('Toluene', 'Solvent'),
    64: ('MeOH', 'Solvent'),
    65: ('DMF', 'Solvent'),
    66: ('DMA', 'Solvent'),
    67: ('NMP', 'Solvent'),
    68: ('DCM', 'Solvent'),
    69: ('tAmylOH', 'Solvent'),
    70: ('DME', 'Solvent'),
    # Amines / misc
    28: ('Quinuclidine', 'Amine-HAT'),
    37: ('DBU', 'Base-amidine'),
    71: ('DBU (dup)', 'Base-amidine'),
    49: ('CuI', 'Cu-cat'),
}

print("=== REAGENT INVENTORY BY CLASS ===\n")
from collections import defaultdict
by_class = defaultdict(list)
for idx, (name, cls) in classifications.items():
    by_class[cls].append((idx, name))

for cls in sorted(by_class):
    print(f"--- {cls} ---")
    for idx, name in by_class[cls]:
        print(f"  [{idx:2d}] {name}")
    print()
