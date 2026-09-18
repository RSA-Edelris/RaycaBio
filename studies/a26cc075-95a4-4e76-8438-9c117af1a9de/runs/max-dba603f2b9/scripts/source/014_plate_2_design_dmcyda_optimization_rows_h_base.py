
import pandas as pd
import numpy as np

# ── Plate 2 design: DMCyDA optimization ──────────────────────────────────────
# Rows A-H = Base × Solvent (8 combos; 4 bases, 4 solvents covering known + new)
# Cols 1-12 = Cu source × loading (6 Cu sources × 2 loadings)

ROWS_DESIGN = [
    ('A', 'K2CO3',  'Dioxane'),   # ← best base+solvent from screen 1 (CONTROL)
    ('B', 'K2CO3',  'DMF'),       # ← screen 1 control
    ('C', 'Cs2CO3', 'Dioxane'),   # NEW base - stronger, more soluble
    ('D', 'Cs2CO3', 'DMF'),       # NEW base × new solvent pairing
    ('E', 'K3PO4',  'Dioxane'),   # ← screen 1 control
    ('F', 'K3PO4',  'DMF'),       # ← re-run of anomalous F9 zone
    ('G', 'K2CO3',  'DMSO'),      # NEW solvent - excellent Cu solvation
    ('H', 'K2CO3',  'MeCN'),      # NEW solvent - polar aprotic contrast
]

COLS_DESIGN = [
    (1,  'CuI',        5),
    (2,  'CuI',       10),
    (3,  'Cu(OTf)2',   5),
    (4,  'Cu(OTf)2',  10),
    (5,  'CuBr',       5),   # NEW Cu(I) halide
    (6,  'CuBr',      10),
    (7,  'CuCl',       5),   # NEW Cu(I) halide
    (8,  'CuCl',      10),
    (9,  'Cu(OAc)2',   5),   # NEW Cu(II) source
    (10, 'Cu(OAc)2',  10),
    (11, 'Cu2O',       5),   # NEW Cu(I) oxide, air-stable
    (12, 'Cu2O',      10),
]

# Generate the 96 conditions
records = []
rxn_base = 'SCREEN2'
n = 1
for row_lbl, base, solvent in ROWS_DESIGN:
    for col_num, cu, loading in COLS_DESIGN:
        well      = f'{row_lbl}{col_num}'
        rxn_id    = f'{rxn_base}-{n:03d}'
        condition = f'DMCyDA_{base}_{cu}_{loading}mol%_{solvent}'
        records.append({'Reaction': rxn_id, 'Conditions': condition,
                        'Ligand': 'DMCyDA', 'Base': base,
                        'Cu': cu, 'Cu_loading_mol%': loading,
                        'Solvent': solvent, 'Well': well})
        n += 1

plate2_df = pd.DataFrame(records)

# Save
out_csv = '/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/conditions_screen2.csv'
plate2_df.to_csv(out_csv, index=False)
print(f"Saved {len(plate2_df)} conditions → {out_csv}")
print("\nSample (first 16):")
print(plate2_df.head(16).to_string(index=False))
print("\nCu sources:", plate2_df['Cu'].unique().tolist())
print("Bases:",       plate2_df['Base'].unique().tolist())
print("Solvents:",    plate2_df['Solvent'].unique().tolist())
print("Loadings:",    sorted(plate2_df['Cu_loading_mol%'].unique().tolist()))
