
import html as H

# ─── SMILES data (same as before, cache already built) ───────────────────────
COMPOUNDS = [
  { 'id': 'MCUF651', 'full_name': 'MCUF651',
    'target_smiles': 'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended',
        'strategic': 'Amide N–C(O) then piperidine N-alkylation',
        'steps': [
          ('mol','O=C(O)[C@H]1CCCNC1','(R)-Nipecotic acid','sm'),
          ('arrow',['HATU (1.1 eq), DIPEA (3 eq)','+ 4,6-Difluoroindol-2-amine'],'DMF, 0 °C → RT, 12 h','75–85%'),
          ('mol','O=C([C@H]1CCCNC1)Nc1cc2cc(F)cc(F)c2[nH]1','Amide intermediate','int'),
          ('arrow',['K₂CO₃ (2 eq)','+ 2-Bromo-N,N-dimethylethylamine (1.1 eq)'],'MeCN, 60 °C, 8 h','65–80%'),
          ('mol','CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1','MCUF651','prod'),
        ]},
    ]},
  { 'id': 'A317', 'full_name': 'A317',
    'target_smiles': 'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended · Hantzsch',
        'strategic': 'Hantzsch thiazole C4–C from carbonyl C of α-bromo ketone; then amide N–C(O)',
        'steps': [
          ('mol','CC(=O)[C@@H]1CCCN1','(S)-2-Acetylpyrrolidine','sm'),
          ('arrow',['CuI (10 mol%), K₃PO₄ (2 eq)','+ 2-Bromopyridine'],'DMSO, 110 °C, 12 h','60–75%'),
          ('mol','CC(=O)[C@@H]1CCCN1c1ccccn1','1-(Pyridin-2-yl)prolinoyl\nmethyl ketone','int'),
          ('arrow',['NBS (1.1 eq)'],'AcOH / CHCl₃, 0 °C → RT','80–90%'),
          ('mol','O=C(CBr)[C@@H]1CCCN1c1ccccn1','α-Bromo ketone','int'),
          ('arrow',['Thiourea (1.1 eq)'],'EtOH, reflux, 2 h','70–80%'),
          ('mol','Nc1nc([C@@H]2CCCN2c2ccccn2)cs1','4-(Pyrrolidinyl)-2-\naminothiazole','int'),
          ('arrow',['HATU (1.1 eq), DIPEA (3 eq)','+ 1-(4-Picolyl)pyrrole-2-COOH'],'DMF, RT, 12 h','65–75%'),
          ('mol','O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1','A317','prod'),
        ]},
      { 'label': 'Route 2', 'tag': 'Independent · Suzuki',
        'strategic': 'C4–C(aryl) of thiazole via Pd-catalysed Suzuki coupling',
        'steps': [
          ('mol','Nc1nc(Br)cs1','4-Bromo-2-aminothiazole','sm'),
          ('arrow',['Pd(dppf)Cl₂ (5 mol%), K₂CO₃','+ (R)-Pyrrolidinyl boronate pinacol ester'],'dioxane/H₂O, 90 °C, 12 h','65–75%'),
          ('mol','Nc1nc([C@@H]2CCCN2c2ccccn2)cs1','4-(Pyrrolidinyl)-2-\naminothiazole','int'),
          ('arrow',['HATU (1.1 eq), DIPEA (3 eq)','+ 1-(4-Picolyl)pyrrole-2-COOH'],'DMF, RT, 12 h','65–75%'),
          ('mol','O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1','A317','prod'),
        ]},
    ]},
  { 'id': '8008', 'full_name': '8008',
    'target_smiles': 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#Cc3cncc(C(=O)OC)c3)nc2c1O',
    'routes': [
      { 'label': 'Route 1', 'tag': 'Recommended · Sulfonylation + 2× Sonogashira',
        'strategic': 'Sulfonamide N–S bond; O-alkylation; two sequential Sonogashira sp–sp² couplings',
        'steps': [
          ('mol','O=S(=O)(Cl)c1cnc2cccnc2c1O','Naphthyridinol sulfonyl chloride','sm'),
          ('arrow',['4-Chloroaniline (1.0 eq), Et₃N (2 eq)'],'CH₂Cl₂, 0 °C → RT, 4 h','75–85%'),
          ('mol','O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2cccnc2c1O','Sulfonamide (OH free)','int'),
          ('arrow',['EtI (1.5 eq), K₂CO₃ (2 eq)'],'DMF, 60 °C, 6 h','85–92%'),
          ('mol','O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC)nc2c1O','O-Ethyl sulfonamide','int'),
          ('arrow',['Pd(PPh₃)₄ (5 mol%), CuI (10 mol%)','TMS-acetylene (1.5 eq), Et₃N','then K₂CO₃/MeOH (TMS removal)'],'DMF, 50 °C, 8 h','75–85%'),
          ('mol','O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#C)nc2c1O','Terminal alkyne','int'),
          ('arrow',['Pd(PPh₃)₄ (5 mol%), CuI (10 mol%)','+ Methyl 5-bromonicotinate (1.2 eq), Et₃N'],'DMF, 50 °C, 12 h','75–85%'),
          ('mol','O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#Cc3cncc(C(=O)OC)c3)nc2c1O','8008','prod'),
        ]},
    ]},
  { 'id': '7977', 'full_name': '7977',
    'target_smiles': 'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended · CDI cyclization',
        'strategic': 'CDI closes imidazo[4,5-c]pyridinone ring on diaminopyridine; N-alkylation then Suzuki',
        'steps': [
          ('mol','Cc1cnc(Br)cc1N','3-Amino-5-bromo-4-methylpyridine','sm'),
          ('arrow',['Fe (5 eq), AcOH (cat.)','+ 3-Bromo-4-nitropyridine'],'EtOH/H₂O, 80 °C, 4 h','75–85%'),
          ('mol','Cc1cnc(Br)cc1Nc1cnccc1','Diaminopyridine\n(5-bromo retained)','int'),
          ('arrow',['CDI (1.0 eq)'],'DMF, 80 °C, 4 h','70–80%'),
          ('mol','O=c1[nH]c2cnccc2n1CC(N)=O','Imidazo[4,5-c]pyridinone\n(N-H, bromo present)','int'),
          ('arrow',['ClCH₂C(=O)NH₂ (1.1 eq), K₂CO₃ (2 eq)'],'DMF, 60 °C, 6 h','70–80%'),
          ('mol','O=c1[nH]c2cnccc2n1CC(N)=O','N-Chloroacetamide adduct','int'),
          ('arrow',['Pd(dppf)Cl₂ (5 mol%), K₂CO₃','+ 2-Cl-4-F-phenylboronic acid (1.5 eq)'],'dioxane/H₂O, 85 °C, 12 h','75–85%'),
          ('mol','Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21','7977','prod'),
        ]},
    ]},
  { 'id': '7877', 'full_name': '7877  (furo[2,3-b]pyridine — corrected)',
    'target_smiles': 'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1',
    'routes': [
      { 'label': 'Route 2', 'tag': 'Recommended · Lautens 5-exo-dig',
        'strategic': 'Furan ring O–C2 and C3–C3(pyr) bonds formed together in one Pd/Cu 5-exo-dig cyclization',
        'steps': [
          ('mol','Oc1ncccc1Br','3-Bromo-2-hydroxypyridine','sm'),
          ('arrow',['K₂CO₃ (2 eq)','+ BrCH₂C≡C-Ar (propargyl bromide, Ar = 4-COOMe-2-cyclopentylphenyl)'],'DMF, RT, 12 h\n(O-propargylation)','85–90%'),
          ('mol','BrCC#Cc1ccc(C(=O)OC)c(C2CCCC2)c1','Propargyl ester\nbromide (co-SM)','sm'),
          ('arrow',['PdCl₂ (5 mol%), CuI (10 mol%)','Cs₂CO₃ (2 eq)'],'DMF, 80 °C, 12 h\n(5-exo-dig ring closure)','55–70%'),
          ('mol','COC(=O)c1ccc(-c2coc3ncccc23)cc1C1CCCC1','3-Bromo-5-aryl-furo[2,3-b]pyridine\nmethyl ester','int'),
          ('arrow',['m-Tolylboronic acid (1.5 eq)','Pd(dppf)Cl₂ (5 mol%), K₂CO₃'],'dioxane/H₂O, 90 °C, 12 h','70–80%'),
          ('mol','Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)OC)c(C5CCCC5)c4)c3c2)c1','Methyl ester\nintermediate','int'),
          ('arrow',['LiOH (3 eq)'],'THF/H₂O, RT, 4 h','≥95%'),
          ('mol','Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1','7877','prod'),
        ]},
      { 'label': 'Route 3', 'tag': 'Independent · Majumdar cyclodehydration',
        'strategic': 'Furan ring formed by tandem K₂CO₃-mediated O-alkylation / intramolecular Knoevenagel on 2-hydroxypyridine-3-carbaldehyde',
        'steps': [
          ('mol','O=Cc1cnc(Br)cc1O','3-Formyl-5-bromo-\n2-hydroxypyridine','sm'),
          ('arrow',['m-TolBpin (1.5 eq), Pd(dppf)Cl₂','K₂CO₃, dioxane/H₂O, 80 °C; then KOH/H₂O'],'Suzuki + 2-Cl→2-OH hydrolysis','65–75%'),
          ('mol','O=Cc1cnc(-c2cccc(C)c2)cc1O','3-Formyl-5-(m-tolyl)-\n2-hydroxypyridine','int'),
          ('arrow',['K₂CO₃ (2 eq)','+ BrCH₂CO-Ar(cyclopentyl, methyl ester)'],'DMF, 80 °C, 6 h\n(tandem O-alkyl / Knoevenagel ring closure)','45–60%'),
          ('mol','Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)OC)c(C5CCCC5)c4)c3c2)c1','Methyl ester\nintermediate','int'),
          ('arrow',['LiOH (3 eq)'],'THF/H₂O, RT, 4 h','≥95%'),
          ('mol','Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1','7877','prod'),
        ]},
    ]},
  { 'id': 'B54', 'full_name': 'B54',
    'target_smiles': 'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended · Hantzsch + Aldol',
        'strategic': 'MnO₂ oxidation → crossed aldol → α-bromination → Hantzsch thiazole → amide coupling (5 steps, all SM commercial)',
        'steps': [
          ('mol','OCc1cn(C2CCCCC2)cn1','(1-Cyclohexylimidazol-4-yl)\nmethanol','sm'),
          ('arrow',['MnO₂ (5 eq, activated)'],'CH₂Cl₂, RT, 4 h','85–92%'),
          ('mol','O=Cc1cn(C2CCCCC2)cn1','(1-Cyclohexylimidazol-4-yl)\ncarbaldehyde','int'),
          ('arrow',['Acetone (5 eq), NaOH 10%'],'EtOH/H₂O, RT, 2 h','60–70%'),
          ('mol','CC(=O)C=Cc1cn(C2CCCCC2)cn1','(E)-4-(1-Cyclohexylimidazol-4-yl)\nbut-3-en-2-one','int'),
          ('arrow',['NBS (1.1 eq), AcOH'],'CHCl₃, 0 °C → RT\n(α-bromination, ionic)','75–85%'),
          ('mol','O=C(CBr)C=Cc1cn(C2CCCCC2)cn1','α-Bromo enone','int'),
          ('arrow',['Thiourea NC(N)=S (1.1 eq)'],'EtOH, reflux, 2 h\n(Hantzsch; C=O carbon → C4)','70–80%'),
          ('mol','Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1','2-Amino-4-(vinylimidazoyl)\nthiazole','int'),
          ('arrow',['HATU (1.1 eq), DIPEA (3 eq)','+ 1-(4-Picolyl)pyrrole-2-COOH'],'DMF, RT, 12 h','65–75%'),
          ('mol','O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1','B54','prod'),
        ]},
      { 'label': 'Route 3', 'tag': 'Independent · HWE Olefination',
        'strategic': 'C4=C(vinyl) of thiazole set by HWE olefination on 2-amino-4-formylthiazole',
        'steps': [
          ('mol','Nc1nc(C=O)cs1','2-Amino-4-\nformylthiazole','sm'),
          ('arrow',['(EtO)₂P(O)CH₂-(1-cyclohexylimidazol-4-yl) (1.2 eq)','NaH (1.3 eq)'],'THF, 0 °C → RT, 2 h\n(E-selective HWE)','55–70%'),
          ('mol','Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1','2-Amino-4-(vinylimidazoyl)\nthiazole','int'),
          ('arrow',['HATU (1.1 eq), DIPEA (3 eq)','+ 1-(4-Picolyl)pyrrole-2-COOH'],'DMF, RT, 12 h','65–75%'),
          ('mol','O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1','B54','prod'),
        ]},
    ]},
]

# ─── CSS ─────────────────────────────────────────────────────────────────────
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 13px; background: #f5f5f5; color: #1a1a1a;
  padding: 24px 32px 60px;
}
h1 { font-size: 20px; font-weight: 700; color: #111; margin-bottom: 4px; }
.subtitle { color: #555; font-size: 12px; margin-bottom: 32px; }
nav { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:28px; }
nav a {
  background:#fff; border:1px solid #d0d0d0; border-radius:4px;
  padding:4px 12px; font-size:12px; color:#1558b0; text-decoration:none;
  transition: background .15s;
}
nav a:hover { background:#e8f0fe; }

/* compound section */
.compound-section {
  background:#fff; border:1px solid #ddd; border-radius:8px;
  margin-bottom:28px; overflow:hidden;
}
.compound-header {
  display:flex; align-items:center; justify-content:space-between;
  background:#f0f4ff; padding:14px 20px; border-bottom:1px solid #ddd;
}
.compound-title-block {}
.compound-name { font-size:17px; font-weight:700; color:#12307a; }
.compound-meta { font-size:11px; color:#666; display:block; margin-top:2px; }
.compound-thumb-wrap img { border:1px solid #ccc; border-radius:4px; background:#fff; display:block; }

/* route */
.route-block { padding: 16px 20px 20px; border-bottom:1px solid #eee; }
.route-block:last-child { border-bottom:none; }
.route-header { display:flex; align-items:baseline; gap:10px; margin-bottom:4px; }
.route-label { font-size:14px; font-weight:700; color:#1558b0; }
.route-tag { font-size:11px; background:#e8f0fe; color:#1558b0; border-radius:3px; padding:2px 7px; }
.route-steps { font-size:11px; color:#888; margin-left:auto; }
.route-strategic {
  font-size:11.5px; color:#444; background:#fafafa; border-left:3px solid #b0c4f0;
  padding:5px 10px; margin-bottom:14px; border-radius:0 3px 3px 0;
}

/* scheme row - horizontal scroll */
.scheme-row {
  display:flex; align-items:center; overflow-x:auto; padding:4px 0 8px;
  scrollbar-width:thin; scrollbar-color:#ccc #f5f5f5;
}

/* molecule box */
.mol-box {
  display:flex; flex-direction:column; align-items:center;
  min-width:195px; max-width:195px; flex-shrink:0;
  border:1.5px solid #ccc; border-radius:6px; background:#fff;
  padding:6px 6px 4px; position:relative;
}
.mol-sm    { border-color:#5a8ade; background:#f0f5ff; }
.mol-int   { border-color:#a0a0a0; background:#fafafa; }
.mol-prod  { border-color:#2a8a4a; background:#f0faf2; box-shadow: 0 0 0 2px #2a8a4a40; }

.mol-role-tag {
  position:absolute; top:4px; left:6px; font-size:9.5px; font-weight:700;
  border-radius:2px; padding:1px 5px; letter-spacing:.3px;
}
.tag-sm   { background:#5a8ade22; color:#1558b0; }
.tag-int  { background:#88888822; color:#555; }
.tag-prod { background:#2a8a4a22; color:#1a6b3a; }

.mol-img-wrap { margin-top:14px; }
.mol-img { display:block; }
.mol-err {
  width:175px; height:125px; display:flex; align-items:center; justify-content:center;
  font-size:10px; color:#c00; background:#fff0f0; border:1px dashed #c00;
  word-break:break-all; padding:6px; text-align:center;
}
.mol-name {
  font-size:10.5px; color:#333; text-align:center; margin-top:5px;
  line-height:1.4; min-height:30px; font-style:italic;
}

/* arrow block */
.arrow-block {
  display:flex; flex-direction:column; align-items:center;
  min-width:190px; max-width:220px; flex-shrink:0; padding:0 4px;
}
.arrow-reagents {
  font-size:10.5px; color:#222; text-align:center; line-height:1.45;
  margin-bottom:4px; background:#fffdf0; border:1px solid #e8e0b0;
  border-radius:3px; padding:3px 7px; min-height:28px;
}
.arrow-shaft {
  display:flex; align-items:center; width:100%; margin:2px 0;
}
.arrow-line {
  flex:1; height:2px; background:#444;
}
.arrow-head {
  font-size:16px; color:#444; margin-left:-2px; line-height:1;
}
.arrow-conditions {
  font-size:10px; color:#555; text-align:center; line-height:1.4; margin-top:2px;
}
.arrow-yield {
  font-size:10px; font-weight:700; color:#2a8a4a; margin-top:1px;
}

/* footer */
footer {
  font-size:11px; color:#999; margin-top:24px; text-align:center;
  border-top:1px solid #ddd; padding-top:12px;
}
"""

# ─── HTML builders (inline — no persistent functions) ────────────────────────
def build_html():
    nav_links = ''.join(
        f'<a href="#{c["id"]}">{H.escape(c["id"])}</a>' for c in COMPOUNDS
    )
    sections = []
    for cpd in COMPOUNDS:
        cid  = H.escape(cpd['id'])
        fname = H.escape(cpd['full_name'])
        tgt_b64 = SVG_CACHE.get(cpd['target_smiles'], '')
        tgt_img = (f'<img src="data:image/svg+xml;base64,{tgt_b64}" '
                   f'width="210" height="148" alt="target {cid}">') if tgt_b64 else ''
        n_routes = len(cpd['routes'])
        routes_out = []
        for route in cpd['routes']:
            lbl   = H.escape(route['label'])
            tag   = H.escape(route['tag'])
            strat = H.escape(route['strategic'])
            n_steps = sum(1 for s in route['steps'] if s[0]=='arrow')
            # build scheme row
            parts = []
            for s in route['steps']:
                if s[0] == 'mol':
                    _, smi, name, role = s
                    b64 = SVG_CACHE.get(smi,'')
                    cls = {'sm':'mol-sm','int':'mol-int','prod':'mol-prod'}.get(role,'mol-int')
                    rtag = {'sm':'SM','int':'INT','prod':'★ TARGET'}.get(role,'')
                    rcls = {'sm':'tag-sm','int':'tag-int','prod':'tag-prod'}.get(role,'')
                    if b64:
                        img = (f'<img class="mol-img" src="data:image/svg+xml;base64,{b64}" '
                               f'width="175" height="125" alt="{H.escape(smi[:40])}">')
                    else:
                        img = f'<div class="mol-err">{H.escape(smi[:30])}</div>'
                    nlines = name.replace('\n','<br>')
                    parts.append(
                        f'<div class="mol-box {cls}">'
                        f'<span class="mol-role-tag {rcls}">{rtag}</span>'
                        f'<div class="mol-img-wrap">{img}</div>'
                        f'<div class="mol-name">{nlines}</div></div>'
                    )
                elif s[0] == 'arrow':
                    _, reagents, conditions, yld = s
                    reag_h = '<br>'.join(H.escape(r) for r in reagents)
                    cond_h = H.escape(conditions).replace('\n','<br>')
                    parts.append(
                        f'<div class="arrow-block">'
                        f'<div class="arrow-reagents">{reag_h}</div>'
                        f'<div class="arrow-shaft"><div class="arrow-line"></div>'
                        f'<div class="arrow-head">▶</div></div>'
                        f'<div class="arrow-conditions">{cond_h}</div>'
                        f'<div class="arrow-yield">{H.escape(yld)}</div>'
                        f'</div>'
                    )
            scheme = f'<div class="scheme-row">{"".join(parts)}</div>'
            routes_out.append(
                f'<div class="route-block">'
                f'<div class="route-header">'
                f'<span class="route-label">{lbl}</span>'
                f'<span class="route-tag">{tag}</span>'
                f'<span class="route-steps">{n_steps} step{"s" if n_steps!=1 else ""}</span>'
                f'</div>'
                f'<div class="route-strategic">Key disconnection: {strat}</div>'
                f'{scheme}</div>'
            )
        sections.append(
            f'<section class="compound-section" id="{cid}">'
            f'<div class="compound-header">'
            f'<div class="compound-title-block">'
            f'<h2 class="compound-name">{fname}</h2>'
            f'<span class="compound-meta">{n_routes} route{"s" if n_routes!=1 else ""} shown — scroll →</span>'
            f'</div>'
            f'<div class="compound-thumb-wrap">{tgt_img}</div>'
            f'</div>'
            f'{"".join(routes_out)}'
            f'</section>'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Synthetic Schemes — Phase 1 Analysis</title>
<style>{CSS}</style>
</head>
<body>
<h1>Synthetic Schemes — Phase 1 Retrosynthetic Analysis</h1>
<p class="subtitle">Input: <em>Projets Custom.sdf</em> (researcher-supplied, 7 compounds).
AiZynthFinder (uspto policy, gpu=True). Generated 2026-09-02.
Three CRITICAL errors corrected per independent audit: see <em>retrosynthesis_phase1_corrected.md</em>.</p>
<nav>{nav_links}</nav>
{"".join(sections)}
<footer>Structures rendered with RDKit. Reagents above arrow · Conditions &amp; yield below arrow.
SM = starting material · INT = intermediate · ★ TARGET = final product.</footer>
</body>
</html>"""

page = build_html()
out_path = '/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/synthetic_schemes.html'
with open(out_path, 'w') as f:
    f.write(page)
size_kb = len(page) / 1024
print(f"Written: {out_path}")
print(f"File size: {size_kb:.1f} KB")
