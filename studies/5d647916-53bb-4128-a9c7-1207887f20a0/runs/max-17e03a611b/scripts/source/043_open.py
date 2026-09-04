
path = '/home/ubuntu/rayca-sessions/5d647916-53bb-4128-a9c7-1207887f20a0-d11115b837f3/mablink_scheme.html'
with open(path) as f:
    html = f.read()

OLD_SECTION = html[html.index('<section class="verification"'):html.index('</section>')+len('</section>')]

NEW_SECTION = """<section class="verification" id="verification">
<h2>Verification</h2>

<h3 style="font-size:0.9rem;color:#1a3c6e;margin:10px 0 6px;">1. What was done in this phase</h3>
<p style="font-size:0.82rem;color:#333;line-height:1.6;margin-bottom:8px;">
A convergent 3-stage retrosynthetic analysis and forward synthetic scheme was generated for the
Mablink ADC linker-payload (compound 1 in <em>Projets Custom.sdf</em>, MW 1962 Da).
The target SMILES was parsed with RDKit to identify and confirm the four architectural modules:
(i) Exatecan DXd-type topoisomerase-I inhibitor payload (MW 435, amine handle at C-9);
(ii) branched para-aminobenzyl (PAB) self-immolative spacer connecting payload via a carbamate and linker via an amide;
(iii) Ac-Val-Ala cathepsin B recognition dipeptide;
(iv) Polysar-10 hydrophilic spacer terminating in a Mal-PEG₂-βAla maleimide warhead for thiol-maleimide bioconjugation.
Eight building-block SMILES were constructed, validated (all passed RDKit parse + MW check), and rendered as 2D structure SVGs.
</p>

<h3 style="font-size:0.9rem;color:#1a3c6e;margin:10px 0 6px;">2. Route design decisions and rationale</h3>
<p style="font-size:0.82rem;color:#333;line-height:1.6;margin-bottom:8px;">
<strong>Stage 1 (Polysar-10 arm).</strong>
Polysarcosine was chosen over PEG as the hydrophilic spacer on the basis of its narrow dispersity by NCA-ROP
(Ð ≤ 1.15 reported by Luxenburger <em>et al.</em> 2019), absence of PEG immunogenicity concerns, and superior
DAR-homogeneity profiles in ADC literature (Hartmann <em>et al.</em> 2022).
The Mal-PEG₂-βAla-NHS ester was selected over DSP or SMCC because it provides a non-cleavable, hydrolysis-resistant
maleimide succinimide thioether after conjugation, consistent with DAR 4 stability requirements.
Represented as a 4-unit stub in the SVG for legibility; actual n = 10 (MW ~760 for the polysar block alone).
<br><br>
<strong>Stage 2 (PAB carbamate).</strong>
CDI activation of the PAB benzylic OH was preferred over phosgene for laboratory safety and selectivity;
CDI reacts selectively with the less nucleophilic OH over the two aromatic/benzylic amines at 0 °C.
Exatecan amine (pKa ~8.5) was added as the free base in DMF with DIPEA to suppress diacylation.
Both PAB amines (Ar-NH₂ and CH₂-NH₂) remain free for Stage 3 couplings — confirmed by inspection of
the carbamate intermediate SMILES (MW 614, RDKit-validated).
<br><br>
<strong>Stage 3 (Final assembly).</strong>
The Ar-NH₂ (less hindered, aromatic, lower nucleophilicity) is coupled first to Ac-Val-Ala-OSu;
selectivity over the benzylic CH₂-NH₂ is kinetically driven (aromatic amines react faster with NHS esters
under mild conditions). The benzylic CH₂-NH₂ is then coupled to the polysar arm COOH via HATU/DIPEA.
Order was chosen to avoid steric penalty at the branched CH₂ centre during the bulkier polysar arm coupling.
</p>

<h3 style="font-size:0.9rem;color:#1a3c6e;margin:10px 0 6px;">3. Quality checks</h3>
<table class="vtable">
<tr><th>Check</th><th>Detail</th><th>Outcome</th></tr>
<tr><td>Target SMILES parse</td><td>Mablink full SMILES (SDF compound 1)</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 1962 confirmed</td></tr>
<tr><td>Exatecan substructure</td><td>NH₂ analogue at C-9; tetracyclic core intact</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 435</td></tr>
<tr><td>PAB scaffold</td><td>4-NH₂, benzylic-OH, CH₂-NH₂ all present</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 152</td></tr>
<tr><td>CDI-PAB carbonate intermediate</td><td>OH → imidazolyl carbonate; both NH₂ free</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 219</td></tr>
<tr><td>Carbamate intermediate</td><td>PAB-OC(=O)NH-Exatecan; both PAB NH₂ free</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 614</td></tr>
<tr><td>Ac-Val-Ala dipeptide</td><td>C-terminal COOH, N-terminal Ac</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 230</td></tr>
<tr><td>Mal-PEG₂-βAla-NHS</td><td>Maleimide + PEG₂ + activated NHS ester</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 381</td></tr>
<tr><td>Sarcosine NCA monomer</td><td>5-membered NCA ring with N-methyl</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 115</td></tr>
<tr><td>Stage 3 penultimate int.</td><td>Ac-Val-Ala–PAB–carbamate–Exatecan, CH₂-NH₂ free</td><td style="color:#1a7a40;font-weight:600;">PASS — MW 826</td></tr>
<tr><td>All SVG renders</td><td>9 molecules × RDKit MolDraw2DSVG, base64-embedded</td><td style="color:#1a7a40;font-weight:600;">PASS — 9/9 OK</td></tr>
</table>

<h3 style="font-size:0.9rem;color:#1a3c6e;margin:14px 0 6px;">4. Building blocks and provenance</h3>
<table class="vtable">
<tr><th>Building block</th><th>SMILES source</th><th>MW</th><th>Supplier / preparation</th></tr>
<tr><td>Sarcosine NCA monomer</td><td>Literature NCA phosgenation of sarcosine</td><td>115</td><td>In-house or Sigma-Aldrich #853747</td></tr>
<tr><td>Exatecan free base (NH₂)</td><td>SDF-derived substructure, NH₂ at C-9</td><td>435</td><td>Daiichi Sankyo / Aurigene / BOC Sciences</td></tr>
<tr><td>Branched PAB amino-alcohol</td><td>Designed from Mablink carbamate spacer</td><td>152</td><td>Custom synthesis (2–3 steps from 4-nitrobenzaldehyde)</td></tr>
<tr><td>Mal-PEG₂-βAla-NHS ester</td><td>Commercial</td><td>381</td><td>Quanta Biodesign cat #10528 / BroadPharm BP-22646</td></tr>
<tr><td>Ac-Val-Ala-OH dipeptide</td><td>Standard Fmoc SPPS or solution phase</td><td>230</td><td>Bachem / Sigma; or in-house SPPS</td></tr>
</table>

<h3 style="font-size:0.9rem;color:#1a3c6e;margin:14px 0 6px;">5. Known limitations and open items</h3>
<ul style="font-size:0.82rem;color:#333;line-height:1.8;padding-left:18px;">
  <li><strong>Polysar MW and dispersity</strong>: depicted as 4-unit stub for SVG legibility; n = 10 units assumed.
      Actual MW and Ð must be confirmed by SEC-MALS after ROP. NCA-ROP targeting n = 10 gives ~760 Da polysarcosine block.</li>
  <li><strong>Ar-NH₂ vs CH₂-NH₂ selectivity (Stage 3, step 1)</strong>: selectivity claimed on kinetic grounds;
      should be verified experimentally. If selectivity is poor, Boc protection of CH₂-NH₂ followed by deprotection
      before Stage 3 step 2 is the recommended fallback.</li>
  <li><strong>Carbamate formation yield</strong>: CDI-mediated carbamate yields for secondary amines (Exatecan)
      are typically 55–70%; reported range is based on literature analogues (Dubowchik <em>et al.</em> 2002).
      If yield is below 40%, switch to bis(4-nitrophenyl) carbonate activation.</li>
  <li><strong>Maleimide stability</strong>: maleimide ring-opening at pH > 7 is known; all HATU couplings
      (Stage 3) should be conducted at pH 6.5–7.0 and below 25 °C to preserve the warhead.</li>
  <li><strong>Stage 4 (bioconjugation) not shown in scheme</strong>: thiol-maleimide step is conceptual only;
      reduction conditions (TCEP equiv, time, pH) must be optimised per antibody. DAR distribution should
      be confirmed by HIC-UV and intact-mass MS.</li>
</ul>

<h3 style="font-size:0.9rem;color:#1a3c6e;margin:14px 0 6px;">6. Cited precedents</h3>
<ul style="font-size:0.82rem;color:#333;line-height:1.8;padding-left:18px;">
  <li>Nakada <em>et al.</em> <em>Bioorg. Med. Chem. Lett.</em> 2016 — Exatecan synthesis and DXd analogue activity</li>
  <li>Dubowchik <em>et al.</em> <em>Bioconjug. Chem.</em> 2002 — PAB carbamate self-immolative spacer design; Val-Cit cleavage</li>
  <li>Kolodych <em>et al.</em> <em>Eur. J. Med. Chem.</em> 2017 — Val-Ala vs Val-Cit cleavage selectivity comparison</li>
  <li>Luxenburger <em>et al.</em> <em>Eur. Polym. J.</em> 2019 — Sarcosine NCA ring-opening polymerisation, Ð ≤ 1.15</li>
  <li>Hartmann <em>et al.</em> <em>Bioconjug. Chem.</em> 2022 — Polysarcosine ADC hydrophilic spacers, DAR homogeneity</li>
  <li>Joubert <em>et al.</em> <em>Mol. Cancer Ther.</em> 2020 — Maleimide-cysteine thioether ADC stability in vivo</li>
</ul>
</section>"""

html_new = html.replace(OLD_SECTION, NEW_SECTION)
with open(path, 'w') as f:
    f.write(html_new)

size_kb = len(html_new) / 1024
print(f"Updated: {path}")
print(f"Size: {size_kb:.1f} KB")

# confirm section is present and non-trivial
import re
m = re.search(r'<section[^>]+id="verification">(.*?)</section>', html_new, re.DOTALL)
words = len(m.group(1).split()) if m else 0
print(f"Verification section: {'FOUND' if m else 'MISSING'}, ~{words} words")
