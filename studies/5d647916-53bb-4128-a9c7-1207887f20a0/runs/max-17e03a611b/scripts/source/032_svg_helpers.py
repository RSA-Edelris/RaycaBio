
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
import base64, html as H

# ── SVG helpers ──────────────────────────────────────────────────────────────
def mol_b64(smiles, w=175, h=125):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None: return None
    AllChem.Compute2DCoords(mol)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    d.drawOptions().clearBackground = False
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return base64.b64encode(d.GetDrawingText().encode()).decode()

# ── Route data ───────────────────────────────────────────────────────────────
# Format per step: ('mol', smiles, display_name, role)   role = sm|int|prod
#                  ('arrow', [reagent_lines], conditions_str, yield_str)
#                  ('plus', smiles, display_name)         — extra SM shown above arrow

COMPOUNDS = [
  { 'id': 'MCUF651', 'full_name': 'MCUF651',
    'target_smiles': 'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended',
        'strategic': 'Amide bond N–C(O) then piperidine N-alkylation',
        'steps': [
          ('mol', 'O=C(O)[C@H]1CCCNC1',  '(R)-Nipecotic acid', 'sm'),
          ('arrow', ['HATU (1.1 eq), DIPEA (3 eq)', '+ 4,6-Difluoroindol-2-amine'], 'DMF, 0 °C → RT', '75–85%'),
          ('mol', 'O=C([C@H]1CCCNC1)Nc1cc2cc(F)cc(F)c2[nH]1', 'Amide intermediate', 'int'),
          ('arrow', ['K₂CO₃ (2 eq)', 'CN(C)CCBr (1.1 eq)'], 'MeCN, 60 °C, 8 h', '65–80%'),
          ('mol', 'CN(C)CCN1CC[C@@H](NC(=O)c2cc3cc(F)cc(F)c3[nH]2)CC1', 'MCUF651', 'prod'),
        ]
      },
    ]
  },
  { 'id': 'A317', 'full_name': 'A317',
    'target_smiles': 'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended · Hantzsch',
        'strategic': 'Hantzsch thiazole C4–C disconnection; amide N–C(O)',
        'steps': [
          ('mol', 'CC(=O)[C@@H]1CCCN1', '(S)-2-Acetylpyrrolidine', 'sm'),
          ('arrow', ['CuI (10 mol%), K₃PO₄', '+ 2-Bromopyridine'], 'DMSO, 110 °C, 12 h', '60–75%'),
          ('mol', 'CC(=O)[C@@H]1CCCN1c1ccccn1', '1-(Pyridin-2-yl)-L-prolinoyl\nmethyl ketone', 'int'),
          ('arrow', ['NBS (1.1 eq), AcOH'], 'CHCl₃, 0 °C → RT, 2 h', '80–90%'),
          ('mol', 'O=C(CBr)[C@@H]1CCCN1c1ccccn1', 'α-Bromo ketone', 'int'),
          ('arrow', ['Thiourea (1.1 eq)'], 'EtOH, reflux, 2 h', '70–80%'),
          ('mol', 'Nc1nc([C@@H]2CCCN2c2ccccn2)cs1', '4-(Pyrrolidinyl)-2-\naminothiazole', 'int'),
          ('arrow', ['HATU (1.1 eq), DIPEA (3 eq)', '+ 1-(4-Picolyl)pyrrole-2-COOH'], 'DMF, RT, 12 h', '65–75%'),
          ('mol', 'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1', 'A317', 'prod'),
        ]
      },
      { 'label': 'Route 2', 'tag': 'Independent · Suzuki',
        'strategic': 'C4–C(aryl) of thiazole via Suzuki coupling',
        'steps': [
          ('mol', 'Nc1nc(Br)cs1', '4-Bromo-2-aminothiazole', 'sm'),
          ('arrow', ['Pd(dppf)Cl₂ (5 mol%), K₂CO₃', '+ (R)-Pyrrolidinyl boronate'], 'dioxane/H₂O, 90 °C, 12 h', '65–75%'),
          ('mol', 'Nc1nc([C@@H]2CCCN2c2ccccn2)cs1', '4-(Pyrrolidinyl)-2-\naminothiazole', 'int'),
          ('arrow', ['HATU (1.1 eq), DIPEA (3 eq)', '+ 1-(4-Picolyl)pyrrole-2-COOH'], 'DMF, RT, 12 h', '65–75%'),
          ('mol', 'O=C(Nc1nc([C@H]2CCCN2c2ccccn2)cs1)c1cccn1Cc1ccncc1', 'A317', 'prod'),
        ]
      },
    ]
  },
  { 'id': '8008', 'full_name': '8008',
    'target_smiles': 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#Cc3cncc(C(=O)OC)c3)nc2c1O',
    'routes': [
      { 'label': 'Route 1', 'tag': 'Recommended · Sulfonylation + 2× Sonogashira',
        'strategic': 'Sulfonamide N–S, then O-alkylation, then two Sonogashira couplings',
        'steps': [
          ('mol', 'O=S(=O)(Cl)c1cnc2cccnc2c1O', 'Naphthyridinol\nsulfonyl chloride', 'sm'),
          ('arrow', ['4-Chloroaniline (1.0 eq), Et₃N'], 'CH₂Cl₂, 0 °C → RT', '75–85%'),
          ('mol', 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2cccnc2c1O', 'Sulfonamide (OH free)', 'int'),
          ('arrow', ['EtI (1.5 eq), K₂CO₃'], 'DMF, 60 °C, 6 h', '85–92%'),
          ('mol', 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC)nc2c1O', 'O-Ethyl sulfonamide', 'int'),
          ('arrow', ['Pd/Cu, TMS-acetylene', 'Pd(PPh₃)₄, CuI, Et₃N'], '50 °C, 8 h  →  K₂CO₃/MeOH', '75–85%'),
          ('mol', 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#C)nc2c1O', 'Terminal alkyne', 'int'),
          ('arrow', ['Pd(PPh₃)₄ (5 mol%), CuI', '+ Methyl 5-bromonicotinate'], 'Et₃N, DMF, 50 °C, 12 h', '75–85%'),
          ('mol', 'O=S(=O)(Nc1ccc(Cl)cc1)c1cnc2ccc(OCC#Cc3cncc(C(=O)OC)c3)nc2c1O', '8008', 'prod'),
        ]
      },
    ]
  },
  { 'id': '7977', 'full_name': '7977',
    'target_smiles': 'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended · CDI cyclization',
        'strategic': 'CDI closure of imidazo[4,5-c]pyridinone ring, then N-alkyl + Suzuki',
        'steps': [
          ('mol', 'Cc1cnc(Br)cc1N',  '3-Amino-5-bromo-4-methylpyridine', 'sm'),
          ('arrow', ['Fe (5 eq), AcOH', '+ 3-Bromo-4-nitropyridine'], 'EtOH/H₂O, 80 °C\n(reduce nitro → diamine)', '75–85%'),
          ('mol', 'Cc1cnc(Br)cc1Nc1cnccc1', 'Diaminopyridine\n(bromo-methyl)', 'int'),
          ('arrow', ['CDI (1.0 eq)'], 'DMF, 80 °C, 4 h', '70–80%'),
          ('mol', 'O=c1[nH]c2cnccc2n1CC(N)=O', 'Imidazo[4,5-c]pyridinone\n(N-H free)', 'int'),
          ('arrow', ['ClCH₂C(=O)NH₂ (1.1 eq)', 'K₂CO₃ (2 eq)'], 'DMF, 60 °C, 6 h', '70–80%'),
          ('mol', 'O=c1[nH]c2cnccc2n1CC(N)=O', 'N-Chloroacetamide adduct', 'int'),
          ('arrow', ['Pd(dppf)Cl₂ (5 mol%), K₂CO₃', '+ 2-Cl-4-F-phenylboronic acid'], 'dioxane/H₂O, 85 °C, 12 h', '75–85%'),
          ('mol', 'Cc1cnc(-c2cc(Cl)ccc2F)cc1-n1c(=O)n(CC(N)=O)c2cnccc21', '7977', 'prod'),
        ]
      },
    ]
  },
  { 'id': '7877', 'full_name': '7877  (furo[2,3-b]pyridine)',
    'target_smiles': 'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1',
    'routes': [
      { 'label': 'Route 2', 'tag': 'Recommended · Lautens 5-exo-dig',
        'strategic': 'Furan ring O–C2 + C3–C3(pyr) formed in one Pd/Cu intramolecular cyclization',
        'steps': [
          ('mol', 'Oc1ncccc1Br',  '3-Bromo-2-hydroxypyridine', 'sm'),
          ('arrow', ['BrCC#Cc1ccc(C(=O)OC)c(C2CCCC2)c1', 'K₂CO₃ (2 eq)'], 'DMF, RT, 12 h\n(O-propargylation)', '85–90%'),
          ('mol', 'BrCC#Cc1ccc(C(=O)OC)c(C2CCCC2)c1', 'Propargyl ester\nbromide', 'sm'),
          ('arrow', ['PdCl₂ (5 mol%), CuI (10 mol%)', 'Cs₂CO₃'], 'DMF, 80 °C, 12 h\n(5-exo-dig)', '55–70%'),
          ('mol', 'COC(=O)c1ccc(-c2coc3ncccc23)cc1C1CCCC1', '3-Bromo-5-aryl-\nfuro[2,3-b]pyridine ester', 'int'),
          ('arrow', ['m-Tolylboronic acid (1.5 eq)', 'Pd(dppf)Cl₂ (5 mol%), K₂CO₃'], 'dioxane/H₂O, 90 °C, 12 h', '70–80%'),
          ('mol', 'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)OC)c(C5CCCC5)c4)c3c2)c1', 'Methyl ester\nintermediate', 'int'),
          ('arrow', ['LiOH (3 eq)'], 'THF/H₂O, RT, 4 h', '≥95%'),
          ('mol', 'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1', '7877', 'prod'),
        ]
      },
      { 'label': 'Route 3', 'tag': 'Independent · Cyclodehydration (Majumdar)',
        'strategic': 'Furan ring formed by tandem O-alkylation / intramolecular Knoevenagel',
        'steps': [
          ('mol', 'O=Cc1cnc(Br)cc1O',  '3-Formyl-5-bromo-\n2-hydroxypyridine', 'sm'),
          ('arrow', ['m-TolBpin (1.5 eq), Pd(dppf)Cl₂', 'K₂CO₃, dioxane/H₂O, 80 °C'], 'then KOH, H₂O, reflux\n(Suzuki + 2-Cl→2-OH)', '65–75%'),
          ('mol', 'O=Cc1cnc(-c2cccc(C)c2)cc1O', '3-Formyl-5-(m-tolyl)-\n2-hydroxypyridine', 'int'),
          ('arrow', ['K₂CO₃ (2 eq)', '+ BrCH₂CO-Ar(cyclopentyl)'], 'DMF, 80 °C, 6 h\n(tandem O-alkyl / ring-close)', '45–60%'),
          ('mol', 'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)OC)c(C5CCCC5)c4)c3c2)c1', 'Methyl ester\nintermediate', 'int'),
          ('arrow', ['LiOH (3 eq)'], 'THF/H₂O, RT, 4 h', '≥95%'),
          ('mol', 'Cc1cccc(-c2cnc3occ(-c4ccc(C(=O)O)c(C5CCCC5)c4)c3c2)c1', '7877', 'prod'),
        ]
      },
    ]
  },
  { 'id': 'B54', 'full_name': 'B54',
    'target_smiles': 'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1',
    'routes': [
      { 'label': 'Route 1', 'tag': 'AiZ-validated · Recommended · Hantzsch',
        'strategic': 'Hantzsch C4=C(vinyl) from carbonyl carbon of α-bromo enone; preceded by aldol + MnO₂ oxidation',
        'steps': [
          ('mol', 'OCc1cn(C2CCCCC2)cn1', '(1-Cyclohexylimidazol-\n4-yl)methanol', 'sm'),
          ('arrow', ['MnO₂ (5 eq, activated)'], 'CH₂Cl₂, RT, 4 h', '85–92%'),
          ('mol', 'O=Cc1cn(C2CCCCC2)cn1', '(1-Cyclohexylimidazol-\n4-yl)carbaldehyde', 'int'),
          ('arrow', ['Acetone (5 eq), NaOH 10%'], 'EtOH/H₂O, RT, 2 h\n(crossed aldol)', '60–70%'),
          ('mol', 'CC(=O)C=Cc1cn(C2CCCCC2)cn1', '(E)-4-(1-Cyclohexyl-\nimidazol-4-yl)but-3-en-2-one', 'int'),
          ('arrow', ['NBS (1.1 eq), AcOH'], 'CHCl₃, 0 °C → RT\n(α-bromination)', '75–85%'),
          ('mol', 'O=C(CBr)C=Cc1cn(C2CCCCC2)cn1', 'α-Bromo enone', 'int'),
          ('arrow', ['Thiourea (1.1 eq)'], 'EtOH, reflux, 2 h\n(Hantzsch)', '70–80%'),
          ('mol', 'Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1', '2-Amino-4-(vinyl-\nimidazoyl)thiazole', 'int'),
          ('arrow', ['HATU (1.1 eq), DIPEA (3 eq)', '+ 1-(4-Picolyl)pyrrole-2-COOH'], 'DMF, RT, 12 h', '65–75%'),
          ('mol', 'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1', 'B54', 'prod'),
        ]
      },
      { 'label': 'Route 3', 'tag': 'Independent · HWE Olefination',
        'strategic': 'C4=C(vinyl) of thiazole by HWE olefination on 4-formylthiazole',
        'steps': [
          ('mol', 'O=Cc1ncs(c1)N', '2-Amino-4-formylthiazole', 'sm'),
          ('arrow', ['(EtO)₂P(O)CH₂-imidazoyl\nphosphonate (1.2 eq), NaH'], 'THF, 0 °C → RT, 2 h\n(HWE olefination)', '55–70%'),
          ('mol', 'Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1', '2-Amino-4-(vinyl-\nimidazoyl)thiazole', 'int'),
          ('arrow', ['HATU (1.1 eq), DIPEA (3 eq)', '+ 1-(4-Picolyl)pyrrole-2-COOH'], 'DMF, RT, 12 h', '65–75%'),
          ('mol', 'O=C(Nc1nc(C=Cc2cn(C3CCCCC3)cn2)cs1)c1cccn1Cc1ccncc1', 'B54', 'prod'),
        ]
      },
    ]
  },
]

# Pre-generate all molecule images (collect unique SMILES)
unique_smi = set()
for cpd in COMPOUNDS:
    unique_smi.add(cpd['target_smiles'])
    for rt in cpd['routes']:
        for s in rt['steps']:
            if s[0] == 'mol':
                unique_smi.add(s[1])

print(f"Generating SVGs for {len(unique_smi)} unique molecules...")
SVG_CACHE = {}
for smi in unique_smi:
    b = mol_b64(smi)
    if b:
        SVG_CACHE[smi] = b
print(f"Generated: {len(SVG_CACHE)}  Failed: {len(unique_smi)-len(SVG_CACHE)}")
