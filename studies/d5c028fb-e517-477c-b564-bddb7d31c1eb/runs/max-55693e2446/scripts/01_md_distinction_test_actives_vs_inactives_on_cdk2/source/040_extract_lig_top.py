
import os, re

MD = '/home/ubuntu/rayca-sessions/d5c028fb-e517-477c-b564-bddb7d31c1eb-396fce89620d/md_prep'
INP = f'{MD}/inputs'

cpd_ids = ['EDS00495858','EDS00480994','EDS00444974','EDS00481054','EDS00441134','EDS00445742']
cpd_class = {'EDS00495858':'active','EDS00480994':'active','EDS00444974':'active',
             'EDS00481054':'inactive','EDS00441134':'inactive','EDS00445742':'inactive'}

def extract_lig_top(top_path):
    text = open(top_path).read()
    at_match = re.search(r'\[ atomtypes \].*?(?=\[ moleculetype \])', text, re.DOTALL)
    atomtypes = at_match.group(0).strip() if at_match else ''
    mol_match = re.search(r'(\[ moleculetype \].*)', text, re.DOTALL)
    mol_block = mol_match.group(1).strip() if mol_match else ''
    return atomtypes, mol_block

for cid in cpd_ids:
    top_path = f'{MD}/{cid}_gmx/{cid}.amb2gmx/{cid}_GMX.top'
    atomtypes, mol_block = extract_lig_top(top_path)
    
    # Complete combined topology with correct [ molecules ] section
    # (solvate/genion will append SOL and ion lines automatically)
    top = f"""; Combined topology: CDK2-CCNE + {cid}
; Force field: AMBER14SB (protein) + GAFF2/Gasteiger (ligand)
; Water: TIP3P   Ions: NaCl at 0.15 M

; AMBER14SB force field
#include "amber14sb.ff/forcefield.itp"

; GAFF2 atom types for ligand {cid}
{atomtypes}

; Chain A — CDK2 (AMBER14SB)
#include "protein_Protein_chain_A.itp"
#ifdef POSRES
#include "protein_posre_Protein_chain_A.itp"
#endif

; Chain B — Cyclin E (AMBER14SB)
#include "protein_Protein_chain_B.itp"
#ifdef POSRES
#include "protein_posre_Protein_chain_B.itp"
#endif

; Ligand {cid} (GAFF2 + Gasteiger charges)
{mol_block}

#ifdef POSRES
#include "posre_{cid}.itp"
#endif

; TIP3P water
#include "amber14sb.ff/tip3p.itp"

; Ions
#include "amber14sb.ff/ions.itp"

[ system ]
CDK2-CCNE + {cid} ({cpd_class[cid]})

[ molecules ]
Protein_chain_A   1
Protein_chain_B   1
 {cid}            1
"""
    with open(f'{INP}/{cid}_topol.top', 'w') as f:
        f.write(top)
    
    print(f'{cid}: topol.top written ({len(top)} chars)')

print('\nAll combined topologies written to inputs/')
