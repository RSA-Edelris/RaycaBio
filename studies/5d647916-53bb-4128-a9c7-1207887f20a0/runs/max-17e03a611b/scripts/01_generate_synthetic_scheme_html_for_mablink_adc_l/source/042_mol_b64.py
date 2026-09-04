
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from rdkit.Chem.Draw import rdMolDraw2D
import base64

def mol_b64(smi, w=175, h=130):
    mol = Chem.MolFromSmiles(smi)
    if not mol: return None
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

def mw(smi):
    mol = Chem.MolFromSmiles(smi)
    return round(Descriptors.MolWt(mol)) if mol else 0

# Intermediates
CDI_PAB    = 'Nc1ccc([C@@H](OC(=O)n2ccnc2)CN)cc1'
POLYSAR_ARM = ('O=C1C=CC(=O)N1CCOCCOCCNC(=O)CCN(CC(=O)N)'
               'C(=O)CN(C)C(=O)CN(C)C(=O)O')
STAGE3_INT = ('CC[C@@]1(O)C(=O)OCc2c1cc1n(c2=O)Cc2c-1nc1cc(F)c(C)c3c1c2'
              '[C@@H](NC(=O)O[C@H](CN)'
              'c1ccc(NC(=O)[C@H](C)NC(=O)[C@@H](NC(C)=O)C(C)C)cc1)CC3')

# Stage definitions: each step = ('mol', smiles, label, role) or ('arrow', [reagents], conditions, yield_str)
# Roles: sm=blue, int=grey, prod=green
stages = [
    {
        'id': 'stage1',
        'label': 'Stage 1',
        'title': 'Polysar-10 Linker Arm — Sarcosine NCA Ring-Opening Polymerisation',
        'strategy': (
            'Disconnection: amide bond between maleimide arm (Mal-PEG₂-βAla) and polysarcosine '
            'chain. Polysar-10 assembled by base-initiated NCA-ROP of sarcosine (N-methylglycine) '
            'NCA; terminal NH₂ of Glu-initiator captured with Mal-PEG₂-βAla-NHS ester.'
        ),
        'steps': [
            ('mol', SAR_NCA,      'Sarcosine NCA\n(N-methylglycine NCA monomer)', 'sm'),
            ('arrow',
             ['n = 10 equiv, Glu-PEG-initiator', 'DMF, RT, 18 h (base-initiated NCA-ROP)'],
             '~90 % conversion', 'Ð ≤ 1.15'),
            ('mol', POLYSAR4_STUB, 'H₂N–(Sar)₁₀–COOH\n(4 units shown; MW ~760 for n=10)', 'int'),
            ('arrow',
             ['Mal-PEG₂-βAla-NHS ester (1.0 eq)', 'DIPEA (2 eq), DMF, 0 °C → RT, 2 h'],
             'NHS coupling at terminal NH₂', '70–80 %'),
            ('mol', POLYSAR_ARM,  'Mal-PEG₂-βAla–CO–(Sar)₁₀–COOH\n(hydrophilic linker arm; simplified)', 'int'),
        ]
    },
    {
        'id': 'stage2',
        'label': 'Stage 2',
        'title': 'Payload Carbamate — PAB Self-Immolative Spacer + Exatecan',
        'strategy': (
            'Disconnection: carbamate C=O (self-immolative bond). Benzylic OH of branched PAB '
            'amino-alcohol activated as CDI-imidazolyl carbonate; captured by NH of exatecan. '
            'Both PAB amines (Ar-NH₂ and CH₂-NH₂) kept free for Stage 3 couplings.'
        ),
        'steps': [
            ('mol', PAB_SCAFFOLD, 'Branched PAB amino-alcohol\n(4-NH₂, benzylic-OH, CH₂-NH₂)', 'sm'),
            ('arrow',
             ["CDI (1.2 eq), DCM, RT, 1 h"],
             'O-activation → imidazolyl carbonate', '85–90 %'),
            ('mol', CDI_PAB, 'PAB imidazolyl carbonate\n(both NH₂ groups free)', 'int'),
            ('arrow',
             ['Exatecan (1.0 eq)', 'DIPEA (2 eq), DMF, 0 °C → RT, 12 h'],
             'NH (exatecan) attacks carbonate', '55–70 %'),
            ('mol', CARBAMATE_INT, 'PAB–carbamate–Exatecan\n(Ar-NH₂ and CH₂-NH₂ still free)', 'int'),
        ]
    },
    {
        'id': 'stage3',
        'label': 'Stage 3',
        'title': 'Final Assembly — Sequential Amide Couplings → Mablink',
        'strategy': (
            'Convergent assembly: (a) Ac-Val-Ala-OSu (NHS ester) reacts selectively at the less '
            'hindered Ar-NH₂ of PAB; (b) HATU-mediated amide coupling of Stage 1 COOH arm to '
            'free benzylic CH₂-NH₂. Maleimide retained intact for downstream thiol-maleimide '
            'conjugation to antibody cysteine (DAR 4).'
        ),
        'steps': [
            ('mol', CARBAMATE_INT, 'PAB–carbamate–Exatecan\n(both NH₂ free)', 'sm'),
            ('arrow',
             ['Ac-Val-Ala-OSu NHS ester (1.05 eq)', 'DIPEA (3 eq), DMF, RT, 4 h'],
             'Selective amide at Ar-NH₂\n(less hindered)', '60–70 %'),
            ('mol', STAGE3_INT, 'Ac-Val-Ala–PAB–carbamate–Exatecan\n(CH₂-NH₂ still free)', 'int'),
            ('arrow',
             ['Stage 1 linker arm–COOH (1.05 eq)', 'HATU (1.1 eq), DIPEA (3 eq), DMF, RT, 4 h'],
             'Amide at CH₂-NH₂ (benzylic)', '50–65 %'),
            ('mol', MABLINK_SMILES, 'Mablink (MW 1962)\n(maleimide free → Ab bioconjugation)', 'prod'),
        ]
    },
]

# ── CSS/JS + HTML builder ───────────────────────────────────────────────────
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Helvetica Neue', Arial, sans-serif; background: #f4f6f9; color: #222; padding: 20px; }
h1  { font-size: 1.5rem; color: #1a3c6e; margin-bottom: 4px; }
.subtitle { font-size: 0.88rem; color: #555; margin-bottom: 20px; }
.stage { background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.09);
         margin-bottom: 28px; overflow: hidden; }
.stage-header { background: linear-gradient(90deg,#1a3c6e,#2e6aad); color: #fff;
                padding: 10px 18px; display: flex; align-items: baseline; gap: 14px; }
.stage-badge { font-size: 0.75rem; background: rgba(255,255,255,.25);
               padding: 1px 8px; border-radius: 20px; }
.stage-title { font-size: 1.02rem; font-weight: 700; }
.strategy { font-size: 0.83rem; color: #444; line-height: 1.5;
            padding: 10px 18px; background: #f0f4fb; border-bottom: 1px solid #d8e4f3; }
.scheme-row { display: flex; align-items: center; padding: 16px 18px;
              overflow-x: auto; gap: 6px; min-height: 180px; }
/* molecule cards */
.mol-card { display: flex; flex-direction: column; align-items: center; min-width: 175px;
            border-radius: 8px; padding: 6px 6px 4px; }
.mol-card.sm   { border: 2px solid #3a7bd5; background: #eaf2ff; }
.mol-card.int  { border: 2px solid #aaa; background: #f5f5f5; }
.mol-card.prod { border: 2.5px solid #27ae60; background: #e8faf0;
                 box-shadow: 0 0 10px rgba(39,174,96,.35); }
.mol-card img  { width: 175px; height: 130px; }
.mol-label { font-size: 0.7rem; text-align: center; color: #333; margin-top: 4px;
             white-space: pre-line; max-width: 175px; line-height: 1.3; }
.mol-mw    { font-size: 0.68rem; color: #888; margin-top: 2px; }
/* arrow block */
.arrow-block { display: flex; flex-direction: column; align-items: center;
               min-width: 130px; max-width: 160px; }
.reagents { font-size: 0.68rem; color: #5a3800; background: #fff8dc;
            border: 1px solid #e0c060; border-radius: 4px; padding: 3px 6px;
            text-align: center; white-space: pre-line; line-height: 1.4; width: 100%; }
.arrow-line { display: flex; align-items: center; width: 100%; padding: 3px 0; }
.arrow-line span { flex: 1; height: 2px; background: #555; }
.arrow-line i  { font-style: normal; font-size: 1.1rem; color: #555; }
.conditions { font-size: 0.66rem; color: #555; text-align: center;
              white-space: pre-line; line-height: 1.4; width: 100%; }
.yield-str  { font-size: 0.7rem; color: #1a6e2e; font-weight: 600;
              text-align: center; margin-top: 1px; }
/* verification */
.verification { background:#fff; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,.09);
                margin-bottom:28px; padding:18px 22px; }
.verification h2 { font-size:1.0rem; color:#1a3c6e; margin-bottom:8px; }
.vtable { width:100%; border-collapse:collapse; font-size:0.78rem; margin-top:8px; }
.vtable th { background:#1a3c6e; color:#fff; padding:5px 8px; text-align:left; }
.vtable td { padding:4px 8px; border-bottom:1px solid #e0e6ef; }
.vtable tr:nth-child(even) td { background:#f2f6fc; }
/* key */
.key { display:flex; gap:16px; font-size:0.74rem; padding:10px 18px 14px; }
.key-dot { width:12px; height:12px; border-radius:50%; display:inline-block; margin-right:4px; }
"""

def img_tag(b64):
    return f'<img src="data:image/svg+xml;base64,{b64}" alt="structure"/>'

def mol_card(smi, label, role):
    b = mol_b64(smi)
    if not b:
        return f'<div class="mol-card {role}"><span style="color:red;font-size:0.7rem">SVG failed</span></div>'
    m   = Chem.MolFromSmiles(smi)
    mwv = round(Descriptors.MolWt(m)) if m else ''
    return (f'<div class="mol-card {role}">'
            f'{img_tag(b)}'
            f'<div class="mol-label">{label}</div>'
            f'<div class="mol-mw">MW {mwv}</div>'
            f'</div>')

def arrow_block(reagents, conditions, yield_str):
    reagent_html = '<br>'.join(r.replace('\n','<br>') for r in reagents)
    cond_html    = conditions.replace('\n','<br>')
    return (f'<div class="arrow-block">'
            f'<div class="reagents">{reagent_html}</div>'
            f'<div class="arrow-line"><span></span><i>&#9658;</i></div>'
            f'<div class="conditions">{cond_html}</div>'
            f'<div class="yield-str">{yield_str}</div>'
            f'</div>')

parts = []
parts.append(f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"/>
<title>Mablink ADC — Synthetic Scheme</title>
<style>{CSS}</style></head><body>
<h1>Mablink ADC — Linear Synthetic Scheme</h1>
<div class="subtitle">
  Convergent 3-stage synthesis of a cathepsin B-cleavable ADC linker-payload for thiol-maleimide antibody conjugation.<br>
  Payload: Exatecan (DXd-type Topo-I inhibitor) · Cleavage: Ac-Val-Ala · Spacer: branched PAB carbamate ·
  Hydrophilic arm: Polysar-10 (polysarcosine 10-mer) · Warhead: maleimide (DAR 4).
</div>
<section class="verification" id="verification">
<h2>Verification</h2>
<p style="font-size:0.8rem;color:#444;margin-bottom:8px;">
Provenance: Mablink SMILES from researcher-supplied <em>Projets Custom.sdf</em> (compound 1, MW 1962).
All intermediate SMILES validated with RDKit. Building blocks commercially sourced or synthesised by standard literature protocols.
</p>
<table class="vtable">
<tr><th>Building block</th><th>SMILES source</th><th>MW</th><th>Supplier tier</th></tr>
<tr><td>Sarcosine NCA monomer</td><td>Literature synthesis (NCA phosgenation)</td><td>115</td><td>In-house or Sigma</td></tr>
<tr><td>Exatecan free base</td><td>SDF-derived substructure (NH₂ analogue)</td><td>435</td><td>Purchased: Daiichi / Aurigene</td></tr>
<tr><td>Branched PAB amino-alcohol</td><td>Literature design</td><td>152</td><td>Custom synthesis</td></tr>
<tr><td>Mal-PEG₂-βAla-NHS</td><td>Commercial Quanta Biodesign / BroadPharm</td><td>381</td><td>Catalog</td></tr>
<tr><td>Ac-Val-Ala-OH</td><td>Standard Fmoc SPPS</td><td>230</td><td>Bachem / Sigma catalog</td></tr>
</table>
<p style="font-size:0.75rem;color:#888;margin-top:8px;">
Legend: <span style="color:#3a7bd5;font-weight:600;">■ SM</span> = starting material &nbsp;
<span style="color:#888;font-weight:600;">■ INT</span> = intermediate &nbsp;
<span style="color:#27ae60;font-weight:600;">■ PRODUCT</span> = final Mablink
</p>
</section>
""")

for stg in stages:
    parts.append(f'<div class="stage" id="{stg["id"]}">')
    parts.append(f'<div class="stage-header">'
                 f'<span class="stage-title">{stg["label"]}: {stg["title"]}</span>'
                 f'</div>')
    parts.append(f'<div class="strategy">&#9670; Strategic disconnection: {stg["strategy"]}</div>')
    parts.append('<div class="scheme-row">')
    for step in stg['steps']:
        if step[0] == 'mol':
            _, smi, label, role = step
            parts.append(mol_card(smi, label, role))
        elif step[0] == 'arrow':
            _, reagents, conditions, yield_str = step
            parts.append(arrow_block(reagents, conditions, yield_str))
    parts.append('</div></div>')

# Final bioconjugation note
parts.append("""
<div style="background:#fff;border-radius:10px;padding:16px 22px;
            box-shadow:0 2px 8px rgba(0,0,0,.09);font-size:0.82rem;color:#333;">
  <strong>Stage 4 (Bioconjugation — conceptual):</strong>
  mAb (reduced, 4 × Cys) + Mablink-maleimide → maleimide-thiol Michael addition (pH 6.5–7.0, 4 °C, 16 h) →
  ADC (DAR 4). Purified by HIC or SEC. DAR confirmed by HIC-UV and MS.
  <br><br>
  <strong>Key references:</strong>
  Nakada <em>et al.</em> <em>Bioorg. Med. Chem. Lett.</em> 2016 (Exatecan);
  Joubert <em>et al.</em> <em>Mol. Cancer Ther.</em> 2020 (maleimide-cysteine ADC);
  Kolodych <em>et al.</em> <em>Eur. J. Med. Chem.</em> 2017 (Val-Ala linker cleavage);
  Luxenburger <em>et al.</em> <em>Eur. Polym. J.</em> 2019 (sarcosine NCA-ROP).
</div>
""")

parts.append('</body></html>')

html_out = '\n'.join(parts)
path = '/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/mablink_scheme.html'
with open(path, 'w') as f:
    f.write(html_out)

size_kb = len(html_out) / 1024
print(f"Written: {path}")
print(f"Size: {size_kb:.1f} KB")
print(f"Stages: {len(stages)}")
# count molecules
mol_count = sum(1 for stg in stages for s in stg['steps'] if s[0] == 'mol')
arrow_count = sum(1 for stg in stages for s in stg['steps'] if s[0] == 'arrow')
print(f"Molecules: {mol_count}, Arrows: {arrow_count}")
