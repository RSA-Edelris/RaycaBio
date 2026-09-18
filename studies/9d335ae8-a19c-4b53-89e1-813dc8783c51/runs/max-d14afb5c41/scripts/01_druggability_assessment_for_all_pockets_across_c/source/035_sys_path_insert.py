
import sys, os
sys.path.insert(0, '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap

# ---- Druggability scoring (0-10 composite) ----
# Volume score (hull Cα proxy): <500=1, 500-1500=2, 1500-4000=3, >4000=4  (max 4)
# Hydrophobicity:  <0.25=0, 0.25-0.40=1, 0.40-0.50=2, >0.50=3            (max 3)
# Aromatic content: <0.05=0, 0.05-0.12=1, >0.12=2                         (max 2)
# Literature/experimental confirmation: none=0, leads=1, clinical=3        (max 3)
# Total max = 12 → normalize to 10

lit_scores = {
    'Main (thalidomide/IMiD)':       3,   # lenalidomide, pomalidomide FDA-approved
    'Allosteric (zinc shell)':        0,   # no confirmed SM binders
    'ATP-binding':                    3,   # hundreds of clinical CDK2 inhibitors
    'T-loop allosteric':              1,   # ANS-site fragments reported, no drugs
    'CDK2–CyclinE1 interface (apo)':  1,   # PPI leads in literature
    'CTX binding (interface)':        2,   # CTX itself; class validated
}

def score_pocket(d, lit):
    vol = d['vol_hull']
    v  = 1 if vol < 500 else (2 if vol < 1500 else (3 if vol < 4000 else 4))
    h  = 0 if d['f_hydro'] < 0.25 else (1 if d['f_hydro'] < 0.40 else (2 if d['f_hydro'] < 0.50 else 3))
    ar = 0 if d['f_arom'] < 0.05 else (1 if d['f_arom'] < 0.12 else 2)
    raw = v + h + ar + lit
    return round(raw / 12 * 10, 1)

verdicts = {
    'Main (thalidomide/IMiD)':       ('Highly druggable',   '#27ae60'),
    'Allosteric (zinc shell)':        ('Challenging',        '#c0392b'),
    'ATP-binding':                    ('Highly druggable',   '#27ae60'),
    'T-loop allosteric':              ('Moderately druggable','#f39c12'),
    'CDK2–CyclinE1 interface (apo)':  ('Moderately druggable','#f39c12'),
    'CTX binding (interface)':        ('Druggable',          '#2980b9'),
}

rows = []
for d in results:
    lit  = lit_scores[d['pocket']]
    scr  = score_pocket(d, lit)
    verd, vcol = verdicts[d['pocket']]
    rows.append({**d, 'score': scr, 'verdict': verd, 'vcol': vcol, 'lit': lit})

# ---- Figure: horizontal bar chart + table ----
BG = '#1a1a2e'
fig = plt.figure(figsize=(14, 7), facecolor=BG)
gs  = fig.add_gridspec(1, 2, width_ratios=[1, 1.4], wspace=0.05)
ax_bar  = fig.add_subplot(gs[0])
ax_tbl  = fig.add_subplot(gs[1])
for ax in [ax_bar, ax_tbl]:
    ax.set_facecolor(BG)

labels   = [f"{r['target']}\n{r['pocket']}" for r in rows]
scores   = [r['score'] for r in rows]
colors   = [r['vcol']  for r in rows]

y_pos = np.arange(len(rows))
bars = ax_bar.barh(y_pos, scores, color=colors, height=0.6, edgecolor='none')
ax_bar.set_xlim(0, 10)
ax_bar.set_yticks(y_pos)
ax_bar.set_yticklabels(labels, color='white', fontsize=8.5)
ax_bar.set_xlabel('Druggability score (0–10)', color='#aaaacc', fontsize=9)
ax_bar.tick_params(axis='x', colors='#888899')
ax_bar.axvline(5, color='#ffffff22', lw=1, ls='--')
ax_bar.axvline(7, color='#ffffff33', lw=1, ls='--')
for sp in ax_bar.spines.values(): sp.set_color('#333355')
for i, (bar, scr) in enumerate(zip(bars, scores)):
    ax_bar.text(scr + 0.15, i, f'{scr}', va='center', color='white', fontsize=9, fontweight='bold')
ax_bar.set_title('Druggability score', color='white', fontsize=10, pad=6)
ax_bar.invert_yaxis()

# Table
ax_tbl.axis('off')
col_labels = ['Target', 'Pocket', 'n', 'Vol\n(Å³)', 'Hydro', 'Arom', 'Score', 'Verdict']
table_data = []
for r in rows:
    table_data.append([
        r['target'].replace('–','-'),
        r['pocket'],
        str(r['n_res']),
        f"{r['vol_hull']:.0f}",
        f"{r['f_hydro']:.2f}",
        f"{r['f_arom']:.2f}",
        f"{r['score']}",
        r['verdict']
    ])

tbl = ax_tbl.table(cellText=table_data, colLabels=col_labels,
                   loc='center', cellLoc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)
tbl.scale(1, 1.65)

for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#2c2c4e')
        cell.set_text_props(color='white', fontweight='bold')
    else:
        verdict_col = rows[row-1]['vcol']
        if col == 7:
            cell.set_facecolor(verdict_col + '55')
            cell.set_text_props(color='white', fontsize=7.5)
        else:
            cell.set_facecolor('#111130' if row % 2 == 0 else '#1a1a3a')
            cell.set_text_props(color='#ddddee')
    cell.set_edgecolor('#333355')

legend_elems = [
    mpatches.Patch(color='#27ae60', label='Highly druggable  (score ≥ 8)'),
    mpatches.Patch(color='#2980b9', label='Druggable  (6–8)'),
    mpatches.Patch(color='#f39c12', label='Moderately druggable  (4–6)'),
    mpatches.Patch(color='#c0392b', label='Challenging  (< 4)'),
]
ax_tbl.legend(handles=legend_elems, loc='lower center', framealpha=0.2,
              labelcolor='white', fontsize=8, facecolor='#111122',
              edgecolor='#444466', ncol=2, bbox_to_anchor=(0.5, -0.02))

fig.suptitle('Pocket Druggability Assessment — CRBN, dpCDK2–CyclinE1, CDK2–CCNE',
             color='white', fontsize=12, y=1.01)

out = '/home/ubuntu/rayca-sessions/9d335ae8-a19c-4b53-89e1-813dc8783c51-0e2dd53329c8/druggability_all_pockets.png'
plt.tight_layout()
plt.savefig(out, dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()
print("Saved:", out, os.path.getsize(out), "bytes")
for r in rows:
    print(f"  {r['score']:4.1f}  {r['verdict']:25s}  {r['target']:25s}  {r['pocket']}")
