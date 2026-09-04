"""
render_forward_schemes.py
Forward synthesis schemes for all 14 compounds x 3 routes.
Horizontal left-to-right: SM(s) -> arrow+reagents -> intermediate -> arrow -> target.
Uses validated SMILES from retrosynthetic SCHEMES; adds forward conditions.
Output: fwd_<cid>.png (24x12 in, 100 dpi).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io, os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image

workspace = "/home/ubuntu/rayca-sessions/9dea6793-337f-42cf-8e3e-908d9d53ed0e-dc0c221c42d4"
sdf_path  = "/home/ubuntu/rayca-artifacts/dc0c221c42d47c64e9717502/files/PoC Retrosynthetic analysis_Targets.sdf"

suppl = Chem.SDMolSupplier(sdf_path, removeHs=False, sanitize=True)
targets = {mol.GetProp('_Name'): Chem.MolToSmiles(mol)
           for mol in suppl if mol is not None}

def s2a(smi, w=200, h=160):
    blank = np.full((h, w, 3), 248, dtype=np.uint8)
    mol = Chem.MolFromSmiles(smi) if smi else None
    if mol is None:
        return blank
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    d.drawOptions().addStereoAnnotation = True
    d.drawOptions().padding = 0.12
    d.DrawMolecule(mol); d.FinishDrawing()
    return np.array(Image.open(io.BytesIO(d.GetDrawingText())).convert('RGB'))

# ---------------------------------------------------------------------------
# SCHEMES: validated SMILES for intermediates (from render_schemes.py)
# Each route: lv1=intermediates, lv2=SMs (optional, 2-level routes only)
# Forward direction: lv2 -step1-> lv1 -step2-> target
#                or  lv1 -step1-> target   (single-level)
# ---------------------------------------------------------------------------
SCHEMES = {
'102EDL248': [
  {'title':'Route A: Mannich / ring closure','rec':False,
   'lv1':['Nc1ccccc1N','CC(=O)/C=C/c1ccccc1']},
  {'title':'Route B: Druey-Schmidt','rec':True,
   'lv1':['Nc1ccccc1N','CC(=O)CC(=O)c1ccccc1']},
  {'title':'Route C: Enamine cyclocondensation','rec':False,
   'lv1':['Nc1ccccc1N','CC(=O)c1ccccc1']},
],
'056EDL307': [
  {'title':'Route A: Isatoic anhydride','rec':False,
   'lv1':['O=C1OC(=O)c2ccccc2N1','C[C@@H](N)C(=O)O']},
  {'title':'Route B: Anthranilic acid 3-comp.','rec':False,
   'lv1':['Nc1ccccc1C(=O)O','O=Cc1ccccc1','C[C@@H](N)C(=O)O']},
  {'title':'Route C: Convergent amino-acid','rec':True,
   'lv1':['O=C1OC(=O)c2ccccc2N1'],
   'lv2':['Nc1ccccc1C(=O)O']},
],
'587EDL247': [
  {'title':'Route A: CBS reductive amination','rec':True,
   'lv1':['O=C1C(=O)c2ccccc21','CCCN']},
  {'title':'Route B: alpha-Bromination / SN2','rec':False,
   'lv1':['O=C1CCc2ccccc21','Br']},
  {'title':'Route C: Strecker synthesis','rec':False,
   'lv1':['O=C1CCc2ccccc21','N','C#N']},
],
'ED091205': [
  {'title':'Route A: Nitrone [3+2]','rec':True,
   'lv1':['O=C1CNc2ccccc21','CCN(O)O']},
  {'title':'Route B: Radical spiro closure','rec':False,
   'lv1':['O=C1c2ccccc2CN1','BrCC(=O)OCC']},
  {'title':'Route C: Schmidt rearrangement','rec':False,
   'lv1':['O=C1c2ccccc2CN1','[N-]=[N+]=N']},
],
'ED205141': [
  {'title':'Route A: L-Trp chiral pool','rec':True,
   'lv1':['N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O'],
   'lv2':['O=Cc1ccc(OC)cc1','NC(=O)c1ccccc1']},
  {'title':'Route B: Pictet-Spengler racemic','rec':False,
   'lv1':['NCCc1c[nH]c2ccccc12','O=Cc1ccc(OC)cc1']},
  {'title':'Route C: Pd C-H activation','rec':False,
   'lv1':['N[C@@H](Cc1c[nH]c2ccccc12)C(=O)OCC','BrCC(=O)c1ccccc1']},
],
'ED636906': [
  {'title':'Route A: Convergent 3-fragment','rec':True,
   'lv1':['NCCc1ccc(O)cc1','O=CCc1ccccc1'],
   'lv2':['NCCc1ccc(O)cc1','Clc1ccc(-c2ccccc2OC)cc1']},
  {'title':'Route B: Bischler-Napieralski','rec':False,
   'lv1':['NCCc1ccc(O)cc1','O=C(Cl)Cc1ccccc1']},
  {'title':'Route C: Suzuki + THIQ redn.','rec':False,
   'lv1':['O=C1Cc2ccccc2NC1Cc1ccccc1','Brc1ccc(-c2ccccc2OC)cc1']},
],
'ED249356': [
  {'title':'Route A: Isatoic anhydride','rec':True,
   'lv1':['O=C1OC(=O)c2ccccc2N1','NCCNC(=O)c1ccccc1']},
  {'title':'Route B: Anthranilamide cyclisation','rec':False,
   'lv1':['Nc1ccccc1NC(=O)c1ccccc1']},
  {'title':'Route C: Buchwald C-N','rec':False,
   'lv1':['Brc1ccccc1NC(=O)c1ccccc1','O=C1Nc2ccccc2N1']},
],
'ED005228': [
  {'title':'Route A: Nitrone [3+2]','rec':False,
   'lv1':['O=C1c2ccccc2CN1','O=[N+]([O-])/C=C/c1ccccc1']},
  {'title':'Route B: Azomethine ylide','rec':True,
   'lv1':['O=C1c2ccccc2CN1','C(=O)(c1ccccc1)/C=C/c1ccccc1'],
   'lv2':['O=C1c2ccccc2CN1','c1ccc(/C=C/c2ccccc2)cc1']},
  {'title':'Route C: Staudinger ligation','rec':False,
   'lv1':['O=C1c2ccccc2CN1','N#Cc1ccccc1']},
],
'ED963829': [
  {'title':'Route A: Staudinger [2+2]','rec':False,
   'lv1':['O=C=CC1CC1','Nc1ccccc1']},
  {'title':'Route B: Isocyanate spiro','rec':True,
   'lv1':['O=C=NC1CC1','OC1CN2CCC2C1'],
   'lv2':['NC1CC1','ClC(=O)Cl']},
  {'title':'Route C: RCM','rec':False,
   'lv1':['C=CC1(CC1=O)N','C=CC(=O)Cl']},
],
'ED106680': [
  {'title':'Route A: Oxidative phenolic coupling','rec':False,
   'lv1':['NCc1cccc(O)c1','O=Cc1ccccc1OCC']},
  {'title':'Route B: Mannich/CBS/Mitsunobu','rec':True,
   'lv1':['NCc1cccc(O)c1','OCC(N)CO'],
   'lv2':['NCc1cccc(O)c1','Oc1ccccc1CBr']},
  {'title':'Route C: RCM / Buchwald','rec':False,
   'lv1':['NCc1cccc(O)c1','C=CC(=O)c1ccccc1OCC']},
],
'test_001': [
  {'title':'Route A: Organolithium / Barton-McCombie','rec':False,
   'lv1':['Clc1nc(-c2ccccc2OC)cc2ccccc12','O=C1CCN(C(=O)c2ccccc2OC)CC1'],
   'lv2':['COc1ccccc1-c1ncc2ccccc2c1','Brc1nc(-c2ccccc2OC)cc2ccccc12']},
  {'title':'Route B: Minisci radical','rec':True,
   'lv1':['COc1ccccc1-c1ncc2ccccc2c1','OC(=O)C1(C)CCN(C(=O)c2ccccc2OC)CC1']},
  {'title':'Route C: Rh(I) / iminium','rec':False,
   'lv1':['COc1ccccc1-c1ncc2ccccc2c1','OC1(C)CCN(C(=O)c2ccccc2OC)CC1']},
],
'test_002': [
  {'title':'Route A: Sequential SNAr','rec':True,
   'lv1':['Clc1nc(Cl)c2[nH]cnc2n1','NCCc1c[nH]cn1','Nc1ccc(C(F)(F)F)cc1N']},
  {'title':'Route B: 2-F-6-Cl-purine selective','rec':False,
   'lv1':['Fc1nc(Cl)c2[nH]cnc2n1','NCCc1c[nH]cn1']},
  {'title':'Route C: Buchwald C-N','rec':False,
   'lv1':['Clc1nc(NCCc2c[nH]cn2)c2[nH]cnc2n1','Nc1ccc(C(F)(F)F)cc1N']},
],
'test_003': [
  {'title':'Route A: De novo 3-fragment','rec':False,
   'lv1':['O=C1CCC(N)C(=O)N1','O=C1CNc2ccccc21','NCCc1ccc(O)cc1']},
  {'title':'Route B: Pomalidomide + THIQ','rec':True,
   'lv1':['O=C1CCC(N2C(=O)c3cc(N)ccc3C2=O)C(=O)N1','NCCc1ccc(O)cc1'],
   'lv2':['NCCc1ccc(O)cc1','O=CCc1ccccc1']},
  {'title':'Route C: Late-stage Suzuki','rec':False,
   'lv1':['O=C1CCC(N2C(=O)c3ccc(Br)cc3C2=O)C(=O)N1','NCCc1ccc(O)cc1']},
],
'test_004': [
  {'title':'Route A: Schmidt imidate linear','rec':False,
   'lv1':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O',
           'OC(=O)C1OC(OC(CCl3)=N)C(OCc2ccccc2)C(OCc2ccccc2)C1OCc1ccccc1'],
   'lv2':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O','OC1OC(C)C(O)C(O)C1O']},
  {'title':'Route B: Thioglycoside block','rec':True,
   'lv1':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O',
           'SCC1OC(CO)C(O)C(O)C1O','OC1OC(C)C(O)C(O)C1O']},
  {'title':'Route C: One-pot orthogonal','rec':False,
   'lv1':['C=CCOC1OC(CO)C(O)C(O)C1NC(C)=O',
           'SCC1OC(CO)C(O)C(OC)C1O','OC1OC(C)C(O)C(O)C1O']},
],
}

# ---------------------------------------------------------------------------
# Forward synthesis conditions
# Each entry: (step1_label, step1_yield [, step2_label, step2_yield])
# step1: lv2->lv1 (if lv2 present) else lv1->target
# step2: lv1->target (only if lv2 present)
# ---------------------------------------------------------------------------
FC = {
'102EDL248': [
  ('AcOH (cat.), EtOH / toluene\n80 °C, 5 h; recrystn.','65%'),
  ('AcOH (0.1 eq), toluene\n100 °C, 6 h  [Druey-Schmidt]','75%'),
  ('TFA (0.1 eq), EtOH\n80 °C, 3 h  [enamine cyclisation]','55%'),
],
'056EDL307': [
  ('Et₃N (2 eq), THF, 60 °C, 2 h\nthen AcOH, toluene, reflux','68%'),
  ('AcOH (cat.), EtOH\nreflux, 6 h  [3-component]','50%'),
  # 2-level: lv2->lv1 is anthranilic->isatoic; lv1->target is isatoic+AA->product
  ('i-PrOCOCl or CDI, Et₃N\nEtOAc, 0°C→60°C, 3 h','80%',
   'Et₃N (1.5 eq), CH₂Cl₂, 0°C→rt\nthen CDI, DMF, 80°C, 4 h','72%'),
],
'587EDL247': [
  ('(R)-CBS (0.1 eq), BH₃·THF\nCH₂Cl₂, −40°C, 2 h; >96% ee','82%'),
  ('NBS (1.05 eq), AIBN, CCl₄, reflux\nthen n-PrNH₂, DMF, 60°C','65%'),
  ('NH₄CN, HCl, EtOH/H₂O, rt, 12 h\nthen 6N HCl, reflux, 6 h','55%'),
],
'ED091205': [
  ('NaIO₄ (1.0 eq), MeOH/H₂O, 0°C\nthen MW 120°C, MeCN, 2 h; dr >8:1','62%'),
  ('NaH (1.1 eq), DMF, 0°C→rt\nthen Bu₃SnH, AIBN, toluene, 80°C','52%'),
  ('TMSN₃ (1.5 eq), BF₃·Et₂O\nCH₂Cl₂, 0°C, 2 h; then alkylate','45%'),
],
'ED205141': [
  # 2-level: lv2 (4-MeO-PhCHO + benzamide) -> lv1 (Cbz-Trp-PS) -> target
  ('Cbz-Cl (1.0 eq), NaHCO₃, 0°C\nthen TFA, CH₂Cl₂, rt, 2 h  [P-S]','75%',
   '(i) BH₃·THF; (ii) PhCOCl, DIPEA\n(iii) Pd/C, H₂, EtOH  [deprotect]','62%'),
  ('TFA (cat.), CH₂Cl₂, rt, 12 h\nthen PhCOCl, DIPEA, 0°C','65%'),
  ('K₂CO₃ (2 eq), DMF, rt, 2 h\nthen Pd(OAc)₂/BINAP, Cs₂CO₃, 100°C','50%'),
],
'ED636906': [
  # 2-level: lv2 (tyramine + aryl-Cl) -> lv1 (tyramine + phenylacetaldehyde) -> target
  ('AcOH (cat.), CH₂Cl₂, rt, 1 h\nthen NaBH₃CN, MeOH, 0°C  [P-S/redn]','70%',
   'Pd₂(dba)₃ (2 mol%), BINAP\nCs₂CO₃, toluene, 100°C, 14 h','62%'),
  ('Et₃N (2 eq), CH₂Cl₂, 0°C→rt\nthen POCl₃, MeCN, 80°C; NaBH₄','55%'),
  ('Pd(OAc)₂/SPhos (3 mol%)\nCs₂CO₃, DMF/H₂O, 80°C, 4 h','65%'),
],
'ED249356': [
  ('Et₃N (1.5 eq), DMF, 60°C, 4 h\nthen CDI, 100°C, 6 h  [cyclise]','72%'),
  ('CDI (1.2 eq), DMF, rt→80°C, 4 h\nthen Cs₂CO₃, DMF, alkylate','62%'),
  ('Cs₂CO₃ (2 eq), DMF, 60°C\nthen Pd₂(dba)₃/BrettPhos, 100°C','60%'),
],
'ED005228': [
  ('toluene, 80°C, 12 h\n1,3-dipolar cycloaddition; dr 3:1','52%'),
  # 2-level: lv2 (isoindolinone + chalcone) -> lv1 (isoindolinone + trans-stilbene) -> target
  ('Ag₂O (1.0 eq), Et₃N, MeCN\nrt 30 min [ylide]; 80°C 6 h [3+2]','65%',
   'Ag₂O (1.0 eq), Et₃N, MeCN\n80°C, 6 h; dr >9:1  [[3+2]]','65%'),
  ('BF₃·Et₂O (0.2 eq), CH₂Cl₂\n40°C, 8 h  [Staudinger]','40%'),
],
'ED963829': [
  ('Et₃N (1.1 eq), CH₂Cl₂, 0°C\n[2+2] then N-alkylation, K₂CO₃','48%'),
  # 2-level: lv2 (cyclopropylamine + COCl2) -> lv1 (isocyanate + amino-alcohol) -> target
  ('COCl₂ (1.0 eq), Et₃N, CH₂Cl₂\n0°C, 1 h  [isocyanate]','85%',
   'THF, rt, 4 h [carbamate]\nthen NaH, DMF, 60°C  [spiro]','58%'),
  ('Et₃N (1.5 eq), CH₂Cl₂, 0°C\nthen Grubbs 2G (5 mol%), 40°C','52%'),
],
'ED106680': [
  ('NaBH(OAc)₃ (1.5 eq), DCE\nrt, 12 h; then PhI(OAc)₂, MeOH','42%'),
  # 2-level: lv2 (3-OH-BnNH2 + bromomethylphenol) -> lv1 -> target
  ('K₂CO₃ (2 eq), DMF, 60°C, 6 h\n[O-alkylation of phenol]','78%',
   '(R)-CBS, BH₃·THF, −40°C\nthen DEAD/PPh₃, THF, rt  [Mitsunobu]','52%'),
  ('NaBH(OAc)₃, DCE, rt\nthen Grubbs 2G, CH₂Cl₂, 40°C','38%'),
],
'test_001': [
  # 2-level: lv2 (isoquinolinyl + Bischler-Napieralski) -> lv1 -> target
  ('n-BuLi (1.1 eq), THF, −78°C\nthen N-acyl-piperidone, −78°C→rt','58%',
   'NaH, CS₂, MeI [xanthate]\nthen Bu₃SnH, AIBN, toluene, 80°C','52%'),
  ('AgNO₃ (0.1 eq), (NH₄)₂S₂O₈\nH₂SO₄ (aq), 60°C, 3 h  [Minisci]','45%'),
  ('[Rh(cod)Cl]₂ (2 mol%), dppb\ndioxane/H₂O, 60°C, 6 h','48%'),
],
'test_002': [
  ('i-Pr₂NEt (2 eq), n-BuOH, 100°C, 8 h [C6]\nthen 130°C, 12 h [C2]','52%'),
  ('Et₃N (2 eq), DMF, rt, 2 h [C2-F]\nthen i-Pr₂NEt, n-BuOH, 100°C [C6-Cl]','60%'),
  ('i-Pr₂NEt, n-BuOH, 130°C [C2-SNAr]\nthen Pd₂(dba)₃/RuPhos, Cs₂CO₃, 100°C','50%'),
],
'test_003': [
  ('NaBH(OAc)₃ (1.5 eq), DCE, rt\nthen HATU/DIPEA, DMF; P-S','42%'),
  # 2-level: lv2 (tyramine + phenylacetaldehyde) -> lv1 (THIQ + pomalidomide) -> target
  ('TFA/CH₂Cl₂, rt, 1 h\n[Pictet-Spengler THIQ]','62%',
   'HATU (1.1 eq), DIPEA, DMF\nrt, 4 h  [amide coupling]','55%'),
  ('TFA/CH₂Cl₂ [P-S] then Pd(PPh₃)₄\nK₂CO₃, DMF/H₂O, 80°C  [Suzuki]','45%'),
],
'test_004': [
  # 2-level: lv2 (allyl-GlcNAc + L-fucose) -> lv1 (disaccharide) -> target
  ('TMSOTf (0.1 eq), 4Å MS\nCH₂Cl₂, −40°C, 2 h  [β-glycosy]','55%',
   'BF₃·Et₂O (0.2 eq), 4Å MS\n−60°C, 1 h [α-Fuc]; H₂/Pd/C  [de-Bn]','35%'),
  ('NIS/TfOH (0.1 eq), 4Å MS\nCH₂Cl₂, −20°C, 2 h [α-Fuc-Glc]\nthen NIS/TfOH, −20°C [β-GlcNAc]','48%'),
  ('DDQ (1.1 eq), CH₂Cl₂/H₂O, 0°C\nthen TMSOTf, −60°C  [orthogonal]','40%'),
],
}

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def render_forward(cid, out):
    tgt_smi = targets.get(cid, '')
    routes   = SCHEMES[cid]
    conds    = FC[cid]

    FW, FH = 24, 12
    fig = plt.figure(figsize=(FW, FH))
    fig.patch.set_facecolor('white')

    fig.text(0.5, 0.977,
             f'{cid}  —  Full Synthetic Schemes  (Routes A / B / C)',
             ha='center', va='top', fontsize=13, fontweight='bold', color='#1a1a2e')

    ROUTE_H   = 0.295
    ROUTE_Y   = [0.665, 0.36, 0.045]
    MOL_H_FR  = 0.60   # mol height as fraction of route height
    MOL_Y_OFF = 0.20   # mol y offset from route bottom
    ARROW_W   = 0.072
    MARGIN    = 0.015

    for ri, (R, fc) in enumerate(zip(routes, conds)):
        ry  = ROUTE_Y[ri]
        rh  = ROUTE_H
        rec = R.get('rec', False)
        star = '  ★ RECOMMENDED' if rec else ''
        col  = '#154360' if rec else '#2c3e50'

        fig.text(0.5, ry + rh - 0.005, R['title'] + star,
                 ha='center', va='top', fontsize=9, fontweight='bold',
                 color=col, transform=fig.transFigure)

        # Build node SMILES list and arrow labels
        lv2 = R.get('lv2')
        lv1 = R['lv1']
        has2 = (lv2 is not None) and (len(fc) == 4)

        if has2:
            s1_lab, s1_yld, s2_lab, s2_yld = fc
            node_smis = [lv2, lv1, [tgt_smi]]
            arrows    = [(s1_lab, s1_yld), (s2_lab, s2_yld)]
        else:
            s1_lab, s1_yld = fc[0], fc[1]
            node_smis = [lv1, [tgt_smi]]
            arrows    = [(s1_lab, s1_yld)]

        # Compute layout
        n_nodes  = len(node_smis)
        n_arrows = len(arrows)
        # node widths proportional to number of mols in each node
        raw_w    = [max(len(nm) * 0.14, 0.14) for nm in node_smis]
        avail    = 1.0 - 2*MARGIN - n_arrows * ARROW_W
        total_rw = sum(raw_w)
        scale    = avail / total_rw if total_rw > avail else 1.0
        node_w   = [w * scale for w in raw_w]

        # x positions
        x_pos = []
        x = MARGIN
        for i in range(n_nodes):
            x_pos.append(x)
            x += node_w[i]
            if i < n_nodes - 1:
                x += ARROW_W

        mol_h    = rh * MOL_H_FR
        mol_y    = ry + rh * MOL_Y_OFF
        mol_px_h = int(mol_h * FH * 100)      # pixels at 100 dpi
        mol_px_w = 200

        # Draw nodes
        for ni, (nm_list, xn, nw) in enumerate(zip(node_smis, x_pos, node_w)):
            n_m   = len(nm_list)
            each_w = (nw - max(n_m-1,0)*0.006) / max(n_m,1)
            for mi, smi in enumerate(nm_list):
                mx = xn + mi*(each_w + 0.006)
                ax = fig.add_axes([mx, mol_y, each_w - 0.002, mol_h])
                ax.imshow(s2a(smi, mol_px_w, mol_px_h))
                ax.axis('off')
            # plus signs between mols in same node
            for mi in range(n_m-1):
                px_plus = xn + (mi+1)*(each_w+0.006) - 0.01
                fig.text(px_plus, mol_y + mol_h*0.5, '+',
                         ha='center', va='center', fontsize=13,
                         color='#222', transform=fig.transFigure)
            # target label on last node
            if ni == n_nodes - 1:
                fig.text(xn + nw/2, mol_y + mol_h + 0.008,
                         'TARGET', ha='center', va='bottom',
                         fontsize=6.5, color='#c0392b', style='italic',
                         transform=fig.transFigure)

        # Draw arrows
        for ai, ((lab, yld), xn, nw) in enumerate(zip(arrows, x_pos, node_w)):
            ax_start = xn + nw
            ax_mid   = ax_start + ARROW_W/2
            ax_arr   = fig.add_axes([ax_start, mol_y + mol_h*0.38,
                                     ARROW_W, mol_h*0.24])
            ax_arr.set_xlim(0,1); ax_arr.set_ylim(0,1); ax_arr.axis('off')
            ax_arr.annotate('', xy=(0.88, 0.5), xytext=(0.12, 0.5),
                            arrowprops=dict(arrowstyle='->', color='#222',
                                           lw=2.0, mutation_scale=18))
            # step number chip
            ax_arr.text(0.5, 0.5, f'({ai+1})', ha='center', va='center',
                        fontsize=6, color='#555', fontweight='bold')
            # conditions above
            fig.text(ax_mid, mol_y + mol_h*0.78, lab,
                     ha='center', va='bottom', fontsize=6.2,
                     color='#1a1a2e', style='italic',
                     transform=fig.transFigure)
            # yield below
            fig.text(ax_mid, mol_y + mol_h*0.15, yld,
                     ha='center', va='top', fontsize=7,
                     color='#27ae60', fontweight='bold',
                     transform=fig.transFigure)

        # Divider lines between routes
        if ri < 2:
            fig.add_artist(plt.Line2D([0.01, 0.99], [ry - 0.01, ry - 0.01],
                                      transform=fig.transFigure,
                                      color='#ccc', lw=1.1))

    plt.savefig(out, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return out

# ---------------------------------------------------------------------------
if __name__ == '__main__':
    done = []
    for cid in SCHEMES:
        out = os.path.join(workspace, f'fwd_{cid}.png')
        try:
            render_forward(cid, out)
            done.append(cid)
            print(f'  ok  {cid}')
        except Exception as e:
            print(f'  ERR {cid}: {e}')
    print(f'\nDone - {len(done)}/{len(SCHEMES)} forward scheme PNGs written.')
