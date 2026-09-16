
# Duplicate check within actives, MS-artefact assessment, and deeper reactive flag analysis
from rdkit import Chem
from rdkit.Chem import inchi

# ---- Duplicate within actives by InChIKey ----
ik_seen = {}
active_dups = []
for r in results:
    ik = r['inchi_key']
    if ik in ik_seen:
        active_dups.append((r['EDS_Number'], ik_seen[ik]))
    else:
        ik_seen[ik] = r['EDS_Number']
print(f"Intra-active duplicates (by InChIKey): {len(active_dups)}")
if active_dups:
    for d in active_dups: print(f"  {d}")

# ---- Reassess reactive flags with context ----
# The broad aryl_halide SMARTS fires on F/Cl substituents which are standard med-chem handles.
# Re-examine what each "hit" actually is:
print("\n=== Reactive/Structural Flag Audit ===")
for r in results:
    if r['react'] != '-' or r['brenk'] != '-' or r['pains'] != '-':
        mol = r['mol']
        smi = r['Smiles']
        print(f"\n{r['EDS_Number']} | PAINS={r['pains']} | BRENK={r['brenk']} | REACT={r['react']}")
        print(f"  SMILES: {smi}")
        # Check for actual reactive groups: acid halides, epoxides, Michael acceptors
        # (as opposed to stable CF3, aryl-Cl, etc.)
        pat_acylhal = Chem.MolFromSmarts('[CX3](=O)[F,Cl,Br,I]')
        pat_epox    = Chem.MolFromSmarts('C1OC1')
        pat_mich_k  = Chem.MolFromSmarts('[CX3H1,CX3H0]=[CX3][CX3](=O)[!O]')  # vinyl ketone/aldehyde
        pat_mich_e  = Chem.MolFromSmarts('[CX3]=[CX3][CX3](=O)[OX2][CX4]')     # alpha,beta-unsat ester
        pat_cf3_ether = Chem.MolFromSmarts('OCC(F)(F)F')
        pat_gem_diF  = Chem.MolFromSmarts('[CX4](F)(F)')
        pat_aryl_cl = Chem.MolFromSmarts('[c][Cl]')
        pat_aryl_f  = Chem.MolFromSmarts('[c][F]')
        pat_pyr_cl  = Chem.MolFromSmarts('n[c][Cl]')
        
        flags = []
        if mol.HasSubstructMatch(pat_acylhal): flags.append('TRUE_ACID_HALIDE')
        if mol.HasSubstructMatch(pat_epox):    flags.append('TRUE_EPOXIDE')
        if mol.HasSubstructMatch(pat_mich_k):  flags.append('TRUE_MICHAEL_ACCEPTOR_ketone')
        if mol.HasSubstructMatch(pat_mich_e):  flags.append('TRUE_MICHAEL_ACCEPTOR_ester')
        if mol.HasSubstructMatch(pat_cf3_ether): flags.append('stable_CF3_ether')
        if mol.HasSubstructMatch(pat_gem_diF): flags.append('stable_gem_diF')
        if mol.HasSubstructMatch(pat_pyr_cl):  flags.append('hetAryl_Cl_activated')
        elif mol.HasSubstructMatch(pat_aryl_cl): flags.append('stable_aryl_Cl')
        if mol.HasSubstructMatch(pat_aryl_f):  flags.append('stable_aryl_F')
        print(f"  Detailed: {' | '.join(flags) if flags else 'no_true_reactive_groups'}")
