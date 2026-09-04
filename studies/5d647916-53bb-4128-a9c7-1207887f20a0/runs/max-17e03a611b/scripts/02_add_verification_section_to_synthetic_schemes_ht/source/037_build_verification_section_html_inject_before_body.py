
# Build the verification section HTML and inject it before </body>

VERIFY_CSS = """
.verify-section {
  background:#fff; border:1px solid #ddd; border-radius:8px;
  margin-bottom:28px; overflow:hidden;
}
.verify-header {
  background:#fff8e8; border-bottom:1px solid #e8d88c;
  padding:12px 20px;
}
.verify-header h2 { font-size:15px; font-weight:700; color:#7a5800; }
.verify-body { padding:16px 20px; }
.verify-body h3 { font-size:12.5px; font-weight:700; color:#333; margin:14px 0 6px; border-bottom:1px solid #eee; padding-bottom:3px; }
.verify-body h3:first-child { margin-top:0; }
.verify-table { border-collapse:collapse; width:100%; font-size:11.5px; margin-bottom:8px; }
.verify-table th { background:#f0f4ff; color:#12307a; font-weight:700; text-align:left; padding:5px 10px; border:1px solid #d0d8f0; }
.verify-table td { padding:4px 10px; border:1px solid #e0e0e0; vertical-align:top; }
.verify-table tr:nth-child(even) td { background:#fafafa; }
.smiles-cell { font-family:monospace; font-size:10.5px; word-break:break-all; color:#333; }
.audit-crit { color:#c00; font-weight:700; }
.audit-ok   { color:#2a8a4a; font-weight:700; }
.verify-note { font-size:11.5px; color:#555; line-height:1.6; margin-bottom:6px; }
code { font-family:monospace; font-size:11px; background:#f0f0f0; padding:1px 4px; border-radius:2px; }
"""

# Route summary for verification table
ROUTE_SUMMARY = [
  ('MCUF651', 'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1',
   'Route 1', 'Amide coupling + N-alkylation', 2, 'AiZ-validated', 'is_solved=True, score=0.994'),
  ('A317',    'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1',
   'Route 1', 'Hantzsch thiazole (Cu N-aryl → NBS → thiourea) + amide', 4, 'AiZ-validated (CRITICAL-3 corrected)', 'is_solved=True, score=0.987'),
  ('A317',    'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1',
   'Route 2', 'Suzuki at C4-thiazole + amide', 2, 'Independent', '—'),
  ('8008',    'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#Cc3cncc(C(=O)OC)c3)nc2c1O',
   'Route 1', 'Sulfonylation + O-alkyl + 2× Sonogashira', 6, 'Recommended', 'is_solved=False (score=0.817); missing leaf: sulfonyl chloride'),
  ('7977',    'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21',
   'Route 1', 'CDI ring-close + N-alkyl (chloroacetamide) + Suzuki', 4, 'AiZ-validated', 'is_solved=True, score=0.963'),
  ('7877',    'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1',
   'Route 2', 'O-propargylation + Lautens 5-exo-dig (Pd/Cu) + Suzuki + saponification', 4, 'CRITICAL-1 corrected; furo[2,3-b]pyr', 'is_solved=False (score=0.773); ring corrected to furan'),
  ('7877',    'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1',
   'Route 3', 'Suzuki + cyclodehydration (Majumdar) + saponification', 3, 'CRITICAL-1 corrected; independent', '—'),
  ('B54',     'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1',
   'Route 1', 'MnO₂ + aldol + NBS + Hantzsch + amide', 5, 'AiZ-validated (CRITICAL-2 corrected)', 'is_solved=True, score=0.963; first successful dispatch'),
  ('B54',     'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1',
   'Route 3', 'HWE olefination on 4-formylthiazole + amide', 2, 'Independent', '—'),
]

import html as H

rows = ''.join(
    f'<tr>'
    f'<td><strong>{H.escape(cpd)}</strong></td>'
    f'<td class="smiles-cell">{H.escape(smi)}</td>'
    f'<td>{H.escape(rt)}</td>'
    f'<td>{H.escape(desc)}</td>'
    f'<td style="text-align:center">{n}</td>'
    f'<td>{H.escape(status)}</td>'
    f'<td style="font-size:10px;color:#666">{H.escape(aiz)}</td>'
    f'</tr>'
    for cpd, smi, rt, desc, n, status, aiz in ROUTE_SUMMARY
)

AUDIT_ROWS = [
  ('CRITICAL-1', '7877 ring misidentified as oxazolo[4,5-c]pyridine; Routes 2&3 targeted N–C oxazole synthesis',
   'RDKit atom analysis: 5-membered ring = (O,C,C,C,C), zero N → furan. Ring = furo[2,3-b]pyridine. Routes 2&3 replaced with Lautens 5-exo-dig and Majumdar cyclodehydration.'),
  ('CRITICAL-2', 'B54 AiZ failure called "timeout" (two independent attempts)',
   'JSON record shows rc=null, error="input_file_not_staged", duration_s=0.0, image=null. Container never started; /C=C/ slashes in SMILES were parsed as a file path. Fixed: canonical SMILES dispatched. B54 now solved (rc=0, 78.9 s, is_solved=True, score=0.963).'),
  ('CRITICAL-3', 'A317 AiZ Route 1 flagged as Hantzsch regiochemical error; "correction" proposed',
   'Hantzsch rule: carbonyl C (bearing substituent) → C4 of thiazole; alpha-C (bearing Br) → C5. The AiZ haloketone O=C(CBr)[C@@H]1CCCN1c1ccccn1 has pyrrolidinyl on the carbonyl C → correctly maps to C4. Phase-1 "correction" placed pyrrolidinyl on alpha-C → C5 (wrong regioisomer). AiZ Route 1 restored.'),
  ('MAJOR',      'No persistent document written for phase 1 (inline chat text only)',
   'Resolved: retrosynthesis_phase1_corrected.md written with full analysis, all 7 compounds, scoring tables, and audit corrections.'),
]

audit_rows = ''.join(
    f'<tr>'
    f'<td class="{"audit-crit" if s.startswith("CRIT") else "audit-ok"}">{H.escape(s)}</td>'
    f'<td>{H.escape(orig)}</td>'
    f'<td>{H.escape(fix)}</td>'
    f'</tr>'
    for s, orig, fix in AUDIT_ROWS
)

VERIFY_BLOCK = f"""
<section class="verify-section" id="verification">
<div class="verify-header">
  <h2>Phase Verification Record</h2>
</div>
<div class="verify-body">

<h3>Provenance</h3>
<p class="verify-note">
  <strong>Input file:</strong> <code>Projets Custom.sdf</code> — researcher-supplied SDF (V3000 format, 7 compounds, 20209 bytes).
  No public reference compound was substituted. SMILES extracted via RDKit <code>SDMolSupplier</code>.<br>
  <strong>AiZynthFinder:</strong> <code>registry.rayca.org/rayca-tools/aizynthfinder:latest</code>,
  dispatch via <code>run_aidd_tool</code>, <code>gpu=True</code>, <code>expansion_policy=uspto</code>,
  <code>filter_policy=uspto</code>, <code>iteration_limit=150</code>, <code>time_limit=150</code>,
  <code>max_routes=5</code>. Results saved to
  <code>aizynthfinder-results.json</code> through <code>aizynthfinder-results-6.json</code>.<br>
  <strong>Structure rendering:</strong> RDKit (run_python environment, 2D coords via <code>AllChem.Compute2DCoords</code>,
  SVG via <code>MolDraw2DSVG</code>). All 32 SMILES validated before rendering; 1 SMILES corrected
  (<code>O=Cc1ncs(c1)N</code> → <code>Nc1nc(C=O)cs1</code>).<br>
  <strong>Corrected analysis document:</strong> <code>retrosynthesis_phase1_corrected.md</code> —
  full route descriptions, reagents, conditions, yield bases, scoring tables, recommendations.
</p>

<h3>Routes and steps — complete inventory</h3>
<table class="verify-table">
<tr>
  <th>Compound</th><th>Target SMILES</th><th>Route</th><th>Strategy</th>
  <th>Steps</th><th>Status</th><th>AiZ result</th>
</tr>
{rows}
</table>
<p class="verify-note" style="font-size:10.5px;color:#777;margin-top:4px">
  "Steps" = number of reaction arrows shown. Mablink (MW 1962, ADC linker-payload) is out of AiZynthFinder scope and not shown here;
  see <em>retrosynthesis_phase1_corrected.md §Compound 7</em> for programme-level analysis.
</p>

<h3>How to cross-check this document</h3>
<p class="verify-note">
  1. Every SMILES shown in a molecule box can be independently validated with any SMILES parser (RDKit, ChemDraw, MarvinSketch).<br>
  2. AiZ JSON files (<code>aizynthfinder-results-1</code> through <code>-6.json</code>) contain the raw <code>reaction_tree</code> nodes; leaf SMILES are in the <code>in_stock</code> records and can be searched directly on Sigma-Aldrich, Combi-Blocks, Enamine, and Fluorochem.<br>
  3. All reagent choices and yield estimates are cited in <code>retrosynthesis_phase1_corrected.md</code> with literature class references (Valeur &amp; Bradley 2009; Mérour et al. 2014; Lautens JACS 2006; Majumdar Tetrahedron 2010; Isloor Eur. J. Med. Chem. 2009; Clayden OC).<br>
  4. Stereochemical assignments (A317 pyrrolidine (R), MCUF651 nipecotyl (R)) derive from the chiral-pool starting materials; ring-system assignments (furo[2,3-b]pyridine for 7877; imidazo[4,5-c]pyridinone for 7977; pyridin-2-yl for A317) were independently verified by RDKit atom-distance analysis (see <code>phase1_audit.md</code>).
</p>

<h3>Audit corrections applied (from independent subagent audit, 2026-09-02)</h3>
<table class="verify-table">
<tr><th>Severity</th><th>Original error</th><th>Correction applied</th></tr>
{audit_rows}
</table>

</div>
</section>
"""

# Inject into HTML: insert verify block and extra CSS before </body> and </style>
path = '/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/synthetic_schemes.html'
with open(path) as f:
    html_src = f.read()

# inject CSS into <style> block
html_src = html_src.replace('</style>', VERIFY_CSS + '\n</style>', 1)

# inject verify block right after <nav>...</nav> block (before first compound section)
nav_end = html_src.find('<section class="compound-section"')
html_src = html_src[:nav_end] + VERIFY_BLOCK + html_src[nav_end:]

with open(path, 'w') as f:
    f.write(html_src)

print(f"Injected verification section. New size: {len(html_src)/1024:.1f} KB")

# Quick sanity check
assert 'Phase Verification Record' in html_src
assert 'CRITICAL-1' in html_src
assert 'CRITICAL-2' in html_src
assert 'CRITICAL-3' in html_src
assert 'Provenance' in html_src
assert 'How to cross-check' in html_src
print("All assertions pass.")
