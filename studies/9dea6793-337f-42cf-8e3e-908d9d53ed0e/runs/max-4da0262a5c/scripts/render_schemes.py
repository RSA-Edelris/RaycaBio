"""
ChemSketch-style retrosynthetic scheme renderer for all 14 compounds.
Produces one PNG per compound (scheme_<ID>.png) in the workspace.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image
import io, os, numpy as np

workspace = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4"
sdf_path  = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"

# ─── read target SMILES ──────────────────────────────────────────────────────
suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)
targets = {mol.GetProp('_Name'): Chem.MolToSmiles(mol)
           for mol in suppl if mol is not None}

# ─── rendering helpers ───────────────────────────────────────────────────────
def s2a(smi, w=300, h=220):
    """SMILES string → numpy RGB array for imshow."""
    blank = np.full((h, w, 3), 248, dtype=np.uint8)
    if not smi:
        return blank
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return blank
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    d.drawOptions().addStereoAnnotation = True
    d.drawOptions().padding = 0.13
    d.DrawMolecule(mol); d.FinishDrawing()
    return np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert('RGB'))

def retro_arrow(ax, lab=''):
    """Draw double retrosynthetic arrow across the full axes height."""
    for dx in [0.44, 0.49]:
        ax.annotate('', xy=(dx, 0.06), xytext=(dx, 0.94),
                    arrowprops=dict(arrowstyle='->', color='#111',
                                   lw=3 if dx == 0.44 else 1.8,
                                   mutation_scale=20), zorder=5)
    if lab:
        ax.text(0.53, 0.50, lab, fontsize=7.5, color='#c0392b',
                va='center', style='italic', wrap=True)

def mol_row(fig, smis, row_y, row_h, col_x, col_w):
    """Place a row of molecule images inside a figure column."""
    n  = len(smis)
    mw = (col_w - 0.005 * (n - 1)) / max(n, 1)
    for i, smi in enumerate(smis):
        ax = fig.add_axes([col_x + i * (mw + 0.005), row_y, mw, row_h])
        ax.imshow(s2a(smi, 200, int(row_h * 1500)))
        ax.axis('off')
    for i in range(n - 1):
        fig.text(col_x + (i + 1) * (mw + 0.005) - 0.008,
                 row_y + row_h / 2, '+',
                 ha='center', va='center', fontsize=14, color='#111')

def render_scheme(cid, routes, out):
    tgt_smi = targets.get(cid, '')
    fig = plt.figure(figsize=(21, 16))
    fig.patch.set_facecolor('white')

    # main title
    fig.text(0.5, 0.978,
             f'{cid}  —  Retrosynthetic Analysis  (Routes A / B / C)',
             ha='center', va='top', fontsize=14, fontweight='bold',
             color='#1a1a2e')

    # target structure (top centre)
    ax_t = fig.add_axes([0.28, 0.74, 0.44, 0.22])
    ax_t.imshow(s2a(tgt_smi, 520, 260)); ax_t.axis('off')
    ax_t.set_title('TARGET', fontsize=9, color='#555', pad=3, style='italic')

    COLS = [0.01, 0.345, 0.68]
    CW   = 0.315

    for ri, R in enumerate(routes):
        cx  = COLS[ri]
        mid = cx + CW / 2
        rec = R.get('rec', False)
        hdr = '#1a5276' if rec else '#2c3e50'
        star = '  ★ RECOMMENDED' if rec else ''

        # route header
        fig.text(mid, 0.738, R['title'] + star,
                 ha='center', va='top', fontsize=8.5,
                 fontweight='bold', color=hdr)

        lv2 = R.get('lv2')
        if lv2:
            # two-level layout: target→lv1→lv2
            # first arrow  0.72→0.56
            ax1 = fig.add_axes([cx + 0.01, 0.57, CW - 0.02, 0.14])
            ax1.set_xlim(0, 1); ax1.set_ylim(0, 1); ax1.axis('off')
            retro_arrow(ax1, R.get('lab1', ''))
            mol_row(fig, R['lv1'], 0.40, 0.16, cx, CW)
            # second arrow 0.39→0.24
            ax2 = fig.add_axes([cx + 0.01, 0.22, CW - 0.02, 0.16])
            ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')
            retro_arrow(ax2, R.get('lab2', ''))
            mol_row(fig, lv2, 0.04, 0.17, cx, CW)
            src_y = 0.025
        else:
            # single-level layout: target→lv1
            ax1 = fig.add_axes([cx + 0.01, 0.49, CW - 0.02, 0.22])
            ax1.set_xlim(0, 1); ax1.set_ylim(0, 1); ax1.axis('off')
            retro_arrow(ax1, R.get('lab1', ''))
            mol_row(fig, R['lv1'], 0.22, 0.25, cx, CW)
            src_y = 0.195

        src = R.get('src', [])
        if src:
            fig.text(mid, src_y, '  |  '.join(src),
                     ha='center', va='top', fontsize=6.5,
                     color='#555', style='italic')

    for dx in [0.335, 0.668]:
        fig.add_artist(plt.Line2D([dx, dx], [0.02, 0.965],
                                  transform=fig.transFigure,
                                  color='#bbb', lw=1.2))

    plt.savefig(out, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return out

# ─── scheme data for all 14 compounds ───────────────────────────────────────
SCHEMES = {

'102EDL248': [
  {'title':'Route A: Mannich / ring closure', 'rec':False,
   'lv1':['Nc1ccccc1N','CC(=O)/C=C/c1ccccc1'],
   'lab1':'acid-cat. cyclocondensation\n(AcOH, Δ, toluene)',
   'src':['oPDA Σ-131016 T1','benzalacetone Σ T1']},
  {'title':'Route B: Druey–Schmidt ★', 'rec':True,
   'lv1':['Nc1ccccc1N','CC(=O)CC(=O)c1ccccc1'],
   'lab1':'Druey–Schmidt condensation\n(AcOH, toluene, 100 °C)',
   'src':['oPDA Σ-131016 T1','1-Ph-butane-1,3-dione Σ T1']},
  {'title':'Route C: Enamine cyclocondensation', 'rec':False,
   'lv1':['Nc1ccccc1N','CC(=O)c1ccccc1'],
   'lab1':'enamine formation +\nring closure (TFA cat.)',
   'src':['oPDA Σ T1','acetophenone Σ T1']},
],

'056EDL307': [
  {'title':'Route A: Isatoic anhydride route', 'rec':False,
   'lv1':['O=C1OC(=O)c2ccccc2N1','C[C@@H](N)C(=O)O'],
   'lab1':'ring-opening + cyclisation\n(Et3N, THF, 60 °C)',
   'src':['isatoic anhydride Σ T1','L-Ala Σ T1']},
  {'title':'Route B: Anthranilic acid 3-comp.', 'rec':False,
   'lv1':['Nc1ccccc1C(=O)O','O=Cc1ccccc1','C[C@@H](N)C(=O)O'],
   'lab1':'3-component condensation\n(AcOH, Δ)',
   'src':['anthranilic acid Σ T1','PhCHO Σ T1','L-Ala Σ T1']},
  {'title':'Route C: Convergent amino-acid ★', 'rec':True,
   'lv1':['O=C1OC(=O)c2ccccc2N1'],
   'lab1':'isatoic anhydride + amino\nacid ester, cyclise, resolve',
   'lv2':['Nc1ccccc1C(=O)O','O=C=O'],
   'lab2':'from anthranilic acid +\nCO2 / phosgene',
   'src':['anthranilic acid Σ T1','CO2 — bulk gas']},
],

'587EDL247': [
  {'title':'Route A: CBS reductive amination ★', 'rec':True,
   'lv1':['O=C1C(=O)c2ccccc21','CCCN'],
   'lab1':'CBS asymm. reductive amination\n(BH3·THF, −40 °C, >96% ee)',
   'src':['indane-1,2-dione Σ T1','propylamine Σ T1']},
  {'title':'Route B: α-Bromination / SN2', 'rec':False,
   'lv1':['O=C1CCc2ccccc21','Br'],
   'lab1':'NBS radical α-bromination\nthen SN2 with amine',
   'src':['1-indanone Σ T1','NBS Σ T1']},
  {'title':'Route C: Strecker synthesis', 'rec':False,
   'lv1':['O=C1CCc2ccccc21','N','C#N'],
   'lab1':'Strecker + nitrile hydrolysis\n(HCN, NH3, then H3O+)',
   'src':['1-indanone Σ T1','NH3 aq Σ T1','KCN Σ T1']},
],

'ED091205': [
  {'title':'Route A: Nitrone [3+2] cycloadd. ★', 'rec':True,
   'lv1':['O=C1CNc2ccccc21','O=[N+]([O-])CC'],
   'lab1':'1,3-dipolar cycloaddition\n(spiro ring: MW or Δ)',
   'src':['isoindolinone Fluorochem T2','N-alkyl hydroxylamine Σ T1']},
  {'title':'Route B: Radical spiro closure', 'rec':False,
   'lv1':['O=C1c2ccccc2CN1','BrCC(=O)OCC'],
   'lab1':'radical ring closure via\nBu3SnH / AIBN',
   'src':['isoindolin-1-one Σ T1','ethyl bromoacetate Σ T1']},
  {'title':'Route C: Schmidt rearrangement', 'rec':False,
   'lv1':['O=C1c2ccccc2CN1','N=[N+]=[N-]'],
   'lab1':'Schmidt spiro expansion\n(TMSN3, BF3·Et2O)',
   'src':['isoindolin-1-one Σ T1','TMSN3 Σ T1']},
],

'ED205141': [
  {'title':'Route A: L-Trp chiral pool ★', 'rec':True,
   'lv1':['N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O'],
   'lab1':'Pictet–Spengler then\npyrroloindoline closure',
   'lv2':['O=Cc1ccc(OC)cc1','NC(=O)c1ccccc1'],
   'lab2':'Cbz-Trp + 4-MeO-PhCHO\n(TFA, CH2Cl2)',
   'src':['L-Trp Σ T1','4-MeO-benzaldehyde Σ T1','benzamide Σ T1']},
  {'title':'Route B: Pictet–Spengler (racemic)', 'rec':False,
   'lv1':['NCCc1c[nH]c2ccccc12','O=Cc1ccc(OC)cc1'],
   'lab1':'tryptamine + aldehyde\nPictet–Spengler (TFA)',
   'src':['tryptamine Σ T1','4-MeO-PhCHO Σ T1']},
  {'title':'Route C: Asymm. Pd C–H activation', 'rec':False,
   'lv1':['N[C@@H](Cc1c[nH]c2ccccc12)C(=O)OCC','BrCC(=O)c1ccccc1'],
   'lab1':'Pd-cat. intramolecular\nC–H activation (Pd/BINAP)',
   'src':['Trp-OEt Σ T1','phenacyl bromide Σ T1']},
],

'ED636906': [
  {'title':'Route A: Convergent 3-fragment ★', 'rec':True,
   'lv1':['NCCc1ccc(O)cc1','O=CCc1ccccc1'],
   'lab1':'Pictet–Spengler (tyramine +\nphenylacetaldehyde → THIQ)',
   'lv2':['NCCc1ccc(O)cc1','Clc1ccc(-c2ccccc2OC)cc1'],
   'lab2':'THIQ N-arylation\n(Buchwald Pd/BINAP)',
   'src':['tyramine Σ T1','phenylacetaldehyde Σ T1','aryl-Cl Fluorochem T2']},
  {'title':'Route B: Bischler–Napieralski', 'rec':False,
   'lv1':['NCCc1ccc(O)cc1','O=C(Cl)Cc1ccccc1'],
   'lab1':'Bischler–Napieralski: acylation\n→ POCl3 cyclisation',
   'src':['tyramine Σ T1','phenylacetyl-Cl Σ T1']},
  {'title':'Route C: Suzuki + THIQ redn.', 'rec':False,
   'lv1':['O=C1Cc2ccccc2NC1Cc1ccccc1','Brc1ccc(-c2ccccc2OC)cc1'],
   'lab1':'Suzuki coupling at THIQ\naryl position (Pd)',
   'src':['THIQ-1-one Enamine T3','aryl bromide Σ T1']},
],

'ED249356': [
  {'title':'Route A: Isatoic anhydride ★', 'rec':True,
   'lv1':['O=C1OC(=O)c2ccccc2N1','NCCNC(=O)c1ccccc1'],
   'lab1':'ring-opening + benzimidazolone\nclosure (CDI, Et3N)',
   'src':['isatoic anhydride Σ T1','N-Bz-ethylenediamine Σ T1']},
  {'title':'Route B: Anthranilamide cyclisation', 'rec':False,
   'lv1':['Nc1ccccc1NC(=O)c1ccccc1','O=C=O'],
   'lab1':'CDI-mediated urea formation\n(THF, reflux)',
   'src':['2-amino-N-Bz aniline Σ T1','CDI Σ T1']},
  {'title':'Route C: Pd-cat. C–N coupling', 'rec':False,
   'lv1':['Brc1ccccc1NC(=O)c1ccccc1','O=C1Nc2ccccc2N1'],
   'lab1':'Buchwald N-arylation\n(Pd2dba3/BrettPhos)',
   'src':['benzimidazolinone Σ T1','aryl bromide Σ T1']},
],

'ED005228': [
  {'title':'Route A: Nitrone [3+2]', 'rec':False,
   'lv1':['O=C1c2ccccc2CN1','O=[N+]([O-])/C=C/c1ccccc1'],
   'lab1':'nitrone cycloaddition\n(PhCH=CHNMe+O−)',
   'src':['isoindolinone Σ T1','N-methyl-C-Ph nitrone Σ T1']},
  {'title':'Route B: Azomethine ylide ★', 'rec':True,
   'lv1':['O=C1c2ccccc2CN1','C(=O)(c1ccccc1)/C=C/c1ccccc1'],
   'lab1':'[3+2] azomethine ylide\n(Ag2O, MeCN, Δ)',
   'lv2':['O=C1c2ccccc2CN1','c1ccc(/C=C/c2ccccc2)cc1'],
   'lab2':'dipolarophile from\ncinnamaldehyde',
   'src':['isoindolinone Σ T1','trans-chalcone Σ T1']},
  {'title':'Route C: Staudinger ligation', 'rec':False,
   'lv1':['O=C1c2ccccc2CN1','N#Cc1ccccc1'],
   'lab1':'[2+2] Staudinger +\nring expansion',
   'src':['isoindolinone Σ T1','benzonitrile Σ T1']},
],

'ED963829': [
  {'title':'Route A: Staudinger [2+2]', 'rec':False,
   'lv1':['O=C=CC1CC1','Nc1ccccc1'],
   'lab1':'ketene–imine [2+2]\nto spiro β-lactam',
   'src':['cyclopropyl ketene (gen. in situ)','aniline Σ T1']},
  {'title':'Route B: Isocyanate spiro ★', 'rec':True,
   'lv1':['O=C=NC1CC1','OC1CN2CCC2C1'],
   'lab1':'cyclopropyl isocyanate +\nspiro amino alcohol',
   'lv2':['O=C1CC1','ClC(=O)Cl'],
   'lab2':'cyclopropylamine + COCl2\n→ isocyanate',
   'src':['cyclopropylamine Σ T1','amino-alcohol Enamine T3','COCl2 Σ T1']},
  {'title':'Route C: Ring-closing metathesis', 'rec':False,
   'lv1':['C=CC1(CC1=O)N','C=CC(=O)Cl'],
   'lab1':'allylation + RCM\n(Grubbs 2nd gen)',
   'src':['allyl glycine Enamine T3','acryloyl-Cl Σ T1']},
],

'ED106680': [
  {'title':'Route A: Oxidative phenolic coupling', 'rec':False,
   'lv1':['NCc1cccc(O)c1','O=Cc1ccccc1OCC'],
   'lab1':'Barton-type dearomative\noxidative coupling (PhI(OAc)2)',
   'src':['3-OH-benzylamine Σ T1','2-(OEt-methyl)benzaldehyde T2']},
  {'title':'Route B: Mannich/CBS/Mitsunobu ★', 'rec':True,
   'lv1':['NCc1cccc(O)c1','OCC(N)CO'],
   'lab1':'CBS redn. + intramolecular\nMitsunobu (DEAD/PPh3)',
   'lv2':['NCc1cccc(O)c1','Oc1ccccc1CBr'],
   'lab2':'O-alkylation of phenol\n(K2CO3, DMF)',
   'src':['3-OH-benzylamine Σ T1','2-(BrCH2)phenol Σ T1']},
  {'title':'Route C: Ring-closing metathesis', 'rec':False,
   'lv1':['NCc1cccc(O)c1','C=CC(=O)c1ccccc1OCC'],
   'lab1':'Grubbs RCM then\nBuchwald ring closure',
   'src':['3-OH-benzylamine Σ T1','2-MeO-phenyl vinyl ketone Σ T1']},
],

'test_001': [
  {'title':'Route A: Organolithium + Barton–McCombie', 'rec':False,
   'lv1':['Clc1nc(-c2ccccc2OC)cc2ccccc12','O=C1CCN(C(=O)c2ccccc2OC)CC1'],
   'lab1':'C1-Li-isoquinoline addition\nto N-acyl-4-piperidone',
   'lv2':['COc1ccccc1-c1ncc2ccccc2c1','Brc1nc(-c2ccccc2OC)cc2ccccc12'],
   'lab2':'Bischler–Napieralski\n→ 1-Br-isoquinoline',
   'src':['2-MeO-PhAcOH Σ T1','2-aminobenzaldehyde Σ T1','N-acyl-piperidinone T1']},
  {'title':'Route B: Minisci radical ★', 'rec':True,
   'lv1':['COc1ccccc1-c1ncc2ccccc2c1','OC(=O)C1(C)CCN(C(=O)c2ccccc2OC)CC1'],
   'lab1':'Minisci decarboxylative\nradical at isoquinoline C1\n(Ag2S2O8, H2SO4, 60°C)',
   'src':['3-(2-MeO-Ph)isoquinoline Fluorochem T2','N-acyl-4-Me-pip-4-COOH T2']},
  {'title':'Route C: Rh(I) arylboronate / iminium', 'rec':False,
   'lv1':['COc1ccccc1-c1ncc2ccccc2c1','OC1(C)CCN(C(=O)c2ccccc2OC)CC1'],
   'lab1':'Rh(I)-cat. addition of\nboronate to N-acyl iminium',
   'src':['isoquinolinyl Bpin Fluorochem T2','N-acyl-4-Me-piperidinol T2']},
],

'test_002': [
  {'title':'Route A: Sequential SNAr ★', 'rec':True,
   'lv1':['Clc1nc(Cl)c2[nH]cnc2n1','NCCc1c[nH]cn1','Nc1ccc(C(F)(F)F)cc1N'],
   'lab1':'C6-SNAr (aniline, 100°C)\nthen C2-SNAr (histamine, 130°C)',
   'lv2':['Clc1nc(Cl)c2[nH]cnc2n1','C1CCNC1'],
   'lab2':'urea installation: CDI +\npyrrolidine on aniline NH2',
   'src':['2,6-Cl2-purine Σ-D5765 T1','histamine·2HCl Σ-H7125 T1','4-CF3-1,2-PDA Σ T1']},
  {'title':'Route B: 2-F-6-Cl-purine selective', 'rec':False,
   'lv1':['Fc1nc(Cl)c2[nH]cnc2n1','NCCc1c[nH]cn1'],
   'lab1':'C2-F SNAr (alkylamino, RT)\nthen C6-Cl SNAr (aryl, 100°C)',
   'src':['2-F-6-Cl-purine Fluorochem T2','histamine Σ T1']},
  {'title':'Route C: Buchwald C–N amination', 'rec':False,
   'lv1':['Clc1nc(NCCc2c[nH]cn2)c2[nH]cnc2n1','Nc1ccc(C(F)(F)F)cc1N'],
   'lab1':'Pd2(dba)3/RuPhos/Cs2CO3\ntoluene 100°C',
   'src':['2-Cl-6-histaminyl-purine (int)','4-CF3-1,2-PDA Σ T1']},
],

'test_003': [
  {'title':'Route A: De novo 3-fragment', 'rec':False,
   'lv1':['O=C1CCC(N)C(=O)N1','O=C1CNc2ccccc21','NCCc1ccc(O)cc1'],
   'lab1':'glutarimide + isoindolinone\n+ tyramine convergent assembly',
   'src':['3-aminoglutarimide Fluorochem T2','isoindolinone Σ T1','tyramine Σ T1']},
  {'title':'Route B: Pomalidomide + THIQ ★', 'rec':True,
   'lv1':['O=C1CCC(N2C(=O)c3cc(N)ccc3C2=O)C(=O)N1','NCCc1ccc(O)cc1','C1CNCCN1'],
   'lab1':'pomalidomide (commercial) +\nPictet–Spengler THIQ +\npiperazine linker assembly',
   'lv2':['NCCc1ccc(O)cc1','O=CCc1ccccc1'],
   'lab2':'tyramine + phenylacetaldehyde\n→ THIQ (Pictet–Spengler)',
   'src':['pomalidomide Σ-PZ0008 T1','tyramine Σ T1','piperazine Σ T1','PhCH2CHO Σ T1']},
  {'title':'Route C: Late-stage Suzuki assembly', 'rec':False,
   'lv1':['O=C1CCC(N2C(=O)c3ccc(Br)cc3C2=O)C(=O)N1','NCCc1ccc(O)cc1'],
   'lab1':'Pd-cat. Suzuki coupling:\nbromolenalidomide + THIQ-Bpin',
   'src':['bromolenalidomide int (T3)','THIQ boronate (int)']},
],

'test_004': [
  {'title':'Route A: Schmidt imidate linear', 'rec':False,
   'lv1':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O','OCC1OC(OC(CCl3)=N)C(OCC2=CC=CC=C2)C(OCC2=CC=CC=C2)C1OCC1=CC=CC=C1'],
   'lab1':'allyl-GlcNAc acceptor +\nGlc trichloroacetimidate donor\n(TMSOTf, −40°C → β)',
   'lv2':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O','OC1OC(C)C(O)C(O)C1O'],
   'lab2':'second glycosylation: Fuc\nimidate donor (BF3, −60°C → α)',
   'src':['allyl-GlcNAc Σ-A7882 T1','D-glucose Σ T1','L-fucose Σ-F2252 T1']},
  {'title':'Route B: Thioglycoside block ★', 'rec':True,
   'lv1':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O','SCC1OC(CO)C(O)C(O)C1O','OC1OC(C)C(O)C(O)C1O'],
   'lab1':'allyl-GlcNAc acceptor (C3-OH free)\n+ Glc-SEt (NIS/TfOH, β)\n+ Fuc-OH donor pre-made',
   'src':['allyl-GlcNAc Σ T1','Glc-SEt (from D-glc) T1','L-fucose Σ-F2252 T1']},
  {'title':'Route C: One-pot orthogonal glycosylation', 'rec':False,
   'lv1':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O','SCC1OC(CO)C(O)C(OC)C1O','OC1OC(C)C(O)C(O)C1O'],
   'lab1':'one-pot: DDQ activates PMB-S-Glc\nthen TMSOTf activates Fuc-imidate',
   'src':['allyl-GlcNAc Σ T1','PMB-S-Glc donor (int)','Fuc-imidate (int)']},
],

}

# ─── render all 14 ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    generated = []
    for cid, routes in SCHEMES.items():
        out = os.path.join(workspace, f'scheme_{cid}.png')
        render_scheme(cid, routes, out)
        generated.append(out)
    print(f'\nDone — {len(generated)} scheme PNGs written.')
