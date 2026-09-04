
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

STEP_W = 5.2
PAD    = 1.0

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
    ax.text(0.5, 0.97, title, ha='center', va='top', fontsize=10.5,
            fontweight='bold', fontfamily='DejaVu Sans', multialignment='center')

    def cbox(cx, lines, color, price=None):
        bx, by = cx - box_w/2, y_mid - box_h/2
        ax.add_patch(mpatches.FancyBboxPatch((bx, by), box_w, box_h,
            boxstyle="round,pad=0.012", lw=1.2,
            edgecolor='#3a7abf', facecolor=color, zorder=3))
        ax.text(cx, y_mid+0.01, '\n'.join(lines), ha='center', va='center',
                fontsize=8.2, fontfamily='DejaVu Sans', multialignment='center',
                linespacing=1.4, zorder=4)
        if price:
            ax.text(cx, by-0.028, price, ha='center', va='top',
                    fontsize=7.0, color='#666', fontstyle='italic', zorder=4)

    def arrow(x1, x2, reagents, cond, yld, warn=None):
        mx = (x1+x2)/2
        ax.annotate('', xy=(x2, y_mid), xytext=(x1, y_mid),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=1.8, mutation_scale=18), zorder=5)
        ax.text(mx, y_mid+0.24, '\n'.join(reagents), ha='center', va='bottom',
                fontsize=7.8, multialignment='center', linespacing=1.35,
                fontfamily='DejaVu Sans', zorder=5)
        ax.text(mx, y_mid-0.17, cond+('\n'+yld if yld else ''),
                ha='center', va='top', fontsize=7.2, color='#444',
                multialignment='center', linespacing=1.3,
                fontfamily='DejaVu Sans', zorder=5)
        if warn:
            ax.text(mx, y_mid-0.31, warn, ha='center', va='top',
                    fontsize=6.8, color='#c0392b', zorder=5)

    for i, s in enumerate(steps):
        cs, ps = 2*i, 2*i+2
        cx=(cs+0.5)*slot_w; x1=(cs+1)*slot_w
        x2=(2*i+2)*slot_w;  px=(ps+0.5)*slot_w
        cbox(cx, s['sm_lines'], '#DFF0D8' if i==0 else '#E8F4FD', s.get('sm_price'))
        arrow(x1, x2, s['reagents'], s.get('conditions',''),
              s.get('yield_str',''), s.get('warning'))
        if i == len(steps)-1:
            cbox(px, s['product_lines'], '#FFF3CD', s.get('product_price'))

    ax.axhline(y_mid, xmin=0.01, xmax=0.99, color='#e0e0e0', lw=0.5, zorder=1)
    plt.tight_layout(rect=[0,0,1,0.94])
    path = f"{OUT}/{filename}"
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {path}  ({fig_w:.1f} x {fig_h:.1f} in)")

# ── A317 ─────────────────────────────────────────────────────────────────────
make_scheme([
    dict(sm_lines=['(S)-2-Acetylpyrrolidine', '+', '2-Bromopyridine'],
         sm_price='€130/g + €15/g',
         reagents=['Pd₂(dba)₃ (€250/g, 2 mol%)',
                   '(±)-BINAP (€500/g, 4 mol%)', 'Cs₂CO₃ (€15/g)'],
         conditions='Toluene, 90 °C, 12 h', yield_str='65%',
         product_lines=['(S)-2-Acetyl-1-(pyridin-2-yl)-', 'pyrrolidine  [A1]']),
    dict(sm_lines=['[A1]'],
         reagents=['NBS (€5/g, 1.05 eq)'],
         conditions='CHCl₃, 0 °C → rt, 2 h', yield_str='70%',
         warning='⚠ use immediately',
         product_lines=['α-Bromoketone  [A2]']),
    dict(sm_lines=['[A2]  +  Thiourea'],
         sm_price='€1/g',
         reagents=['EtOH, reflux, 1 h', 'then K₂CO₃ (€1/g)'],
         conditions='free base workup', yield_str='62%',
         product_lines=['2-Aminothiazole  [A3]']),
    dict(sm_lines=['[A3]  +', '1-(4-Picolyl)pyrrole-', '2-carboxylic acid *'],
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='55%',
         product_lines=['A317']),
], 'A317 — Route A\nBuchwald N-arylation → α-bromination → Hantzsch → amide  (4 steps, ~16% overall)\n*Parallel: pyrrole-2-COOH (€35/g) + 4-picolyl chloride·HCl (€30/g), K₂CO₃, DMF, 60 °C, 70%',
   'a317_A_v2.png')

make_scheme([
    dict(sm_lines=['(S)-2-Acetylpyrrolidine'],
         sm_price='€130/g',
         reagents=['NBS (€5/g, 1.05 eq)'],
         conditions='CHCl₃, −10 °C, 1 h', yield_str='68%',
         warning='⚠ use immediately',
         product_lines=['α-Bromoketone  [B1]', '(free pyrrolidine NH)']),
    dict(sm_lines=['[B1]  +  Thiourea'],
         sm_price='€1/g',
         reagents=['EtOH, reflux, 45 min', 'then K₂CO₃ (€1/g)'],
         conditions='free base workup', yield_str='58%',
         product_lines=['2-Aminothiazole  [B2]', '(free pyrrolidine NH)']),
    dict(sm_lines=['[B2]  +', '1-(4-Picolyl)pyrrole-', '2-carboxylic acid *'],
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='50%',
         product_lines=['Amide  [B3]', '(free pyrrolidine NH)']),
    dict(sm_lines=['[B3]  +  2-Fluoropyridine'],
         sm_price='€25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='DMSO, 130 °C, 16 h', yield_str='50%',
         warning='⚠ monitor ee — epimerisation risk',
         product_lines=['A317']),
], 'A317 — Route B  (Pd-free)\nα-bromination → Hantzsch → amide → SNAr N-arylation  (4 steps, ~16% overall)\n*Parallel: pyrrole-2-COOH (€35/g) + 4-picolyl chloride·HCl (€30/g), K₂CO₃, DMF, 60 °C, 70%',
   'a317_B_v2.png')

make_scheme([
    dict(sm_lines=['2-Amino-4-bromothiazole', '+',
                   '1-(4-Picolyl)pyrrole-', '2-carboxylic acid *'],
         sm_price='€60/g  (*see parallel)',
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='65%',
         product_lines=['N-(4-Bromothiazol-2-yl)amide  [C1]']),
    dict(sm_lines=['[C1]  +', '(S)-Pyrrolidinyl boronate †'],
         sm_price='(† from N-Boc-L-Pro €35/g + B₂Pin₂ €80/g)',
         reagents=['Pd(PPh₃)₄ (€150/g, 5 mol%)', 'K₂CO₃ (€1/g)'],
         conditions='Dioxane/H₂O, 80 °C, 12 h', yield_str='45%',
         warning='⚠ EXTRAPOLATION — boronate prep needs validation',
         product_lines=['A317']),
], 'A317 — Route C\nAmide on commercial aminobromothiazole → Suzuki  (2 steps + parallel, ~13–18% overall)\n†Boronate: decarboxylative borylation of N-Boc-L-Pro — requires experimental validation',
   'a317_C_v2.png')

print("A317 v2 done")
