
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

STEP_W = 5.2   # inches per step
PAD    = 1.0   # left+right margin

def make_scheme(steps, title, filename):
    n = len(steps)
    fig_w = n * STEP_W + PAD
    fig_h = 6.0

    total_slots = 2 * n + 1
    slot_w = 1.0 / total_slots
    y_mid  = 0.46
    box_h  = 0.22
    box_w  = slot_w * 0.86

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')

    # title — two lines max
    ax.text(0.5, 0.97, title, ha='center', va='top',
            fontsize=10.5, fontweight='bold',
            fontfamily='DejaVu Sans', multialignment='center')

    FS_BOX   = 8.2
    FS_ABOVE = 7.8
    FS_BELOW = 7.2
    FS_WARN  = 6.8
    FS_PRICE = 7.0

    def cbox(cx, lines, color, price=None):
        bx, by = cx - box_w/2, y_mid - box_h/2
        ax.add_patch(mpatches.FancyBboxPatch(
            (bx, by), box_w, box_h,
            boxstyle="round,pad=0.012", lw=1.2,
            edgecolor='#3a7abf', facecolor=color, zorder=3))
        ax.text(cx, y_mid + 0.01, '\n'.join(lines),
                ha='center', va='center', fontsize=FS_BOX,
                fontfamily='DejaVu Sans', multialignment='center',
                linespacing=1.4, zorder=4)
        if price:
            ax.text(cx, by - 0.028, price, ha='center', va='top',
                    fontsize=FS_PRICE, color='#666',
                    fontstyle='italic', zorder=4)

    def arrow(x1, x2, reagents, cond, yld, warn=None):
        mx = (x1 + x2) / 2
        ax.annotate('', xy=(x2, y_mid), xytext=(x1, y_mid),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=1.8, mutation_scale=18), zorder=5)
        ax.text(mx, y_mid + 0.24, '\n'.join(reagents),
                ha='center', va='bottom', fontsize=FS_ABOVE,
                multialignment='center', linespacing=1.35,
                fontfamily='DejaVu Sans', zorder=5)
        below = cond + ('\n' + yld if yld else '')
        ax.text(mx, y_mid - 0.17, below,
                ha='center', va='top', fontsize=FS_BELOW,
                color='#444', multialignment='center',
                linespacing=1.3, fontfamily='DejaVu Sans', zorder=5)
        if warn:
            ax.text(mx, y_mid - 0.31, warn,
                    ha='center', va='top', fontsize=FS_WARN,
                    color='#c0392b', zorder=5)

    for i, s in enumerate(steps):
        cs, ps = 2*i, 2*i+2
        cx = (cs + 0.5) * slot_w
        x1 = (cs + 1)   * slot_w
        x2 = (2*i + 2)  * slot_w
        px = (ps + 0.5)  * slot_w
        cbox(cx, s['sm_lines'],
             '#DFF0D8' if i == 0 else '#E8F4FD', s.get('sm_price'))
        arrow(x1, x2, s['reagents'],
              s.get('conditions', ''), s.get('yield_str', ''),
              s.get('warning'))
        if i == len(steps) - 1:
            cbox(px, s['product_lines'], '#FFF3CD', s.get('product_price'))

    ax.axhline(y_mid, xmin=0.01, xmax=0.99, color='#e0e0e0', lw=0.5, zorder=1)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path = f"{OUT}/{filename}"
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {path}  ({fig_w:.1f} x {fig_h:.1f} in)")

# ── MCUF651 ──────────────────────────────────────────────────────────────────
make_scheme([
    dict(sm_lines=['(R)-Nipecotic acid', '+',
                   '2-Amino-5,6-difluoro-', 'benzothiazole'],
         sm_price='€45/g + €90/g',
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, 0 °C → rt, 12 h', yield_str='72%',
         product_lines=['(R)-N-(5,6-Difluorobenzothiazol-', '2-yl)nipecotamide  [A1]']),
    dict(sm_lines=['[A1]', '+', '2-(Dimethylamino)-', 'ethyl chloride·HCl'],
         sm_price='€25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='MeCN, 80 °C, 8 h', yield_str='63%',
         product_lines=['MCUF651']),
], 'MCUF651 — Route A\nAmide coupling → N-alkylation  (2 steps, ~45% overall)',
   'mcuf651_A_v2.png')

make_scheme([
    dict(sm_lines=['(R)-Nipecotic acid', '+', '2-(DMAE)Cl·HCl'],
         sm_price='€45/g + €25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='DMF, 70 °C, 8 h', yield_str='68%',
         product_lines=['N-Alkylated acid  [B1]']),
    dict(sm_lines=['[B1]'],
         reagents=['CDI (€20/g, 1.2 eq)', 'then 35% aq. NH₃'],
         conditions='THF, 0 °C → rt; 30 min', yield_str='70%',
         product_lines=['Primary amide  [B2]']),
    dict(sm_lines=['[B2]', '+', '2-Cl-5,6-F₂-benzothiazole'],
         sm_price='€120–200/g ⚠',
         reagents=['Pd₂(dba)₃ (€250/g, 2 mol%)',
                   'XantPhos (€120/g, 4 mol%)', 'Cs₂CO₃ (€15/g)'],
         conditions='Toluene, 100 °C, 16 h, N₂', yield_str='55%',
         warning='⚠ SM may exceed €150/g',
         product_lines=['MCUF651']),
], 'MCUF651 — Route B\nN-alkylation → CDI amide → Buchwald C–N arylation  (3 steps, ~26% overall)',
   'mcuf651_B_v2.png')

make_scheme([
    dict(sm_lines=['Ethyl nicotinate'],
         sm_price='€0.60/g',
         reagents=['[Rh(cod)Cl]₂ (€800/g, 0.5 mol%)',
                   '(R)-BINAP (€500/g, 1 mol%)'],
         conditions='AcOH/MeOH, H₂ 50 bar, 60 °C', yield_str='55–65%, ee ~88%',
         warning='⚠ autoclave required',
         product_lines=['Ethyl (R)-nipecotate  [C1]']),
    dict(sm_lines=['[C1]'],
         reagents=['NaOH (2 eq)'],
         conditions='EtOH/H₂O, rt, 2 h', yield_str='98%',
         product_lines=['(R)-Nipecotic acid  [C2]']),
    dict(sm_lines=['[C2]'],
         reagents=['Boc₂O (€5/g, 1.1 eq)', 'NaOH (1 eq)'],
         conditions='THF/H₂O, rt, 12 h', yield_str='92%',
         product_lines=['N-Boc acid  [C3]']),
    dict(sm_lines=['[C3]', '+', '2-Amino-5,6-F₂-benzothiazole'],
         sm_price='€90/g',
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='72%',
         product_lines=['N-Boc amide  [C4]']),
    dict(sm_lines=['[C4]'],
         reagents=['TFA (€5/g, 20 eq)'],
         conditions='DCM, rt, 1 h', yield_str='95%',
         product_lines=['Free NH amide  [C5]']),
    dict(sm_lines=['[C5]', '+', '2-(DMAE)Cl·HCl'],
         sm_price='€25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='MeCN, 80 °C, 8 h', yield_str='63%',
         product_lines=['MCUF651']),
], 'MCUF651 — Route C\nAsymmetric hydrogenation (de novo stereocentre)  (6 steps, ~20% overall)',
   'mcuf651_C_v2.png')

print("MCUF651 v2 done")
