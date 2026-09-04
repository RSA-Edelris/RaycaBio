
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image as PILImage
from rdkit import Chem
from rdkit.Chem import Draw, AllChem

OUT = '/home/ubuntu/rayca-sessions/8309667e-a164-44d9-ac9b-ce1096db0a98-90d0a82fa1dd'
STEP_W = 5.2
FIG_H2 = 11.0

def _mol_img(smiles, size=(260, 170), bg=(255, 255, 255)):
    if smiles is None:
        return np.array(PILImage.new('RGB', size, bg))
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return np.array(PILImage.new('RGB', size, bg))
    AllChem.Compute2DCoords(mol)
    img = Draw.MolToImage(mol, size=size)
    if bg != (255, 255, 255):
        arr = np.array(img, dtype=np.uint8)
        mask = (arr[:,:,0]>240)&(arr[:,:,1]>240)&(arr[:,:,2]>240)
        arr[mask] = bg
        return arr
    return np.array(img)

def _bg(idx, n_total):
    if idx == 0:         return (223,240,216)
    elif idx == n_total: return (255,243,205)
    else:                return (232,244,253)

def make_struct_scheme_2row_v2(row1, row2, title, filename):
    n_max  = max(len(row1), len(row2))
    fig_w  = n_max * STEP_W + 1.0
    total_slots = 2 * n_max + 1
    slot_w = 1.0 / total_slots

    # Increased row separation to prevent warning/reagent text overlap
    y_top  = 0.79      # row-1 y centre  (was 0.75)
    y_bot  = 0.25      # row-2 y centre  (was 0.27)
    box_h  = 0.30
    box_w  = slot_w * 0.88
    n_total = len(row1) + len(row2)

    fig, ax = plt.subplots(figsize=(fig_w, FIG_H2))
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    ax.set_facecolor('white'); fig.patch.set_facecolor('white')
    ax.text(0.5, 0.985, title, ha='center', va='top', fontsize=10,
            fontweight='bold', fontfamily='DejaVu Sans', multialignment='center')

    def draw_box(cx, compounds, box_idx, y_ctr, price=None):
        bg_rgb = _bg(box_idx, n_total)
        bx, by = cx - box_w/2, y_ctr - box_h/2
        ax.add_patch(mpatches.FancyBboxPatch(
            (bx, by), box_w, box_h,
            boxstyle='round,pad=0.01', lw=1.2, edgecolor='#3a7abf',
            facecolor=tuple(c/255 for c in bg_rgb), zorder=3))
        if len(compounds) == 1:
            smi, lbl = compounds[0]
            mol_px = (int(box_w*fig_w*100*0.82), int(box_h*FIG_H2*100*0.72))
            img = _mol_img(smi, size=mol_px, bg=bg_rgb)
            mx = box_w*0.09; my = box_h*0.14
            extent=[bx+mx, bx+box_w-mx, by+my, by+box_h-my-0.03]
            ax.imshow(img, extent=extent, aspect='auto', zorder=4, origin='upper')
            ax.text(cx, by+0.018, lbl, ha='center', va='bottom',
                    fontsize=6.8, fontfamily='DejaVu Sans',
                    color='#222', zorder=5, multialignment='center', linespacing=1.2)
        else:
            smi1,lbl1=compounds[0]; smi2,lbl2=compounds[1]
            half=box_w*0.44
            cx1=bx+half*0.5+box_w*0.01; cx2=bx+box_w-half*0.5-box_w*0.01
            mol_px=(int(half*fig_w*100*0.80), int(box_h*FIG_H2*100*0.68))
            for smi,lbl,cxc in [(smi1,lbl1,cx1),(smi2,lbl2,cx2)]:
                img=_mol_img(smi,size=mol_px,bg=bg_rgb)
                my=box_h*0.14
                bx_m=cxc-half/2+box_w*0.01
                extent=[bx_m,bx_m+half-box_w*0.02,by+my,by+box_h-my-0.03]
                ax.imshow(img,extent=extent,aspect='auto',zorder=4,origin='upper')
                ax.text(cxc,by+0.018,lbl,ha='center',va='bottom',
                        fontsize=6.0,fontfamily='DejaVu Sans',
                        color='#222',zorder=5,multialignment='center')
            ax.text(cx,y_ctr,'+',ha='center',va='center',
                    fontsize=9,fontweight='bold',color='#555',zorder=6)
        if price:
            ax.text(cx, by-0.020, price, ha='center', va='top',
                    fontsize=6.5, color='#666', fontstyle='italic', zorder=5)

    def draw_arr(x1, x2, reagents, cond, yld, y_ctr, warn=None):
        mx=(x1+x2)/2
        ax.annotate('', xy=(x2,y_ctr), xytext=(x1,y_ctr),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=1.6, mutation_scale=16), zorder=5)
        ax.text(mx, y_ctr+0.18, '\n'.join(reagents),
                ha='center', va='bottom', fontsize=7.0,
                multialignment='center', linespacing=1.2,
                fontfamily='DejaVu Sans', zorder=5)
        below = cond+('\n'+yld if yld else '')
        ax.text(mx, y_ctr-0.18, below,
                ha='center', va='top', fontsize=6.6, color='#444',
                multialignment='center', linespacing=1.2,
                fontfamily='DejaVu Sans', zorder=5)
        if warn:
            # FIX: use -0.22 offset (was -0.30) to stay clear of row-2 reagent text
            ax.text(mx, y_ctr-0.22, warn,
                    ha='center', va='top', fontsize=6.2,
                    color='#c0392b', zorder=5)

    # Row 1
    for i,s in enumerate(row1):
        cs=2*i; cx=(cs+0.5)*slot_w; x1=(cs+1)*slot_w
        x2=(2*i+2)*slot_w; px=(2*i+2+0.5)*slot_w
        draw_box(cx, s['sm'], i, y_top, s.get('sm_price'))
        draw_arr(x1,x2,s['reagents'],s.get('conditions',''),
                 s.get('yield_str',''),y_top,s.get('warning'))
        if i==len(row1)-1:
            draw_box(px, [s['product']], len(row1), y_top)

    # Connecting arrow (end of row1 → start of row2)
    x_end = (2*len(row1)+0.5)*slot_w
    x_st  = 0.5*slot_w
    ymid_v = (y_top - box_h/2 + y_bot + box_h/2) / 2
    ax.plot([x_end,x_end],[y_top-box_h/2,ymid_v],color='#111',lw=1.6,zorder=5)
    ax.plot([x_end,x_st], [ymid_v,ymid_v],       color='#111',lw=1.6,zorder=5)
    ax.annotate('', xy=(x_st, y_bot+box_h/2+0.005),
                xytext=(x_st, ymid_v),
                arrowprops=dict(arrowstyle='->', color='#111',
                                lw=1.6, mutation_scale=16), zorder=5)

    # Row 2
    n_r1 = len(row1)
    for i,s in enumerate(row2):
        cs=2*i; cx=(cs+0.5)*slot_w; x1=(cs+1)*slot_w
        x2=(2*i+2)*slot_w; px=(2*i+2+0.5)*slot_w
        draw_box(cx, s['sm'], n_r1+i, y_bot, s.get('sm_price'))
        draw_arr(x1,x2,s['reagents'],s.get('conditions',''),
                 s.get('yield_str',''),y_bot,s.get('warning'))
        if i==len(row2)-1:
            draw_box(px, [s['product']], n_r1+len(row2), y_bot,
                     s.get('product_price'))

    plt.tight_layout(rect=[0,0,1,0.96])
    path=f'{OUT}/{filename}'
    plt.savefig(path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f'Saved: {path}')

# Re-use the SML dictionary already in namespace
_C_A1 = (SML['C1_ethyl_nipecotate'], '[C1] Et ester')
_C_A2 = (SML['R_nipecotic_acid'],    '[C2] (R)-acid')
_C_A3 = (SML['C3_Boc_acid'],         '[C3] N-Boc acid')
_C_A4 = (SML['C4_Boc_amide'],        '[C4] N-Boc amide')
_C_A5 = (SML['amide_A1'],            '[C5] free NH')
_C_fin= (SML['MCUF651'],             'MCUF651')

make_struct_scheme_2row_v2(
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
