
import random

# Full experiment table with randomised dispensing order
random.seed(42)

experiments = []
exp_id = 1
for ri, row in enumerate(ROWS):
    pc = PHOTOCATALYSTS[row]
    for ci, col in enumerate(COLS):
        base_name, base_short, base_src = BASES[col]
        if col in (1,2): lig_name, lig_src = 'dtbbpy', 'kit #27'
        elif col in (3,4): lig_name, lig_src = "4,4'-dMe-bpy", 'kit #1'
        else: lig_name, lig_src = '1,10-phen', 'kit #46'
        
        experiments.append({
            'Exp#': exp_id,
            'Well': f'{row}{col}',
            'Photocatalyst': pc['name'],
            'PC_source': pc['source'],
            'Ni-Ligand': lig_name,
            'Lig_source': lig_src,
            'Base': base_name,
            'Base_source': base_src,
        })
        exp_id += 1

# Randomise dispensing order
disp_order = list(range(len(experiments)))
random.shuffle(disp_order)

print("FULL EXPERIMENT TABLE — 24-Well Plate, Round 1")
print("="*100)
print(f"{'Disp':<5} {'Well':<6} {'Photocatalyst':<38} {'Ni-Ligand':<16} {'Base':<12} {'Sources'}")
print("-"*100)
for rank, idx in enumerate(disp_order):
    e = experiments[idx]
    src = f"PC:{e['PC_source']}  Lig:{e['Lig_source']}  Base:{e['Base_source']}"
    print(f"{rank+1:<5} {e['Well']:<6} {e['Photocatalyst']:<38} {e['Ni-Ligand']:<16} {e['Base']:<12} {src}")

print()
print("Fixed for ALL wells:")
print("  Ni source : NiBr₂·dme (kit #21), 10 mol%")
print("  Solvent   : DMA (kit #66), 0.1 M, 100 µL total volume")
print("  Electrophile : N-Cbz-4-bromopiperidine (BrC1CCN(CC1)C(=O)OCc2ccccc2), 1.0 equiv, 10 µmol")
print("  Acid      : N-Boc-spiro amino acid (CC(C)(C)OC(=O)N1CC2(CC2)CC1C(=O)O), 1.5 equiv")
print("  Base stoich: 2.0 equiv")
print("  Light     : 470 nm, room temperature, 16 h, N₂ atmosphere")
print("  PC loading: 1 mol%")
print("  Analysis  : UPLC, relative conversion = (product area)/(product+SM areas) × 100%")
