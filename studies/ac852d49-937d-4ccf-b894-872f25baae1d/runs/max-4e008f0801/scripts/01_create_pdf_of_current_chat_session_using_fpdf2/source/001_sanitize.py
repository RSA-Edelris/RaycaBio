
from fpdf import FPDF, XPos, YPos
import textwrap, os

def sanitize(text):
    rep = {
        '–': '-', '—': '--', '‘': "'", '’': "'",
        '“': '"', '”': '"', '•': '*', '…': '...',
        '±': '+/-', '×': 'x', '°': ' deg', '→': '->',
        '≥': '>=', '≤': '<=', '²': '2', '³': '3',
        'μ': 'u', '−': '-', '≈': '~=', ' ': ' ',
        'σ': 'sigma', 'Δ': 'Delta', 'µ': 'u',
        '─': '-', '│': '|', '✓': '[OK]', '✗': '[X]',
        'é': 'e', 'β': 'beta', 'α': 'alpha', '·': '.',
        '‑': '-', '‐': '-', '®': '(R)', '←': '<-',
        'γ': 'gamma', 'ε': 'eps', '¹': '1',
    }
    for ch, r in rep.items():
        text = text.replace(ch, r)
    return text.encode('ascii', 'replace').decode('ascii')

messages = [
("user", """Optimise a concrete transformation by default: the Suzuki Miyaura coupling of 4-bromoanisole (SMILES COc1ccc(Br)cc1) with phenylboronic acid (SMILES OB(O)c1ccccc1) to give 4-methoxybiphenyl, with isolated yield as the response. Design a high throughput experimentation campaign to optimise the reaction described in this session, and if I name a different transformation, use mine instead and say so.

Begin by separating what we are optimising from what we are learning: state the response to be maximised, how it is measured, and the precision of that measurement, because a design finer than the assay is wasted plate space. Choose the factors and justify each: catalyst or ligand set, base, solvent, concentration, temperature, stoichiometry and time, saying which are continuous and which categorical, and which you are deliberately holding constant and why.

Then give the actual design, as a plate map I can hand to a technician: the design type with the reason it suits this factor set, the number of experiments, the levels, the randomisation, the replicates and where the centre points and controls sit. State in advance the model you will fit and the effects you can and cannot estimate, so the analysis is fixed before the data exists. Say how many rounds you expect, what decision ends each round, and whether a Bayesian sequential approach would reach the optimum in fewer experiments than a single factorial for this problem."""),

("claude", """## Suzuki-Miyaura Optimization Campaign: Structured Design

### 1. Response, Measurement, and Precision

Response: Isolated yield of 4-methoxybiphenyl (%)

Measurement at HTE scale (0.05 mmol): Use UPLC with a pre-weighed internal standard (1,3,5-trimethoxybenzene, 0.5 equiv added after reaction before workup), area ratios calibrated against a standard curve. This gives molar yield directly.

Assay precision: UPLC area % reproducibility +/-1-2% RSD; calibration introduces +/-1-2% systematic term. Working precision: +/-3% absolute.

Consequence for design: The smallest detectable effect at 95% confidence is ~6% (2 sigma). Any factor whose plausible effect is smaller is not worth a level until larger drivers are resolved. This caps defensible levels per continuous factor at 3 for Round 2.

### 2. Factor Selection

CATEGORICAL FACTORS (vary in Round 1 by array):

Pd/ligand system (4 levels): Largest single driver -- controls oxidative addition rate and transmetalation geometry. 4-Bromoanisole is mildly deactivated (EDG methoxy slows OA vs. aryl iodides). Coverage from soft phosphine (PPh3) to bulky monodentate (SPhos/RuPhos) to bidentate (dppf).

Base (4 levels): Controls transmetalation equilibrium, boronate activation, and competing protodeboronation. pKa and aqueous solubility vary across carbonate, phosphate, fluoride and amine; one cannot be predicted from another.

Solvent (3 levels): Sets boiling point ceiling, water content (critical for boronate activation), Pd solubility and partition. DMF/H2O, dioxane/H2O, EtOH/H2O span the relevant polarity-proticity space.

Why 4x4x3: 48 combinations with duplicates fills one 96-well plate exactly.

CONTINUOUS FACTORS (optimize in Round 2 by RSM):
  Temperature: 60-100 degC
  PhB(OH)2 stoichiometry: 1.0-2.5 equiv
  Concentration: 0.10-0.50 M

HELD CONSTANT:
  Pd loading: 5 mol% -- adding it as a 4th continuous variable halves RSM resolution.
  Reaction time: 16 h -- long enough under favorable conditions; no known degradation of 4-methoxybiphenyl.
  Substrate, boronic acid, scale (0.05 mmol), atmosphere (N2).

### 3. Round 1 -- Categorical HTE Array (96-well plate)

Design type: Full 3-factor categorical factorial with internal duplication.

Reason: The 4x4x3 = 48 combination space is small enough to enumerate completely on one plate. A fractional design would confound catalyst x base interactions, which are chemically real.

With 48 conditions x 2 replicates = 96 wells, all main effects, 2-factor and 3-factor interactions are estimable, plus pure error from duplicate pairs (df = 48).

FACTOR LEVELS:

Pd/Ligand systems:
  Cat-A: Pd(PPh3)4 (5 mol%)
  Cat-B: Pd(dppf)Cl2 (5 mol%)
  Cat-C: Pd(OAc)2 (5 mol%) + SPhos (6 mol%)
  Cat-D: Pd(OAc)2 (5 mol%) + RuPhos (6 mol%)

Bases (2.0 equiv):
  Bs-1: K2CO3 (2 M aq)     Bs-2: K3PO4 (2 M aq)
  Bs-3: Cs2CO3 (solid)     Bs-4: CsF (solid, no added water)

Solvents (0.2 mL total, 0.25 M):
  Sv-X: DMF/H2O 9:1    Sv-Y: 1,4-Dioxane/H2O 9:1    Sv-Z: EtOH/H2O 3:1

Fixed in Round 1: 80 degC, 0.25 M, 1.5 equiv PhB(OH)2, 16 h.

PLATE MAP (logical layout, randomise before dispensing):

         [Sv-X: Bs1 Bs2 Bs3 Bs4] [Sv-Y: Bs1 Bs2 Bs3 Bs4] [Sv-Z: Bs1 Bs2 Bs3 Bs4]
          C01  C02  C03  C04      C05  C06  C07  C08       C09  C10  C11  C12
Row A |  Cat-A  x4            |  Cat-A  x4            |  Cat-A  x4            | (rep-1)
Row B |  Cat-B  x4            |  Cat-B  x4            |  Cat-B  x4            | (rep-1)
Row C |  Cat-C  x4            |  Cat-C  x4            |  Cat-C  x4            | (rep-1)
Row D |  Cat-D  x4            |  Cat-D  x4            |  Cat-D  x4            | (rep-1)
Row E |  Cat-C  x4            |  Cat-C  x4            |  Cat-C  x4            | (rep-2, shuffled)
Row F |  Cat-A  x4            |  Cat-A  x4            |  Cat-A  x4            | (rep-2, shuffled)
Row G |  Cat-D  x4            |  Cat-D  x4            |  Cat-D  x4            | (rep-2, shuffled)
Row H |  Cat-B  x4            |  Cat-B  x4            |  Cat-B  x4            | (rep-2, shuffled)

Row-shuffle (E=Cat-C, F=Cat-A, G=Cat-D, H=Cat-B) prevents systematic liquid-handling artefacts from confounding the catalyst factor.

CONTROLS (replace 8 well-pairs, 16 wells, spread across all solvent columns):
  * No Pd (base+solvent only): 6 wells (3 solvents x 2 rep) -- background check.
  * No base (Pd-A+solvent): 3 wells (1 per solvent, rep-1) -- base requirement check.
  * Positive benchmark (Cat-B/Bs-1/Sv-X): 7 wells replicated -- assay anchor.
This reduces unique tested combinations to 40.

### 4. Pre-Specified Model (Round 1)

Y_ijk = mu + alpha_i + beta_j + gamma_k + (ab)_ij + (ag)_ik + (bg)_jk + (abg)_ijk + eps

i = catalyst (4 levels), j = base (4 levels), k = solvent (3 levels), l = replicate (2).

Estimable: all main effects, all 2-factor interactions, all 3-factor interactions, pure error.
Not estimable: time variation (fixed), Pd loading effects (fixed), continuous variable optima.

Decision threshold: Flag any condition >=60% yield as a lead. If none clears 40%, examine main effects before expanding catalyst set.

### 5. Round 2 -- RSM on Continuous Variables (FCC-CCD, 20 runs)

Design: Face-centred CCD (alpha = 1, axial points on cube faces).
Reason: Stays within factor range; no conditions outside declared bounds.

Factor coded levels (-1, 0, +1):
  Temperature (degC): 60, 80, 100
  PhB(OH)2 equiv:    1.0, 1.75, 2.5
  Concentration (M): 0.10, 0.30, 0.50

Run count: 2^3 factorial (8) + 6 axial + 6 centre replicates = 20 total.

Model: Y = b0 + b1*T + b2*S + b3*C + b11*T^2 + b22*S^2 + b33*C^2 + b12*T*S + b13*T*C + b23*S*C

Estimable: all main effects, all quadratic effects, all 2-factor interactions (10 terms + intercept).
Not estimable: 3-factor interaction T*S*C (aliased with lack-of-fit in FCC-CCD).

### 6. Round Structure and Decision Rules

Round 1 (96 wells, 1 plate, ~1 week): Full categorical array.
  Decision: Identify best Cat/Base/Solvent; >=1 lead above 60% required to advance.

Round 2 (40 wells, half plate, ~1 week): FCC-CCD on T, S, C.
  Decision: RSM predicts optimum within design space; confirm with 3 replicates.

Round 3 optional (6-12 wells): Confirmation + scale-up to 0.5 mmol.
  Decision: Confirm within 5% of prediction. Campaign complete.

Total: 136-148 wells, 2-3 rounds, 3-4 weeks elapsed.

### 7. Bayesian Sequential vs. HTE Array

For this problem, the HTE array reaches the categorical optimum in the same or fewer experiments than BO. The categorical space (48 combinations) is small enough to enumerate on one plate.

A GP BO would need ~10-15 seed experiments then 3-5 rounds x 8 = 34-55 experiments across 4-6 sequential weeks, vs. 48 experiments in 1 week with the array.

BO wins only if: (a) categorical variables are encoded with chemical descriptors (DFT buried volume, Hammett sigma, pKa, polarity), enabling ~20-25 experiment convergence; (b) the campaign spans multiple substrates (surrogate transfers); (c) the categorical space is large (>100 combinations); or (d) the total budget is <25 experiments.

For Round 2 (continuous variables), BO and FCC-CCD have essentially equivalent efficiency at 3 factors. Use CCD if you want a full model; use BO if you want only the optimum.

Summary: Run the HTE array for Round 1. Switch to BO if this is the first substrate in a series."""),

("user", "push everything to RSA-Edelris/RaycaBio github"),

("claude", """Pushing the session to GitHub now.

[Task created, GitHub push executed]

Pushed successfully. 4 files committed to RSA-Edelris/RaycaBio on main.

Commit: ff8e5b2e
URL: studies/ac852d49.../runs/max-01c5ef17a8/

Files include the run record, a generated README describing the campaign, and the updated study index (STUDIES.md)."""),

("claude", """Audit complete. Report saved to audit_hte_suzuki_campaign.md.

CRITICAL -- fix before giving the plate map to a technician:

The second replicate block is misassigned. Row E is labelled Cat-C, not Cat-A -- the row-shuffle is intentional (to break systematic dispensing order) but the grid key does not make this clear. A technician following the grid as written would load the wrong catalyst into the E rows and silently corrupt all catalyst-level yield comparisons. The grid needs an explicit column noting the intended catalyst for each row, with the shuffle motivation stated in the map itself, not only in the prose above it.

MAJOR -- correct before the design is used:

1. Plate map key notation ("A-X / B-X") collides with row letters (A-H) and catalyst letters (Cat-A through Cat-D) -- uninterpretable without a disambiguation rule a technician must infer.

2. Cs2CO3 + bulky phosphine "synergy" is not documented for this substrate class; it conflates two independently valid choices. May mislead analysis of base x catalyst interactions.

3. CsF described as poorly compatible with Pd(OAc)2 -- CsF is routinely used WITH Pd(OAc)2 in Suzuki couplings. A productive combination would be incorrectly flagged as a problem in the data.

4. "No known degradation" of product used to eliminate time as a variable -- this addresses product stability, not whether slow catalyst/base combinations have reached plateau by 16 h. Slow-but-capable conditions will be systematically underscored.

5. Bayesian lower bound of 34 experiments does not follow from the stated parameters: 10-15 seed + 4-5 rounds x 8 = 42-55. The lower bound of 34 is internally inconsistent.

VERIFIED CORRECT:
  * 4 x 4 x 3 = 48 unique conditions
  * 48 x 2 = 96 wells (fills one plate exactly)
  * 16-well / 8-pair / 40-combination consistency
  * CCD 20-run count (8 factorial + 6 axial + 6 centre replicates)
  * 4-bromoanisole correctly described as electron-rich (EDG methoxy slows OA)
  * 1,3,5-trimethoxybenzene as UPLC internal standard: no co-elution with 4-methoxybiphenyl expected on C18 reversed-phase"""),

("user", "With method used in session Photocatalytic decarboxylative arylation HTE design, create a pdf of the chat in the current session and download it. Do not run any audit."),

("claude", """The session "Photocatalytic decarboxylative arylation HTE design" was attached but could not be resolved -- the platform marked it as an unrecognised attachment kind, so I have no access to its contents and cannot use its method here.

I won't invent what that session contained or substitute a default approach in its place, since you specifically asked to use that method.

To unblock this: could you either share the relevant steps from that session directly in the chat, or point me to a file or artifact it produced (e.g. a script path or report file in the workspace)? Once I can see the method, I'll apply it to generate the PDF of this session."""),

("user", "create a pdf of the chat in the current session with fpdf2. When necessary, sanitize the text by replacing common unicode chars with ASCII equivalents before rendering. Download only the created PDF file. Blue bubbles = your messages, grey bubbles = Claude responses"),

("claude", "Checked fpdf2 availability (v2.8.8 present), created task, and now generating the PDF of this session with blue bubbles for user messages and grey bubbles for Claude responses."),
]

# ---- PDF ----

class ChatPDF(FPDF):
    PAGE_W = 210
    MARGIN = 12
    BUBBLE_MAX_W = 155
    LINE_H = 5
    PAD = 4

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, 'Session: Suzuki-Miyaura HTE Campaign Design', align='C',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(180, 180, 180)
        self.line(self.MARGIN, self.get_y(), self.PAGE_W - self.MARGIN, self.get_y())
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, f'Page {self.page_no()}', align='C')

    def add_bubble(self, text, role):
        text = sanitize(text)
        is_user = (role == 'user')
        if is_user:
            fr, fg, fb = 25, 90, 185       # blue
            tr, tg, tb = 255, 255, 255
            label = 'You'
        else:
            fr, fg, fb = 70, 70, 75        # dark grey
            tr, tg, tb = 255, 255, 255
            label = 'Claude'

        self.set_font('Helvetica', '', 8)
        chars_per_line = 95
        lines = []
        for para in text.split('\n'):
            if not para.strip():
                lines.append('')
            else:
                wrapped = textwrap.wrap(para, width=chars_per_line)
                lines.extend(wrapped if wrapped else [''])

        bubble_h = len(lines) * self.LINE_H + 2 * self.PAD + 6

        if self.get_y() + bubble_h > 280:
            self.add_page()

        usable = self.PAGE_W - 2 * self.MARGIN
        bw = min(self.BUBBLE_MAX_W, usable)
        x0 = self.MARGIN if not is_user else self.PAGE_W - self.MARGIN - bw
        y0 = self.get_y()

        self.set_fill_color(fr, fg, fb)
        self.set_draw_color(fr, fg, fb)
        self.rect(x0, y0, bw, bubble_h, style='F')

        self.set_xy(x0 + self.PAD, y0 + self.PAD - 1)
        self.set_font('Helvetica', 'B', 7)
        self.set_text_color(190, 210, 250 if is_user else 190)
        self.cell(bw - 2 * self.PAD, 5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_font('Helvetica', '', 8)
        self.set_text_color(tr, tg, tb)
        for line in lines:
            self.set_x(x0 + self.PAD)
            self.cell(bw - 2 * self.PAD, self.LINE_H,
                      line[:130], new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.set_y(y0 + bubble_h + 3)
        self.set_text_color(0, 0, 0)


pdf = ChatPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(12, 15, 12)
pdf.add_page()

for role, content in messages:
    pdf.add_bubble(content, role)

out = '/tmp/suzuki_hte_chat_session.pdf'
pdf.output(out)
print(f"Written: {out}")
print(f"Size:    {os.path.getsize(out):,} bytes")
print(f"Pages:   {pdf.page}")
