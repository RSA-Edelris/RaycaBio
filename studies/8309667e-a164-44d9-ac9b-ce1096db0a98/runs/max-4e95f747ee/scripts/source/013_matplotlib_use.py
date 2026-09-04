
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def make_scheme_2row(row1, row2, title, filename):
    """
    row1, row2: lists of step dicts (same format as make_scheme).
    Steps in row1 flow left→right, then an arrow drops to row2 which continues left→right.
    """
    n1, n2 = len(row1), len(row2)
    n_max  = max(n1, n2)
    STEP_W = 5.2
    PAD    = 1.0
    fig_w  = n_max * STEP_W + PAD
    fig_h  = 9.5          # tall enough for two rows + connector

    total_slots1 = 2 * n1 + 1
    total_slots2 = 2 * n2 + 1
    slot_w1 = 1.0 / (2 * n_max + 1)   # uniform slot width
    slot_w2 = slot_w1

    y_top = 0.76    # centre of top row
    y_bot = 0.30    # centre of bottom row
    box_h = 0.15
    box_w = slot_w1 * 0.82

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')
    ax.text(0.5, 0.97, title, ha='center', va='top', fontsize=10.5,
            fontweight='bold', fontfamily='DejaVu Sans', multialignment='center')

    FS_BOX=8.0; FS_A=7.6; FS_B=7.0; FS_W=6.6; FS_P=6.8

    def cbox(cx, cy, lines, color, price=None):
        bx, by = cx - box_w/2, cy - box_h/2
        ax.add_patch(mpatches.FancyBboxPatch((bx, by), box_w, box_h,
            boxstyle="round,pad=0.010", lw=1.2,
            edgecolor='#3a7abf', facecolor=color, zorder=3))
        ax.text(cx, cy+0.005, '\n'.join(lines), ha='center', va='center',
                fontsize=FS_BOX, fontfamily='DejaVu Sans',
                multialignment='center', linespacing=1.35, zorder=4)
        if price:
            ax.text(cx, by-0.020, price, ha='center', va='top',
                    fontsize=FS_P, color='#666', fontstyle='italic', zorder=4)

    def harrow(x1, x2, y, reagents, cond, yld, warn=None):
        mx = (x1+x2)/2
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=1.8, mutation_scale=18), zorder=5)
        # reagents above, with gap proportional to box_h
        above_y = y + box_h/2 + 0.09
        ax.text(mx, above_y, '\n'.join(reagents), ha='center', va='bottom',
                fontsize=FS_A, multialignment='center', linespacing=1.3,
                fontfamily='DejaVu Sans', zorder=5)
        below_y = y - box_h/2 - 0.05
        ax.text(mx, below_y, cond+('\n'+yld if yld else ''),
                ha='center', va='top', fontsize=FS_B, color='#444',
                multialignment='center', linespacing=1.3,
                fontfamily='DejaVu Sans', zorder=5)
        if warn:
            ax.text(mx, below_y - 0.08, warn, ha='center', va='top',
                    fontsize=FS_W, color='#c0392b', zorder=5)

    def draw_row(steps, y_mid, start_slot=0):
        for i, s in enumerate(steps):
            si = start_slot + i
            cs = 2*si; ps = 2*si+2
            cx=(cs+0.5)*slot_w1; x1=(cs+1)*slot_w1
            x2=(2*si+2)*slot_w1; px=(ps+0.5)*slot_w1
            cbox(cx, y_mid, s['sm_lines'],
                 '#DFF0D8' if (i==0 and start_slot==0) else '#E8F4FD',
                 s.get('sm_price'))
            harrow(x1, x2, y_mid, s['reagents'],
                   s.get('conditions',''), s.get('yield_str',''), s.get('warning'))
            if i == len(steps)-1:
                cbox(px, y_mid, s['product_lines'], '#E8F4FD' if start_slot==0 else '#FFF3CD',
                     s.get('product_price'))
        return (2*(start_slot+len(steps)-1)+2+0.5)*slot_w1  # x of last product box

    # draw row 1
    last_x = draw_row(row1, y_top, start_slot=0)
    # draw row 2
    draw_row(row2, y_bot, start_slot=0)

    # connector: vertical arrow from end of row1 down to start of row2,
    # then horizontal line to slot 0 of row2
    x_drop  = last_x
    x_start2 = (0 + 0.5)*slot_w1  # centre of first box in row2 ... actually we need to reach x1 of first arrow
    # drop vertically from (last_x, y_top) to (last_x, y_bot)
    ax.annotate('', xy=(last_x, y_bot + box_h/2 + 0.03),
                xytext=(last_x, y_top - box_h/2 - 0.03),
                arrowprops=dict(arrowstyle='->', color='#555',
                               lw=1.4, mutation_scale=14,
                               connectionstyle='arc3,rad=0'), zorder=5)
    # horizontal line from (last_x, y_bot+something) back left to (slot_w1*0.5, y_bot)
    ax.annotate('', xy=(slot_w1*0.5 - box_w/2 - 0.01, y_bot),
                xytext=(last_x, y_bot),
                arrowprops=dict(arrowstyle='->', color='#555',
                               lw=1.4, mutation_scale=14), zorder=5)

    ax.axhline(y_top, xmin=0.01, xmax=0.99, color='#eee', lw=0.4, zorder=1)
    ax.axhline(y_bot, xmin=0.01, xmax=0.99, color='#eee', lw=0.4, zorder=1)
    # row labels
    ax.text(0.005, y_top+box_h/2+0.14, 'Steps 1–3', va='bottom', ha='left',
            fontsize=7, color='#888', fontfamily='DejaVu Sans')
    ax.text(0.005, y_bot+box_h/2+0.14, 'Steps 4–6', va='bottom', ha='left',
            fontsize=7, color='#888', fontfamily='DejaVu Sans')

    plt.tight_layout(rect=[0,0,1,0.95])
    path = f"{OUT}/{filename}"
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {path}")

make_scheme_2row(
    row1=[
        dict(sm_lines=['Ethyl nicotinate'], sm_price='€0.60/g',
             reagents=['[Rh(cod)Cl]₂ (€800/g, 0.5 mol%)', '(R)-BINAP (€500/g, 1 mol%)'],
             conditions='AcOH/MeOH, H₂ 50 bar, 60 °C', yield_str='55–65%, ee ~88%',
             warning='⚠ autoclave required',
             product_lines=['Ethyl (R)-nipecotate', '[C1]']),
        dict(sm_lines=['[C1]'],
             reagents=['NaOH (2 eq)'],
             conditions='EtOH/H₂O, rt, 2 h', yield_str='98%',
             product_lines=['(R)-Nipecotic acid', '[C2]']),
        dict(sm_lines=['[C2]'],
             reagents=['Boc₂O (€5/g, 1.1 eq)', 'NaOH (1 eq)'],
             conditions='THF/H₂O, rt, 12 h', yield_str='92%',
             product_lines=['N-Boc acid', '[C3]']),
    ],
    row2=[
        dict(sm_lines=['[C3]  +  2-Amino-5,6-F₂-', 'benzothiazole'],
             sm_price='€90/g',
             reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
             conditions='DMF, rt, 12 h', yield_str='72%',
             product_lines=['N-Boc amide', '[C4]']),
        dict(sm_lines=['[C4]'],
             reagents=['TFA (€5/g, 20 eq)'],
             conditions='DCM, rt, 1 h', yield_str='95%',
             product_lines=['Free NH amide', '[C5]']),
        dict(sm_lines=['[C5]  +  2-(DMAE)Cl·HCl'],
             sm_price='€25/g',
             reagents=['K₂CO₃ (€1/g)'],
             conditions='MeCN, 80 °C, 8 h', yield_str='63%',
             product_lines=['MCUF651']),
    ],
    title='MCUF651 — Route C\nAsymmetric hydrogenation (de novo stereocentre)  (6 steps, ~20% overall)',
    filename='mcuf651_C_v3.png'
)
print("done")
