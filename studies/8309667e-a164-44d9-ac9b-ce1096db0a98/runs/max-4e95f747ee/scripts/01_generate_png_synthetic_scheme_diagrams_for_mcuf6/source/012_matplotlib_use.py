
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

# ── 7977 ─────────────────────────────────────────────────────────────────────
make_scheme([
    dict(sm_lines=['2-Amino-4-bromo-5-methyl-', 'pyrimidine  +',
                   '3-Bromo-2-nitropyridine'],
         sm_price='€75/g  +  €40/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 100 °C, 8 h', yield_str='60%',
         product_lines=['SNAr diarylamine', '(2 × Br intact)  [A1]']),
    dict(sm_lines=['[A1]'],
         reagents=['Fe (€2/g, 3 eq)', 'AcOH/EtOH (1:3)'],
         conditions='80 °C, 2 h', yield_str='85%',
         product_lines=['Diamine', '(Br on pyrimidine intact)  [A2]']),
    dict(sm_lines=['[A2]'],
         reagents=['CDI (€20/g, 1.2 eq)'],
         conditions='THF, rt → 60 °C', yield_str='70%',
         product_lines=['Bicyclic N-H uracil', '(Br intact)  [A3]']),
    dict(sm_lines=['[A3]  +', '(2-Cl-4-F-phenyl)-', 'boronic acid'],
         sm_price='€50/g',
         reagents=['Pd(PPh₃)₄ (€150/g, 5 mol%)', 'K₂CO₃ (€1/g)'],
         conditions='Dioxane/H₂O (3:1), 80 °C', yield_str='72%',
         product_lines=['Arylated N-H bicycle  [A4]']),
    dict(sm_lines=['[A4]  +  Chloroacetamide'],
         sm_price='€5/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 60 °C, 6 h', yield_str='65%',
         product_lines=['7977']),
], '7977 — Route A\nSNAr → nitro reduction → CDI cyclisation → Suzuki → N-alkylation  (5 steps, ~19% overall)',
   '7977_A_v2.png')

make_scheme([
    dict(sm_lines=['2-Amino-4-bromo-5-methyl-', 'pyrimidine  +',
                   '3-Bromo-2-nitropyridine'],
         sm_price='€75/g  +  €40/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 100 °C, 8 h', yield_str='60%',
         product_lines=['SNAr diarylamine  [B1]']),
    dict(sm_lines=['[B1]  +', '(2-Cl-4-F-phenyl)-', 'boronic acid'],
         sm_price='€50/g',
         reagents=['Pd(PPh₃)₄ (€150/g, 5 mol%)', 'K₂CO₃ (€1/g)'],
         conditions='Dioxane/H₂O (3:1), 80 °C', yield_str='75%',
         product_lines=['Arylated diarylamine', '(NO₂ intact)  [B2]']),
    dict(sm_lines=['[B2]'],
         reagents=['Fe (€2/g, 3 eq)', 'AcOH/EtOH (1:3)'],
         conditions='80 °C, 2 h', yield_str='85%',
         product_lines=['Arylated diamine  [B3]']),
    dict(sm_lines=['[B3]'],
         reagents=['CDI (€20/g, 1.2 eq)'],
         conditions='THF, rt → 60 °C', yield_str='70%',
         product_lines=['Arylated N-H bicycle  [B4]']),
    dict(sm_lines=['[B4]  +  Chloroacetamide'],
         sm_price='€5/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 60 °C, 6 h', yield_str='65%',
         product_lines=['7977']),
], '7977 — Route B  ★ RECOMMENDED\nSNAr → Suzuki → nitro reduction → CDI cyclisation → N-alkylation  (5 steps, ~22% overall)',
   '7977_B_v2.png')

make_scheme([
    dict(sm_lines=['2,4-Dibromo-5-methyl-', 'pyrimidine  +',
                   '(2-Cl-4-F-Ph) boronic acid'],
         sm_price='€90/g  +  €50/g',
         reagents=['Pd(dppf)Cl₂ (€200/g, 2 mol%)', 'K₂CO₃ (€1/g)'],
         conditions='Dioxane/H₂O, 80 °C', yield_str='65%',
         product_lines=['2-Bromo-5-Me-4-(2-Cl-4-F-Ph)-', 'pyrimidine  [C1]']),
    dict(sm_lines=['7-Azaindole'],
         sm_price='€35/g',
         reagents=['Triphosgene (€25/g, 0.35 eq)', 'Pyridine (3 eq)'],
         conditions='DCM, 0 °C → rt', yield_str='55%',
         warning='⚠ EXTRAPOLATION',
         product_lines=['N-H bicyclic uracil', 'scaffold  [C2]']),
    dict(sm_lines=['[C2]  +  [C1]'],
         reagents=['CuI (€15/g, 10 mol%)',
                   'trans-DACH (€10/g, 20 mol%)', 'K₃PO₄ (€2/g)'],
         conditions='DMSO, 110 °C, 24 h', yield_str='50%',
         warning='⚠ EXTRAPOLATION — check N1/N3 regio',
         product_lines=['N1-Arylated bicycle  [C3]']),
    dict(sm_lines=['[C3]  +  Chloroacetamide'],
         sm_price='€5/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 60 °C, 6 h', yield_str='65%',
         product_lines=['7977']),
], '7977 — Route C\nMono-Suzuki on dibromopyrimidine (parallel) + 7-azaindole scaffold + Cu-Ullmann  (4 steps, ~13% overall)',
   '7977_C_v2.png')

print("7977 v2 done")
