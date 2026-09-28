
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# ── Read data ──────────────────────────────────────────────────────────────────
conditions = pd.read_csv(
    '/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/conditions.csv',
    header=None, names=['ID', 'Condition'])

results = pd.read_csv(
    '/home/ubuntu/rayca-artifacts/ab6ab3d3a46e0d2cc39a9030/files/results.csv')

df = results.merge(conditions, on='ID')

# IS-normalised yield
df['norm_yield'] = (df['Area Abs DP'] / df['Area Abs IS']).fillna(0)

# Parse condition string: Ligand_Base_Cu_Solvent
def parse_condition(cond):
    parts = cond.split('_')
    for i, p in enumerate(parts):
        if p in ('K3PO4', 'K2CO3'):
            base_idx = i
            break
    return ('_'.join(parts[:base_idx]), parts[base_idx], parts[base_idx+1], parts[base_idx+2])

df[['Ligand','Base','Cu','Solvent']] = df['Condition'].apply(lambda x: pd.Series(parse_condition(x)))

# Map to 96-well plate (row-major)
well_num = df['ID'].str.extract(r'-(\d+)$').astype(int)[0]
df['row_idx'] = (well_num - 1) // 12
df['col_idx'] = (well_num - 1) % 12 + 1
df['plate_row'] = df['row_idx'].map(lambda i: 'ABCDEFGH'[i])

# Print top conditions
top = df.nlargest(10, 'norm_yield')[['ID','Condition','norm_yield']].reset_index(drop=True)
print("Top 10 conditions (IS-normalised DP/IS ratio):")
print(top.to_string())
print(f"\nBest: {df.loc[df['norm_yield'].idxmax(),'Condition']}")
print(f"Norm yield: {df['norm_yield'].max():.4f}")
