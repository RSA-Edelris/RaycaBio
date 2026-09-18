#!/bin/bash
# =============================================================================
# CDK2-CCNE PPI stabiliser MD pilot: 6 compounds × 3 replicas × 20 ns
# Protocol:  AMBER14SB protein + GAFF2/Gasteiger ligand + TIP3P water
# Box:       dodecahedron, 1.2 nm buffer
# Ions:      0.15 M NaCl + neutralisation (protein net -4e → 4 Na+ added)
# EM:        steepest descent, 50 000 steps, Fmax ≤ 100 kJ/mol/nm, PME CPU
# NVT eq:    100 ps, V-rescale 300 K, PME GPU, pos. restraints
# NPT eq:    500 ps, Parrinello-Rahman 1 bar, PME GPU, pos. restraints
# Prod MD:   20 ns (10 M steps × 2 fs), no restraints, PME GPU
# Analysis:  ligand RMSD, protein-lig H-bonds, min chain-chain dist, SASA/BSA
# =============================================================================

set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────────────────
GMX=/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi
export GMXLIB=/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/share/gromacs/top
PYTHON3=/opt/cray/pe/python/3.11.7/bin/python3
SCRATCH=/scratch/u6sp/hpcuser.u6sp/md_cdk2_$$
INDIR=$RAYCA_OUT/inputs        # inputs were staged here by run_on_cluster

mkdir -p "$SCRATCH"
echo "Working directory: $SCRATCH"
echo "GMXLIB: $GMXLIB"

# Copy all inputs to scratch
cp -r "$INDIR"/. "$SCRATCH"/

cd "$SCRATCH"

# ── Compound definitions ─────────────────────────────────────────────────────
ACTIVES="EDS00495858 EDS00480994 EDS00444974"
INACTIVES="EDS00481054 EDS00441134 EDS00445742"
ALL_CPDS="$ACTIVES $INACTIVES"
N_REPLICAS=3
SEEDS=(1001 2002 3003)

# Protein chain atom counts (from pdb2gmx, used by create_ndx.py)
CHAIN_A_ATOMS=4859
CHAIN_B_ATOMS=4375

# ── Helper: build combined GRO (protein + ligand) ───────────────────────────
combine_gro() {
    local prot_gro=$1 lig_gro=$2 out_gro=$3
    local N1=$(sed -n '2p' "$prot_gro" | tr -d ' ')
    local N2=$(sed -n '2p' "$lig_gro" | tr -d ' ')
    local NTOT=$((N1 + N2))
    echo "CDK2-CCNE complex" > "$out_gro"
    echo "  $NTOT" >> "$out_gro"
    # protein atoms (skip title + count + box)
    tail -n +3 "$prot_gro" | head -n "$N1" >> "$out_gro"
    # ligand atoms (skip title + count + box)
    tail -n +3 "$lig_gro" | head -n "$N2" >> "$out_gro"
    # box from protein
    tail -1 "$prot_gro" >> "$out_gro"
}

# ── Per-system MD pipeline ───────────────────────────────────────────────────
run_system() {
    local CID=$1 REP=$2 SEED=${SEEDS[$((REP-1))]}
    local DIR="$SCRATCH/${CID}_rep${REP}"
    mkdir -p "$DIR" && cd "$DIR"
    echo "=== ${CID} replica ${REP} (seed ${SEED}) ==="

    # 1. Copy topology + MDP files
    cp "$SCRATCH"/${CID}_topol.top topol.top
    cp "$SCRATCH"/${CID}_atomtypes.itp .
    cp "$SCRATCH"/${CID}_mol.itp .
    cp "$SCRATCH"/posre_${CID}.itp .
    cp "$SCRATCH"/protein_Protein_chain_A.itp .
    cp "$SCRATCH"/protein_Protein_chain_B.itp .
    cp "$SCRATCH"/protein_posre_Protein_chain_A.itp .
    cp "$SCRATCH"/protein_posre_Protein_chain_B.itp .
    cp "$SCRATCH"/em.mdp "$SCRATCH"/npt.mdp "$SCRATCH"/md.mdp .
    sed "s/SEED/${SEED}/" "$SCRATCH"/nvt.mdp > nvt.mdp

    # 2. Combine protein + ligand GRO
    combine_gro "$SCRATCH"/protein.gro "$SCRATCH"/${CID}.gro complex.gro

    # 3. Create dodecahedral box (1.2 nm buffer)
    $GMX editconf -f complex.gro -o box.gro -bt dodecahedron -d 1.2 -quiet

    # 4. Solvate (TIP3P; solvate auto-appends SOL count to topol.top)
    $GMX solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top -quiet

    # 5. Generate tpr for genion
    $GMX grompp -f em.mdp -c solv.gro -p topol.top -o ions.tpr \
        -maxwarn 2 -quiet

    # 6. Add ions (neutralise -4e + 0.15 M NaCl; genion appends to topol.top)
    echo "SOL" | $GMX genion -s ions.tpr -o ions.gro -p topol.top \
        -pname NA -nname CL -neutral -conc 0.15 -quiet

    # 7. Build analysis index using the Python helper
    $PYTHON3 "$SCRATCH"/create_ndx.py ions.gro analysis.ndx "$CID"

    # 8. Energy minimisation (PME CPU — as confirmed by Isambard site notes)
    $GMX grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr -maxwarn 2 -quiet
    $GMX mdrun -v -deffnm em -ntomp 8 -nb gpu -pme cpu 2>&1 | tail -5

    # 9. NVT equilibration (PME GPU)
    $GMX grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top \
        -n analysis.ndx -o nvt.tpr -maxwarn 2 -quiet
    $GMX mdrun -v -deffnm nvt -ntomp 8 -nb gpu -pme gpu 2>&1 | tail -5

    # 10. NPT equilibration (PME GPU)
    $GMX grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top \
        -n analysis.ndx -o npt.tpr -maxwarn 2 -quiet
    $GMX mdrun -v -deffnm npt -ntomp 8 -nb gpu -pme gpu 2>&1 | tail -5

    # 11. Production MD (PME GPU, 20 ns)
    $GMX grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top \
        -n analysis.ndx -o md.tpr -maxwarn 2 -quiet
    $GMX mdrun -v -deffnm md -ntomp 8 -nb gpu -pme gpu 2>&1 | tail -5

    echo "=== ${CID} rep${REP}: MD complete ==="
    cd "$SCRATCH"
}

# ── Analysis for one completed system ────────────────────────────────────────
analyse_system() {
    local CID=$1 REP=$2
    local DIR="$SCRATCH/${CID}_rep${REP}"
    cd "$DIR"
    echo "--- Analysing ${CID} rep${REP} ---"
    if [ ! -f md.xtc ]; then
        echo "WARN: md.xtc missing for ${CID} rep${REP} — skipping analysis"
        return
    fi

    # a. Ligand RMSD — fit to protein Cα, measure ligand heavy atoms
    #    Group 3 = Backbone (from default gmx ndx), Group 4 = LIG (custom)
    echo -e "Backbone\nLIG" | $GMX rms \
        -f md.xtc -s md.tpr -n analysis.ndx \
        -o rmsd_lig.xvg -quiet 2>&1 | tail -3

    # b. Protein-ligand H-bond count over time
    echo -e "Protein\nLIG" | $GMX hbond \
        -f md.xtc -s md.tpr -n analysis.ndx \
        -num hbond_prot_lig.xvg -quiet 2>&1 | tail -3

    # c. Minimum inter-chain distance (proxy for protein-protein association)
    echo -e "ChainA_CDK2\nChainB_CyclinE" | $GMX mindist \
        -f md.xtc -s md.tpr -n analysis.ndx \
        -od mindist_chains.xvg -quiet 2>&1 | tail -3

    # d. SASA for buried interface area
    #    BSA = (SASA_A + SASA_B - SASA_AB) / 2
    echo "ChainA_CDK2"   | $GMX sasa -f md.xtc -s md.tpr -n analysis.ndx \
        -o sasa_A.xvg -probe 0.14 -ndots 24 -quiet 2>&1 | tail -2
    echo "ChainB_CyclinE" | $GMX sasa -f md.xtc -s md.tpr -n analysis.ndx \
        -o sasa_B.xvg -probe 0.14 -ndots 24 -quiet 2>&1 | tail -2
    echo "Protein" | $GMX sasa -f md.xtc -s md.tpr -n analysis.ndx \
        -o sasa_AB.xvg -probe 0.14 -ndots 24 -quiet 2>&1 | tail -2

    # e. Extract mean ± std from xvg files (skip @/#-comment lines)
    stats_xvg() {
        local f=$1
        awk '!/^[@#]/{s+=$2; s2+=$2*$2; n++} END{
            if(n>0){m=s/n; v=s2/n-m*m; print m, (v>0?sqrt(v):0), n}
            else{print "0 0 0"}
        }' "$f" 2>/dev/null || echo "0 0 0"
    }

    R_LIG=$(stats_xvg rmsd_lig.xvg)
    HB=$(stats_xvg hbond_prot_lig.xvg)
    DIST=$(stats_xvg mindist_chains.xvg)

    # BSA: compute from 3 SASA files
    BSA=$(awk '!/^[@#]/{a+=$2;na++} END{if(na>0) print a/na; else print "0"}' sasa_A.xvg 2>/dev/null || echo 0)
    BSA_B=$(awk '!/^[@#]/{a+=$2;na++} END{if(na>0) print a/na; else print "0"}' sasa_B.xvg 2>/dev/null || echo 0)
    BSA_AB=$(awk '!/^[@#]/{a+=$2;na++} END{if(na>0) print a/na; else print "0"}' sasa_AB.xvg 2>/dev/null || echo 0)
    BSA_VAL=$(awk -v a="$BSA" -v b="$BSA_B" -v ab="$BSA_AB" 'BEGIN{print (a+b-ab)/2}')

    # Write per-system result line
    echo "${CID},${REP},${R_LIG},${HB},${DIST},${BSA_VAL}" >> "$RAYCA_OUT/md_results.csv"
    echo "  RMSD_lig=${R_LIG} HBonds=${HB} MinDist=${DIST} BSA=${BSA_VAL}"

    # Copy key xvg files to RAYCA_OUT
    OUTDIR="$RAYCA_OUT/${CID}_rep${REP}"
    mkdir -p "$OUTDIR"
    cp rmsd_lig.xvg hbond_prot_lig.xvg mindist_chains.xvg sasa_A.xvg sasa_B.xvg sasa_AB.xvg "$OUTDIR"/ 2>/dev/null || true

    cd "$SCRATCH"
}

# ── Write CSV header ─────────────────────────────────────────────────────────
echo "compound,replica,rmsd_mean_nm,rmsd_std_nm,hbond_mean,hbond_std,"\
"mindist_mean_nm,mindist_std_nm,bsa_mean_nm2" > "$RAYCA_OUT/md_results.csv"

# ── Main loop: run all 18 systems sequentially ───────────────────────────────
for CID in $ALL_CPDS; do
    for REP in 1 2 3; do
        run_system "$CID" "$REP" || echo "ERROR in ${CID} rep${REP}, continuing"
    done
done

# ── Analysis pass ─────────────────────────────────────────────────────────────
for CID in $ALL_CPDS; do
    for REP in 1 2 3; do
        analyse_system "$CID" "$REP" || echo "Analysis error ${CID} rep${REP}"
    done
done

# ── Summarise ────────────────────────────────────────────────────────────────
echo ""
echo "======= RESULTS SUMMARY ======="
cat "$RAYCA_OUT/md_results.csv"
echo "================================"

# ── Copy GROMACS log files for inspection ─────────────────────────────────────
for CID in $ALL_CPDS; do
    for REP in 1 2 3; do
        DIR="$SCRATCH/${CID}_rep${REP}"
        OUTDIR="$RAYCA_OUT/${CID}_rep${REP}"
        mkdir -p "$OUTDIR"
        cp "$DIR"/md.log "$OUTDIR"/ 2>/dev/null || true
        cp "$DIR"/em.log "$OUTDIR"/ 2>/dev/null || true
    done
done

echo "All results written to $RAYCA_OUT"
