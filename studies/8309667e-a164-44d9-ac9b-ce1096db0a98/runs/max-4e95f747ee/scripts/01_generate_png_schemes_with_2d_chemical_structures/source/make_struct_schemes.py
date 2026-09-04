"""
Generate synthetic-scheme PNGs with 2D chemical structure drawings.
Each compound box contains an RDKit-rendered 2D structure instead of text.
Reagents above arrows, conditions/yields below – layout mirrors the v2 text schemes.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image as PILImage
from rdkit import Chem
from rdkit.Chem import Draw, AllChem

OUT = '/home/ubuntu/rayca-sessions/8309667e-a164-44d9-ac9b-ce1096db0a98-90d0a82fa1dd'
STEP_W = 5.2   # inches per step
PAD    = 1.0
FIG_H  = 7.0   # taller than v2 to accommodate structures

# ─── molecule rendering ────────────────────────────────────────────────────────

def _mol_img(smiles, size=(260, 170), bg=(255, 255, 255)):
    """Return numpy array of 2D structure; white box with name if SMILES fails."""
    if smiles is None:
        img = PILImage.new('RGB', size, bg)
        return np.array(img)
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        img = PILImage.new('RGB', size, bg)
        return np.array(img)
    AllChem.Compute2DCoords(mol)
    img = Draw.MolToImage(mol, size=size)
    # Replace the default white (255,255,255) with the requested bg colour
    if bg != (255, 255, 255):
        arr = np.array(img, dtype=np.uint8)
        mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240)
        arr[mask] = bg
        return arr
    return np.array(img)

def _compound_background(step_idx, n_steps):
    """RGB tuple for the compound box fill."""
    if step_idx == 0:
        return (223, 240, 216)   # green  – starting material
    elif step_idx == n_steps:    # last box = final product
        return (255, 243, 205)   # yellow
    else:
        return (232, 244, 253)   # blue   – intermediate

# ─── single-row scheme ────────────────────────────────────────────────────────

def make_struct_scheme(steps, title, filename):
    """
    steps: list of dicts.  Each dict:
      sm     : list of (smiles, label) tuples  –  1 or 2 compounds shown in box
      sm_price: str | None
      reagents: list of str  (above arrow)
      conditions: str
      yield_str: str
      warning  : str | None
      product  : (smiles, label)   ← only on the LAST step
      product_price: str | None
    """
    n = len(steps)
    fig_w = n * STEP_W + PAD
    total_slots = 2 * n + 1
    slot_w = 1.0 / total_slots

    y_mid   = 0.44
    box_h   = 0.38          # taller than text version to hold structure
    box_w   = slot_w * 0.88

    fig, ax = plt.subplots(figsize=(fig_w, FIG_H))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')
    ax.text(0.5, 0.975, title, ha='center', va='top', fontsize=10,
            fontweight='bold', fontfamily='DejaVu Sans',
            multialignment='center')

    def draw_compound_box(cx, compounds, box_idx, price=None):
        """
        compounds: list of (smiles, label) – 1 or 2 entries.
        box_idx  : 0 = green SM, n_steps = yellow product, else blue intermediate.
        """
        bg_rgb = _compound_background(box_idx, n)
        bx, by = cx - box_w / 2, y_mid - box_h / 2
        ax.add_patch(mpatches.FancyBboxPatch(
            (bx, by), box_w, box_h,
            boxstyle='round,pad=0.01', lw=1.2,
            edgecolor='#3a7abf',
            facecolor=tuple(c / 255 for c in bg_rgb),
            zorder=3))

        # Tint background matching box colour for mol rendering
        bg_pil = bg_rgb

        # ── one compound ─────────────────────────────────────────────────────
        if len(compounds) == 1:
            smi, lbl = compounds[0]
            mol_px = (int(box_w * fig_w * 100 * 0.82), int(box_h * FIG_H * 100 * 0.72))
            img = _mol_img(smi, size=mol_px, bg=bg_pil)
            # imshow extent: [x_left, x_right, y_bottom, y_top]
            margin_x = box_w * 0.09
            margin_y = box_h * 0.14
            extent = [bx + margin_x, bx + box_w - margin_x,
                      by + margin_y, by + box_h - margin_y - 0.04]
            ax.imshow(img, extent=extent, aspect='auto', zorder=4, origin='upper')
            # label below structure
            ax.text(cx, by + 0.025, lbl, ha='center', va='bottom',
                    fontsize=7.0, fontfamily='DejaVu Sans',
                    color='#222', zorder=5, multialignment='center',
                    linespacing=1.25)

        # ── two compounds side by side with "+" ───────────────────────────────
        else:
            smi1, lbl1 = compounds[0]
            smi2, lbl2 = compounds[1]
            half = box_w * 0.44
            cx1 = bx + half * 0.5 + box_w * 0.01
            cx2 = bx + box_w - half * 0.5 - box_w * 0.01

            mol_px = (int(half * fig_w * 100 * 0.82), int(box_h * FIG_H * 100 * 0.70))
            for smi, lbl, cxc in [(smi1, lbl1, cx1), (smi2, lbl2, cx2)]:
                img = _mol_img(smi, size=mol_px, bg=bg_pil)
                margin_y = box_h * 0.14
                bx_mol = cxc - half / 2 + box_w * 0.01
                extent = [bx_mol, bx_mol + half - box_w * 0.02,
                          by + margin_y, by + box_h - margin_y - 0.04]
                ax.imshow(img, extent=extent, aspect='auto', zorder=4, origin='upper')
                ax.text(cxc, by + 0.025, lbl, ha='center', va='bottom',
                        fontsize=6.4, fontfamily='DejaVu Sans',
                        color='#222', zorder=5, multialignment='center',
                        linespacing=1.2)

            # "+" in the middle
            ax.text(cx, y_mid, '+', ha='center', va='center',
                    fontsize=10, fontweight='bold', color='#555', zorder=6)

        if price:
            ax.text(cx, by - 0.024, price, ha='center', va='top',
                    fontsize=6.8, color='#666', fontstyle='italic', zorder=5)

    def draw_arrow(x1, x2, reagents, cond, yld, warn=None):
        mx = (x1 + x2) / 2
        ax.annotate('', xy=(x2, y_mid), xytext=(x1, y_mid),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=1.8, mutation_scale=18), zorder=5)
        ax.text(mx, y_mid + 0.24, '\n'.join(reagents),
                ha='center', va='bottom', fontsize=7.4,
                multialignment='center', linespacing=1.3,
                fontfamily='DejaVu Sans', zorder=5)
        below = cond + ('\n' + yld if yld else '')
        ax.text(mx, y_mid - 0.24, below,
                ha='center', va='top', fontsize=7.0, color='#444',
                multialignment='center', linespacing=1.3,
                fontfamily='DejaVu Sans', zorder=5)
        if warn:
            ax.text(mx, y_mid - 0.38, warn,
                    ha='center', va='top', fontsize=6.4,
                    color='#c0392b', zorder=5)

    for i, s in enumerate(steps):
        cs = 2 * i
        cx  = (cs + 0.5) * slot_w
        x1  = (cs + 1)   * slot_w
        x2  = (2 * i + 2) * slot_w
        px  = (2 * i + 2 + 0.5) * slot_w

        draw_compound_box(cx, s['sm'], i, s.get('sm_price'))
        draw_arrow(x1, x2, s['reagents'],
                   s.get('conditions', ''), s.get('yield_str', ''),
                   s.get('warning'))
        if i == n - 1:
            draw_compound_box(px, [s['product']], n, s.get('product_price'))

    ax.axhline(y_mid, xmin=0.01, xmax=0.99,
               color='#e0e0e0', lw=0.5, zorder=1)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    path = f'{OUT}/{filename}'
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f'Saved: {path}  ({fig_w:.1f} × {FIG_H:.1f} in)')


# ─── two-row scheme (MCUF651 Route C) ─────────────────────────────────────────

def make_struct_scheme_2row(row1, row2, title, filename):
    """row1 = steps 1-3; row2 = steps 4-6."""
    n_max = max(len(row1), len(row2))
    fig_w  = n_max * STEP_W + PAD
    fig_h2 = 11.0
    total_slots = 2 * n_max + 1
    slot_w  = 1.0 / total_slots
    y_top   = 0.75
    y_bot   = 0.27
    box_h   = 0.30
    box_w   = slot_w * 0.88

    fig, ax = plt.subplots(figsize=(fig_w, fig_h2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')
    ax.text(0.5, 0.985, title, ha='center', va='top', fontsize=10,
            fontweight='bold', fontfamily='DejaVu Sans',
            multialignment='center')

    n_total = len(row1) + len(row2)

    def draw_box(cx, compounds, box_idx, y_ctr, price=None):
        bg_rgb = _compound_background(box_idx, n_total)
        bx, by = cx - box_w / 2, y_ctr - box_h / 2
        ax.add_patch(mpatches.FancyBboxPatch(
            (bx, by), box_w, box_h,
            boxstyle='round,pad=0.01', lw=1.2,
            edgecolor='#3a7abf',
            facecolor=tuple(c / 255 for c in bg_rgb), zorder=3))
        bg_pil = bg_rgb
        if len(compounds) == 1:
            smi, lbl = compounds[0]
            mol_px = (int(box_w * fig_w * 100 * 0.82),
                      int(box_h * fig_h2 * 100 * 0.72))
            img = _mol_img(smi, size=mol_px, bg=bg_pil)
            mx = box_w * 0.09; my = box_h * 0.14
            extent = [bx + mx, bx + box_w - mx,
                      by + my, by + box_h - my - 0.03]
            ax.imshow(img, extent=extent, aspect='auto', zorder=4, origin='upper')
            ax.text(cx, by + 0.018, lbl, ha='center', va='bottom',
                    fontsize=6.8, fontfamily='DejaVu Sans',
                    color='#222', zorder=5, multialignment='center',
                    linespacing=1.2)
        else:
            smi1, lbl1 = compounds[0]; smi2, lbl2 = compounds[1]
            half = box_w * 0.44
            cx1 = bx + half * 0.5 + box_w * 0.01
            cx2 = bx + box_w - half * 0.5 - box_w * 0.01
            mol_px = (int(half * fig_w * 100 * 0.80),
                      int(box_h * fig_h2 * 100 * 0.68))
            for smi, lbl, cxc in [(smi1, lbl1, cx1), (smi2, lbl2, cx2)]:
                img = _mol_img(smi, size=mol_px, bg=bg_pil)
                my = box_h * 0.14
                bx_mol = cxc - half / 2 + box_w * 0.01
                extent = [bx_mol, bx_mol + half - box_w * 0.02,
                          by + my, by + box_h - my - 0.03]
                ax.imshow(img, extent=extent, aspect='auto', zorder=4, origin='upper')
                ax.text(cxc, by + 0.018, lbl, ha='center', va='bottom',
                        fontsize=6.0, fontfamily='DejaVu Sans',
                        color='#222', zorder=5, multialignment='center')
            ax.text(cx, y_ctr, '+', ha='center', va='center',
                    fontsize=9, fontweight='bold', color='#555', zorder=6)
        if price:
            ax.text(cx, by - 0.020, price, ha='center', va='top',
                    fontsize=6.5, color='#666', fontstyle='italic', zorder=5)

    def draw_arrow_2r(x1, x2, reagents, cond, yld, y_ctr, warn=None):
        mx = (x1 + x2) / 2
        ax.annotate('', xy=(x2, y_ctr), xytext=(x1, y_ctr),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=1.6, mutation_scale=16), zorder=5)
        ax.text(mx, y_ctr + 0.18, '\n'.join(reagents),
                ha='center', va='bottom', fontsize=7.0,
                multialignment='center', linespacing=1.2,
                fontfamily='DejaVu Sans', zorder=5)
        below = cond + ('\n' + yld if yld else '')
        ax.text(mx, y_ctr - 0.18, below,
                ha='center', va='top', fontsize=6.6, color='#444',
                multialignment='center', linespacing=1.2,
                fontfamily='DejaVu Sans', zorder=5)
        if warn:
            ax.text(mx, y_ctr - 0.30, warn, ha='center', va='top',
                    fontsize=6.0, color='#c0392b', zorder=5)

    # ── row 1 ──────────────────────────────────────────────────────────────────
    for i, s in enumerate(row1):
        cs  = 2 * i
        cx  = (cs + 0.5) * slot_w
        x1  = (cs + 1)   * slot_w
        x2  = (2 * i + 2) * slot_w
        px  = (2 * i + 2 + 0.5) * slot_w
        draw_box(cx, s['sm'], i, y_top, s.get('sm_price'))
        draw_arrow_2r(x1, x2, s['reagents'],
                      s.get('conditions', ''), s.get('yield_str', ''), y_top,
                      s.get('warning'))
        if i == len(row1) - 1:
            draw_box(px, [s['product']], len(row1), y_top)

    # ── connecting arrow from end of row1 down to start of row2 ───────────────
    # end of row1 box: x = (2*len(row1)+0.5)*slot_w
    x_end = (2 * len(row1) + 0.5) * slot_w
    x_start_r2 = 0.5 * slot_w
    # vertical line down from (x_end, y_top-box_h/2) to (x_end, (y_top+y_bot)/2)
    ymid_v = (y_top - box_h / 2 + y_bot + box_h / 2) / 2
    ax.plot([x_end, x_end], [y_top - box_h / 2, ymid_v],
            color='#111', lw=1.6, zorder=5)
    # horizontal line from (x_end, ymid_v) to (x_start_r2, ymid_v)
    ax.plot([x_end, x_start_r2], [ymid_v, ymid_v],
            color='#111', lw=1.6, zorder=5)
    # vertical arrow from (x_start_r2, ymid_v) to (x_start_r2, y_bot+box_h/2)
    ax.annotate('', xy=(x_start_r2, y_bot + box_h / 2 + 0.005),
                xytext=(x_start_r2, ymid_v),
                arrowprops=dict(arrowstyle='->', color='#111',
                                lw=1.6, mutation_scale=16), zorder=5)

    # ── row 2 ──────────────────────────────────────────────────────────────────
    n_r1 = len(row1)
    for i, s in enumerate(row2):
        cs  = 2 * i
        cx  = (cs + 0.5) * slot_w
        x1  = (cs + 1)   * slot_w
        x2  = (2 * i + 2) * slot_w
        px  = (2 * i + 2 + 0.5) * slot_w
        draw_box(cx, s['sm'], n_r1 + i, y_bot, s.get('sm_price'))
        draw_arrow_2r(x1, x2, s['reagents'],
                      s.get('conditions', ''), s.get('yield_str', ''), y_bot,
                      s.get('warning'))
        if i == len(row2) - 1:
            draw_box(px, [s['product']], n_r1 + len(row2), y_bot,
                     s.get('product_price'))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = f'{OUT}/{filename}'
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f'Saved: {path}  ({fig_w:.1f} × {fig_h2:.1f} in)')


# ══════════════════════════════════════════════════════════════════════════════
#  SMILES dictionary
# ══════════════════════════════════════════════════════════════════════════════

# MCUF651 compounds
SML = {
    # Targets
    'MCUF651'           : 'CN(C)CCN1CCC[C@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1',
    'A317'              : 'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1',
    '7977'              : 'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21',

    # MCUF651 SMs & intermediates
    'R_nipecotic_acid'  : 'O=C(O)[C@@H]1CCCNC1',
    'amino_F2_BT'       : 'Nc1nc2c(F)cc(F)cc2s1',
    'DMAE_Cl'           : 'ClCCN(C)C',
    'amide_A1'          : 'O=C(Nc1nc2c(F)cc(F)cc2s1)[C@@H]1CCCNC1',
    'B1_acid'           : 'CN(C)CCN1CCC[C@@H](C(=O)O)C1',
    'B2_amide'          : 'CN(C)CCN1CCC[C@@H](C(N)=O)C1',
    'Cl_F2_BT'          : 'Clc1nc2c(F)cc(F)cc2s1',
    'ethyl_nicotinate'  : 'CCOC(=O)c1cccnc1',
    'C1_ethyl_nipecotate': 'CCOC(=O)[C@@H]1CCCNC1',
    'C3_Boc_acid'       : 'CC(C)(C)OC(=O)N1CCC[C@@H](C(=O)O)C1',
    'C4_Boc_amide'      : 'CC(C)(C)OC(=O)N1CCC[C@@H](C(=O)Nc2nc3c(F)cc(F)cc3s2)C1',

    # A317 SMs & intermediates
    'S_acetylpyrrolidine': 'CC(=O)[C@@H]1CCCN1',
    'N_S_acetylpyrrolidine': 'CC(=O)[C@@H]1CCCN1',  # same – free NH
    'bromopyridine'     : 'Brc1ccccn1',
    'A1_A317'           : 'CC(=O)[C@@H]1CCCN1c1ccccn1',
    'A2_A317'           : 'O=C(CBr)[C@@H]1CCCN1c1ccccn1',
    'thiourea'          : 'NC(N)=S',
    'A3_A317'           : 'Nc1nc([C@@H]2CCCN2c2ccccn2)cs1',
    'picolyl_pyrrole_acid': 'OC(=O)c1cccn1Cc1ccncc1',
    'B1_A317'           : 'O=C(CBr)[C@@H]1CCCN1',
    'B2_A317'           : 'Nc1nc([C@@H]2CCCN2)cs1',
    'B3_A317'           : 'O=C(Nc1nc([C@@H]2CCCN2)cs1)c1cccn1Cc1ccncc1',
    'F_pyridine'        : 'Fc1ccccn1',
    'amino_Br_thiazole' : 'Nc1nc(Br)cs1',
    'C1_A317'           : 'O=C(Nc1nc(Br)cs1)c1cccn1Cc1ccncc1',
    'pyrrolidinyl_B(OH)2': 'OB(O)[C@H]1CCCN1c1ccccn1',

    # 7977 SMs & intermediates
    'amino_Br_Me_pym'   : 'Cc1cnc(N)nc1Br',
    'Br_NO2_pyridine'   : 'Brc1cccnc1[N+](=O)[O-]',
    'A1_7977'           : 'Cc1cnc(Nc2ncccc2[N+](=O)[O-])nc1Br',
    'A2_7977'           : 'Cc1cnc(Nc2ncccc2N)nc1Br',
    'A3_7977'           : 'Cc1cnc(Br)cc1-n1c(=O)[nH]c2cnccc21',
    'ClF_Ph_BA'         : 'OB(O)c1cc(Cl)ccc1F',
    'A4_7977'           : 'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)[nH]c2cnccc21',
    'chloroacetamide'   : 'ClCC(N)=O',
    'B2_7977'           : 'Cc1cnc(Nc2ncccc2[N+](=O)[O-])nc1-c1cc(Cl)ccc1F',
    'B3_7977'           : 'Cc1cnc(Nc2ncccc2N)nc1-c1cc(Cl)ccc1F',
    'dibromo_Me_pym'    : 'Cc1cnc(Br)nc1Br',
    'C1_7977'           : 'Cc1cnc(Br)nc1-c1cc(Cl)ccc1F',
    'azaindole'         : 'c1ccc2[nH]ccc2n1',
    'C2_7977_uracil'    : 'O=C1NC(=O)Nc2cnccc21',
    'C3_7977'           : 'Cc1cnc(-c2cc(Cl)ccc2F)nc1-n1c(=O)[nH]c2cnccc21',
}


# ══════════════════════════════════════════════════════════════════════════════
#  MCUF651
# ══════════════════════════════════════════════════════════════════════════════

# ── Route A ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['R_nipecotic_acid'], '(R)-Nipecotic acid'),
             (SML['amino_F2_BT'],      '2-Amino-4,6-F₂-BT')],
         sm_price='€45/g + €90/g',
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, 0 °C → rt, 12 h', yield_str='72%',
         product=(SML['amide_A1'], '[A1] amide')),
    dict(sm=[(SML['amide_A1'],  '[A1]'),
             (SML['DMAE_Cl'],   '2-(DMAE)Cl·HCl')],
         sm_price='€25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='MeCN, 80 °C, 8 h', yield_str='63%',
         product=(SML['MCUF651'], 'MCUF651')),
],
'MCUF651 — Route A\nAmide coupling → N-alkylation  (2 steps, ~45% overall)',
'mcuf651_A_struct.png')

# ── Route B ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['R_nipecotic_acid'], '(R)-Nipecotic acid'),
             (SML['DMAE_Cl'],          '2-(DMAE)Cl·HCl')],
         sm_price='€45/g + €25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='DMF, 70 °C, 8 h', yield_str='68%',
         product=(SML['B1_acid'], '[B1] N-alkyl acid')),
    dict(sm=[(SML['B1_acid'], '[B1]')],
         reagents=['CDI (€20/g, 1.2 eq)', 'then 35% aq. NH₃'],
         conditions='THF, 0 °C → rt, 30 min', yield_str='70%',
         product=(SML['B2_amide'], '[B2] primary amide')),
    dict(sm=[(SML['B2_amide'],  '[B2]'),
             (SML['Cl_F2_BT'],  '2-Cl-4,6-F₂-BT')],
         sm_price='€120–200/g ⚠',
         reagents=['Pd₂(dba)₃ (2 mol%)', 'XantPhos (4 mol%)', 'Cs₂CO₃'],
         conditions='Toluene, 100 °C, 16 h, N₂', yield_str='55%',
         warning='⚠ SM may exceed €150/g',
         product=(SML['MCUF651'], 'MCUF651')),
],
'MCUF651 — Route B\nN-alkylation → CDI amide → Buchwald C–N arylation  (3 steps, ~26% overall)',
'mcuf651_B_struct.png')

# ── Route C (2-row, 6 steps) ──────────────────────────────────────────────────
_C_A1 = (SML['C1_ethyl_nipecotate'], '[C1] Et ester')
_C_A2 = (SML['R_nipecotic_acid'],    '[C2] (R)-acid')
_C_A3 = (SML['C3_Boc_acid'],         '[C3] N-Boc acid')
_C_A4 = (SML['C4_Boc_amide'],        '[C4] N-Boc amide')
_C_A5 = (SML['amide_A1'],            '[C5] free NH')
_C_fin= (SML['MCUF651'],             'MCUF651')

make_struct_scheme_2row(
    row1=[
        dict(sm=[(SML['ethyl_nicotinate'], 'Ethyl nicotinate')],
             sm_price='€0.60/g',
             reagents=['[Rh(cod)Cl]₂ (0.5 mol%)', '(R)-BINAP (1 mol%)'],
             conditions='AcOH/MeOH, H₂ 50 bar, 60 °C', yield_str='55–65%, ee ~88%',
             warning='⚠ autoclave required',
             product=_C_A1),
        dict(sm=[_C_A1],
             reagents=['NaOH (2 eq)'],
             conditions='EtOH/H₂O, rt, 2 h', yield_str='98%',
             product=_C_A2),
        dict(sm=[_C_A2],
             reagents=['Boc₂O (€5/g, 1.1 eq)', 'NaOH (1 eq)'],
             conditions='THF/H₂O, rt, 12 h', yield_str='92%',
             product=_C_A3),
    ],
    row2=[
        dict(sm=[_C_A3, (SML['amino_F2_BT'], '2-Amino-4,6-F₂-BT')],
             sm_price='€90/g',
             reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
             conditions='DMF, rt, 12 h', yield_str='72%',
             product=_C_A4),
        dict(sm=[_C_A4],
             reagents=['TFA (€5/g, 20 eq)'],
             conditions='DCM, rt, 1 h', yield_str='95%',
             product=_C_A5),
        dict(sm=[_C_A5, (SML['DMAE_Cl'], '2-(DMAE)Cl·HCl')],
             sm_price='€25/g',
             reagents=['K₂CO₃ (€1/g)'],
             conditions='MeCN, 80 °C, 8 h', yield_str='63%',
             product=_C_fin),
    ],
    title='MCUF651 — Route C\nAsymmetric hydrogenation (de novo stereocentre)  (6 steps, ~20% overall)',
    filename='mcuf651_C_struct.png'
)


# ══════════════════════════════════════════════════════════════════════════════
#  A317
# ══════════════════════════════════════════════════════════════════════════════

# ── Route A ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['S_acetylpyrrolidine'], '(S)-2-Acetylpyrrolidine'),
             (SML['bromopyridine'],       '2-Bromopyridine')],
         sm_price='€130/g + €15/g',
         reagents=['Pd₂(dba)₃ (2 mol%)', '(±)-BINAP (4 mol%)', 'Cs₂CO₃'],
         conditions='Toluene, 90 °C, 12 h', yield_str='65%',
         product=(SML['A1_A317'], '[A1]')),
    dict(sm=[(SML['A1_A317'], '[A1]')],
         reagents=['NBS (€5/g, 1.05 eq)'],
         conditions='CHCl₃, 0 °C → rt, 2 h', yield_str='70%',
         warning='⚠ use immediately',
         product=(SML['A2_A317'], '[A2] α-bromo')),
    dict(sm=[(SML['A2_A317'], '[A2]'),
             (SML['thiourea'],  'Thiourea')],
         sm_price='€1/g',
         reagents=['EtOH, reflux, 1 h', 'then K₂CO₃'],
         conditions='free base workup', yield_str='62%',
         product=(SML['A3_A317'], '[A3] 2-aminothiazole')),
    dict(sm=[(SML['A3_A317'],           '[A3]'),
             (SML['picolyl_pyrrole_acid'], '1-(4-Picolyl)pyrrole-\n2-COOH')],
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='55%',
         product=(SML['A317'], 'A317')),
],
'A317 — Route A\nBuchwald N-arylation → α-bromination → Hantzsch → amide  (4 steps, ~16% overall)',
'a317_A_struct.png')

# ── Route B ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['N_S_acetylpyrrolidine'], '(S)-2-Acetylpyrrolidine')],
         sm_price='€130/g',
         reagents=['NBS (€5/g, 1.05 eq)'],
         conditions='CHCl₃, −10 °C, 1 h', yield_str='68%',
         warning='⚠ use immediately',
         product=(SML['B1_A317'], '[B1] α-bromo')),
    dict(sm=[(SML['B1_A317'],  '[B1]'),
             (SML['thiourea'], 'Thiourea')],
         sm_price='€1/g',
         reagents=['EtOH, reflux, 45 min', 'then K₂CO₃'],
         conditions='free base workup', yield_str='58%',
         product=(SML['B2_A317'], '[B2] aminothiazole')),
    dict(sm=[(SML['B2_A317'],             '[B2]'),
             (SML['picolyl_pyrrole_acid'], '1-(4-Picolyl)pyrrole-\n2-COOH')],
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='50%',
         product=(SML['B3_A317'], '[B3] amide')),
    dict(sm=[(SML['B3_A317'],   '[B3]'),
             (SML['F_pyridine'], '2-Fluoropyridine')],
         sm_price='€25/g',
         reagents=['K₂CO₃ (€1/g)'],
         conditions='DMSO, 130 °C, 16 h', yield_str='50%',
         warning='⚠ monitor ee — epimerisation risk',
         product=(SML['A317'], 'A317')),
],
'A317 — Route B  (Pd-free)\nα-bromination → Hantzsch → amide → SNAr N-arylation  (4 steps, ~16% overall)',
'a317_B_struct.png')

# ── Route C ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['amino_Br_thiazole'],    '2-Amino-4-Br-thiazole'),
             (SML['picolyl_pyrrole_acid'], '1-(4-Picolyl)pyrrole-\n2-COOH')],
         sm_price='€60/g  (*see parallel)',
         reagents=['HATU (€40/g)', 'DIPEA (€5/g)'],
         conditions='DMF, rt, 12 h', yield_str='65%',
         product=(SML['C1_A317'], '[C1] bromothiazole amide')),
    dict(sm=[(SML['C1_A317'],               '[C1]'),
             (SML['pyrrolidinyl_B(OH)2'],    '(S)-Pyrrolidinyl-\nBpin †')],
         sm_price='† N-Boc-L-Pro + B₂Pin₂',
         reagents=['Pd(PPh₃)₄ (5 mol%)', 'K₂CO₃'],
         conditions='Dioxane/H₂O, 80 °C, 12 h', yield_str='45%',
         warning='⚠ EXTRAPOLATION — boronate prep needs validation',
         product=(SML['A317'], 'A317')),
],
'A317 — Route C\nAmide on commercial aminobromothiazole → Suzuki  (2 steps + parallel, ~13–18% overall)',
'a317_C_struct.png')


# ══════════════════════════════════════════════════════════════════════════════
#  7977
# ══════════════════════════════════════════════════════════════════════════════

# ── Route A ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['amino_Br_Me_pym'],   '2-Amino-4-Br-\n5-Me-pyrimidine'),
             (SML['Br_NO2_pyridine'],   '3-Br-2-NO₂-\npyridine')],
         sm_price='€75/g  +  €40/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 100 °C, 8 h', yield_str='60%',
         product=(SML['A1_7977'], '[A1] SNAr diarylamine')),
    dict(sm=[(SML['A1_7977'], '[A1]')],
         reagents=['Fe (€2/g, 3 eq)', 'AcOH/EtOH (1:3)'],
         conditions='80 °C, 2 h', yield_str='85%',
         product=(SML['A2_7977'], '[A2] diamine')),
    dict(sm=[(SML['A2_7977'], '[A2]')],
         reagents=['CDI (€20/g, 1.2 eq)'],
         conditions='THF, rt → 60 °C', yield_str='70%',
         product=(SML['A3_7977'], '[A3] N-H bicycle')),
    dict(sm=[(SML['A3_7977'],  '[A3]'),
             (SML['ClF_Ph_BA'], '(2-Cl-4-F-Ph)\nboronic acid')],
         sm_price='€50/g',
         reagents=['Pd(PPh₃)₄ (5 mol%)', 'K₂CO₃'],
         conditions='Dioxane/H₂O (3:1), 80 °C', yield_str='72%',
         product=(SML['A4_7977'], '[A4] arylated bicycle')),
    dict(sm=[(SML['A4_7977'],        '[A4]'),
             (SML['chloroacetamide'], '2-Chloroacetamide')],
         sm_price='€5/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 60 °C, 6 h', yield_str='65%',
         product=(SML['7977'], '7977')),
],
'7977 — Route A\nSNAr → nitro reduction → CDI cyclisation → Suzuki → N-alkylation  (5 steps, ~19% overall)',
'7977_A_struct.png')

# ── Route B  ★ RECOMMENDED ────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['amino_Br_Me_pym'],  '2-Amino-4-Br-\n5-Me-pyrimidine'),
             (SML['Br_NO2_pyridine'],  '3-Br-2-NO₂-\npyridine')],
         sm_price='€75/g  +  €40/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 100 °C, 8 h', yield_str='60%',
         product=(SML['A1_7977'], '[B1] SNAr diarylamine')),
    dict(sm=[(SML['A1_7977'],  '[B1]'),
             (SML['ClF_Ph_BA'], '(2-Cl-4-F-Ph)\nboronic acid')],
         sm_price='€50/g',
         reagents=['Pd(PPh₃)₄ (5 mol%)', 'K₂CO₃'],
         conditions='Dioxane/H₂O (3:1), 80 °C', yield_str='75%',
         product=(SML['B2_7977'], '[B2] aryl diarylamine')),
    dict(sm=[(SML['B2_7977'], '[B2]')],
         reagents=['Fe (€2/g, 3 eq)', 'AcOH/EtOH (1:3)'],
         conditions='80 °C, 2 h', yield_str='85%',
         product=(SML['B3_7977'], '[B3] arylated diamine')),
    dict(sm=[(SML['B3_7977'], '[B3]')],
         reagents=['CDI (€20/g, 1.2 eq)'],
         conditions='THF, rt → 60 °C', yield_str='70%',
         product=(SML['A4_7977'], '[B4] N-H bicycle')),
    dict(sm=[(SML['A4_7977'],        '[B4]'),
             (SML['chloroacetamide'], '2-Chloroacetamide')],
         sm_price='€5/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 60 °C, 6 h', yield_str='65%',
         product=(SML['7977'], '7977')),
],
'7977 — Route B  ★ RECOMMENDED\nSNAr → Suzuki → nitro reduction → CDI cyclisation → N-alkylation  (5 steps, ~22% overall)',
'7977_B_struct.png')

# ── Route C ───────────────────────────────────────────────────────────────────
make_struct_scheme([
    dict(sm=[(SML['dibromo_Me_pym'], '2,4-Dibromo-\n5-Me-pyrimidine'),
             (SML['ClF_Ph_BA'],     '(2-Cl-4-F-Ph)\nboronic acid')],
         sm_price='€90/g  +  €50/g',
         reagents=['Pd(dppf)Cl₂ (2 mol%)', 'K₂CO₃'],
         conditions='Dioxane/H₂O, 80 °C', yield_str='65%',
         product=(SML['C1_7977'], '[C1] mono-Suzuki pym')),
    dict(sm=[(SML['azaindole'],      '7-Azaindole'),
             (SML['C2_7977_uracil'], 'N-H uracil scaffold [C2]')],
         sm_price='€35/g   (⚠ parallel step)',
         reagents=['Triphosgene (€25/g)', 'Pyridine (3 eq)'],
         conditions='DCM, 0 °C → rt', yield_str='55%',
         warning='⚠ EXTRAPOLATION',
         product=(SML['C2_7977_uracil'], '[C2] uracil scaffold')),
    dict(sm=[(SML['C2_7977_uracil'], '[C2]'),
             (SML['C1_7977'],        '[C1]')],
         reagents=['CuI (10 mol%)', 'trans-DACH (20 mol%)', 'K₃PO₄'],
         conditions='DMSO, 110 °C, 24 h', yield_str='50%',
         warning='⚠ EXTRAPOLATION — check N1/N3 regio',
         product=(SML['C3_7977'], '[C3] N1-arylated')),
    dict(sm=[(SML['C3_7977'],        '[C3]'),
             (SML['chloroacetamide'], '2-Chloroacetamide')],
         sm_price='€5/g',
         reagents=['K₂CO₃ (€1/g, 2 eq)'],
         conditions='DMF, 60 °C, 6 h', yield_str='65%',
         product=(SML['7977'], '7977')),
],
'7977 — Route C\nMono-Suzuki + 7-azaindole scaffold + Cu-Ullmann  (4 steps, ~13% overall)',
'7977_C_struct.png')

print('\nAll 9 structure schemes done.')
