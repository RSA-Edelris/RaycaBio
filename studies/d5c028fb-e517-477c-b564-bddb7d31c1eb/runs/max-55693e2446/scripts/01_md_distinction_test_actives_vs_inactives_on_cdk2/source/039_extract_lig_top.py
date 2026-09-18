
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
    
    # Write atomtypes-only itp
    with open(f'{INP}/{cid}_atomtypes.itp', 'w') as f:
        f.write(f'; GAFF2 atom types for {cid}\n')
        f.write(atomtypes + '\n')
    
    # Write molecule-only itp (no atomtypes/defaults)
    with open(f'{INP}/{cid}_mol.itp', 'w') as f:
        f.write(f'; Molecule topology for {cid} — GAFF2+Gasteiger\n')
        f.write(mol_block + '\n')
    
    # Copy posre itp
    posre_src = f'{MD}/{cid}_gmx/{cid}.amb2gmx/posre_{cid}.itp'
    os.system(f'cp {posre_src} {INP}/posre_{cid}.itp')

    # Count ligand atoms from gro
    gro_lines = open(f'{INP}/{cid}.gro').readlines()
    n_lig_atoms = int(gro_lines[1].strip())
    
    # Build combined topology
    top = f"""; Combined topology: CDK2-CCNE + {cid}
; Force field: AMBER14SB (protein) + GAFF2/Gasteiger (ligand)
; Water: TIP3P
; Generated for pilot MD comparison study

; AMBER14SB force field
#include "amber14sb.ff/forcefield.itp"

; Additional GAFF2 atom types (ligand {cid})
#include "{cid}_atomtypes.itp"

; Protein chains (AMBER14SB)
#include "protein_Protein_chain_A.itp"

; Position restraints for chain A (used during equilibration)
#ifdef POSRES
#include "protein_posre_Protein_chain_A.itp"
#endif

#include "protein_Protein_chain_B.itp"

; Position restraints for chain B
#ifdef POSRES
#include "protein_posre_Protein_chain_B.itp"
#endif

; Ligand molecule
#include "{cid}_mol.itp"

; Position restraints for ligand
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
; The exact counts will be written by the cluster script after solvation
; Protein_chain_A   1
; Protein_chain_B   1
; {cid}              1
; SOL               NWAT
; NA                NNA
; CL                NCL
"""
    with open(f'{INP}/{cid}_complex.top', 'w') as f:
        f.write(top)
    
    print(f'{cid}: {n_lig_atoms} lig atoms, atomtypes.itp + mol.itp + complex.top written')

print('\nAll per-compound topology files ready')
