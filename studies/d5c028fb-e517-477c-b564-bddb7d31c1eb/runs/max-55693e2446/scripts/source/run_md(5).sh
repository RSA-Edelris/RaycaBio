#!/bin/bash
# =============================================================================
# CDK2-CCNE PPI stabiliser MD pilot: 6 compounds × 3 replicas × 10 ns
# Protocol:  AMBER14SB protein + GAFF2/Gasteiger ligand + TIP3P water
# Box:       dodecahedron, 1.2 nm buffer
# Ions:      0.15 M NaCl + neutralisation (protein net -4e → 4 Na+ added)
# EM:        steepest descent, 50 000 steps, Fmax ≤ 100 kJ/mol/nm, PME CPU
# NVT eq:    100 ps, V-rescale 300 K, PME GPU, pos. restraints
# NPT eq:    500 ps, Parrinello-Rahman 1 bar, PME GPU, pos. restraints
# Prod MD:   10 ns (5 M steps × 2 fs), no restraints, PME GPU
# Analysis:  ligand RMSD, protein-lig H-bonds, min chain-chain dist, SASA/BSA
# Replicas:  3 per compound; seeds 1001/2002/3003
# Fix v2:    ions.itp → ions_tip3p.itp (GROMACS 2026.1 renamed it per water model)
#            explicit || exit 1 guards replace set -e inside function body
# =============================================================================

set -euo pipefail

# ── Paths ─────────────────────────────────────────────────────────────────────
GMX=/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi
export GMXLIB=/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/share/gromacs/top
PYTHON3=/opt/cray/pe/python/3.11.7/bin/python3
JOBDIR=$(pwd)                          # run_on_cluster stages inputs here
SCRATCH=/scratch/u6sp/hpcuser.u6sp/md_cdk2_$$   # Isambard scratch FS
mkdir -p "$SCRATCH"
echo "Job dir: $JOBDIR"
echo "Scratch: $SCRATCH"
echo "GMXLIB: $GMXLIB"
echo "GMX: $($GMX --version 2>&1 | head -1)"

# Verify ions_tip3p.itp is present (GROMACS 2026.1 renamed ions.itp per water model)
if [ ! -f "$GMXLIB/amber14sb.ff/ions_tip3p.itp" ]; then
    echo "FATAL: $GMXLIB/amber14sb.ff/ions_tip3p.itp not found — aborting"
    exit 1
fi
echo "ions_tip3p.itp: OK"

# Copy all inputs to scratch
cp -r "$JOBDIR"/. "$SCRATCH"/

# ── Compound definitions ───────────────────────────────────────────────────────
ACTIVES="EDS00495858 EDS00480994 EDS00444974"
INACTIVES="EDS00481054 EDS00441134 EDS00445742"
ALL_CPDS="$ACTIVES $INACTIVES"
SEEDS=(1001 2002 3003)

# ── Helper: build combined GRO (protein + ligand) ─────────────────────────────
combine_gro() {
    local prot_gro=$1 lig_gro=$2 out_gro=$3
    local N1 N2 NTOT
    N1=$(sed -n '2p' "$prot_gro" | tr -d ' ')
    N2=$(sed -n '2p' "$lig_gro"  | tr -d ' ')
    NTOT=$((N1 + N2))
    echo "CDK2-CCNE complex" > "$out_gro"
    echo "  $NTOT"           >> "$out_gro"
    tail -n +3 "$prot_gro"   | head -n "$N1" >> "$out_gro"
    tail -n +3 "$lig_gro"    | head -n "$N2" >> "$out_gro"
    tail -1    "$prot_gro"                   >> "$out_gro"
}

# ── Per-system MD pipeline ─────────────────────────────────────────────────────
# NOTE: set -e is suppressed by bash for functions called with || or in if-tests.
# Every critical step therefore carries an explicit || exit 1 so failures propagate.
run_system() {
    local CID=$1 REP=$2 SEED=${SEEDS[$((REP-1))]}
    cd "$SCRATCH"
    local DIR="$SCRATCH/${CID}_rep${REP}"
    mkdir -p "$DIR" && cd "$DIR"
    echo "=== ${CID} replica ${REP} (seed ${SEED}) ==="

    # 1. Copy per-compound topology files
    cp "$SCRATCH"/${CID}_topol.top             topol.top                         || exit 1
    cp "$SCRATCH"/posre_${CID}.itp             .                                 || exit 1
    cp "$SCRATCH"/protein_Protein_chain_A.itp  .                                 || exit 1
    cp "$SCRATCH"/protein_Protein_chain_B.itp  .                                 || exit 1
    cp "$SCRATCH"/protein_posre_Protein_chain_A.itp  .                           || exit 1
    cp "$SCRATCH"/protein_posre_Protein_chain_B.itp  .                           || exit 1
    cp "$SCRATCH"/em.mdp "$SCRATCH"/npt.mdp "$SCRATCH"/md.mdp .                  || exit 1
    sed "s/SEED/${SEED}/" "$SCRATCH"/nvt.mdp > nvt.mdp                           || exit 1

    # 2. Combine protein + ligand GRO
    combine_gro "$SCRATCH"/protein.gro "$SCRATCH"/${CID}.gro complex.gro         || exit 1

    # 3. Dodecahedral box (1.2 nm buffer)
    $GMX editconf -f complex.gro -o box.gro -bt dodecahedron -d 1.2 -quiet        || exit 1

    # 4. Solvate (TIP3P); solvate appends SOL count to topol.top
    $GMX solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top -quiet      || exit 1

    # 5. grompp tpr for genion (ions_tip3p.itp is included in topol.top)
    $GMX grompp -f em.mdp -c solv.gro -p topol.top -o ions.tpr -maxwarn 2 -quiet || exit 1

    # 6. Add ions: neutralise -4e + 0.15 M NaCl
    echo "SOL" | $GMX genion -s ions.tpr -o ions.gro -p topol.top \
        -pname NA -nname CL -neutral -conc 0.15 -quiet                            || exit 1

    # 7. Generate default GROMACS index groups (gives Backbone, Protein, etc.)
    echo "q" | $GMX make_ndx -f ions.gro -o default.ndx -quiet 2>/dev/null       || exit 1

    # 8. Append custom analysis groups (ChainA_CDK2, ChainB_CyclinE, LIG …)
    $PYTHON3 "$SCRATCH"/create_ndx.py ions.gro default.ndx analysis.ndx "$CID"   || exit 1

    # 9. Energy minimisation (PME CPU — confirmed by Isambard site notes)
    $GMX grompp -f em.mdp -c ions.gro -p topol.top -o em.tpr -maxwarn 2 -quiet   || exit 1
    $GMX mdrun -v -deffnm em -ntomp 8 -nb gpu -pme cpu 2>&1 | tail -5
    [ -f em.gro ] || { echo "FATAL: em.gro missing after mdrun"; exit 1; }
    echo "  EM done"

    # 10. NVT equilibration 100 ps (PME GPU, position restraints)
    $GMX grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top \
        -n analysis.ndx -o nvt.tpr -maxwarn 2 -quiet                              || exit 1
    $GMX mdrun -v -deffnm nvt -ntomp 8 -nb gpu -pme gpu 2>&1 | tail -5
    [ -f nvt.gro ] || { echo "FATAL: nvt.gro missing after mdrun"; exit 1; }
    echo "  NVT done"

    # 11. NPT equilibration 500 ps (PME GPU, position restraints)
    $GMX grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top \
        -n analysis.ndx -o npt.tpr -maxwarn 2 -quiet                              || exit 1
    $GMX mdrun -v -deffnm npt -ntomp 8 -nb gpu -pme gpu 2>&1 | tail -5
    [ -f npt.gro ] || { echo "FATAL: npt.gro missing after mdrun"; exit 1; }
    echo "  NPT done"

    # 12. Production MD 10 ns (PME GPU, no restraints)
    $GMX grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top \
        -n analysis.ndx -o md.tpr -maxwarn 2 -quiet                               || exit 1
    $GMX mdrun -v -deffnm md -ntomp 8 -nb gpu -pme gpu 2>&1 | tail -5
    [ -f md.xtc ] || { echo "FATAL: md.xtc missing after mdrun"; exit 1; }
    echo "  MD done: ${CID} rep${REP}"

    cd "$SCRATCH"
}

# ── Analysis for one completed system ──────────────────────────────────────────
stats_xvg() {
    awk '!/^[@#]/{s+=$2; s2+=$2*$2; n++} END{
        if(n>0){m=s/n; v=s2/n-m*m; printf "%.5f %.5f %d\n", m, (v>0?sqrt(v):0), n}
        else{print "0 0 0"}
    }' "$1" 2>/dev/null || echo "0 0 0"
}

analyse_system() {
    local CID=$1 REP=$2
    local SDIR="$SCRATCH/${CID}_rep${REP}"
    cd "$SDIR"
    echo "--- Analysing ${CID} rep${REP} ---"
    if [ ! -f md.xtc ]; then
        echo "WARN: md.xtc missing for ${CID} rep${REP} — skipping"
        echo "${CID},${REP},NA,NA,NA,NA,NA,NA,NA" >> "$RAYCA_OUT/md_results.csv"
        cd "$SCRATCH"; return
    fi

    # a. Ligand RMSD — fit to protein Backbone, measure LIG heavy atoms
    echo -e "Backbone\nLIG" | $GMX rms \
        -f md.xtc -s md.tpr -n analysis.ndx \
        -o rmsd_lig.xvg -quiet 2>&1 | grep -v "^$" | tail -3

    # b. Protein-ligand H-bond count over time
    # GROMACS 2026: hbond uses -r/-t selection flags, not stdin group prompts
    $GMX hbond \
        -f md.xtc -s md.tpr -n analysis.ndx \
        -num hbond_prot_lig.xvg -quiet \
        -r 'group "Protein"' -t 'group "LIG"' 2>&1 | grep -v "^$" | tail -3

    # c. Minimum inter-chain distance (proteins stay associated?)
    echo -e "ChainA_CDK2\nChainB_CyclinE" | $GMX mindist \
        -f md.xtc -s md.tpr -n analysis.ndx \
        -od mindist_chains.xvg -quiet 2>&1 | grep -v "^$" | tail -3

    # d. SASA per chain and complex for BSA = (SASA_A + SASA_B - SASA_AB) / 2
    # GROMACS 2026: sasa uses -surface <selection>, not stdin group prompts
    $GMX sasa -f md.xtc -s md.tpr -n analysis.ndx \
        -o sasa_A.xvg -probe 0.14 -ndots 24 -quiet \
        -surface 'group "ChainA_CDK2"' 2>&1 | tail -2
    $GMX sasa -f md.xtc -s md.tpr -n analysis.ndx \
        -o sasa_B.xvg -probe 0.14 -ndots 24 -quiet \
        -surface 'group "ChainB_CyclinE"' 2>&1 | tail -2
    $GMX sasa -f md.xtc -s md.tpr -n analysis.ndx \
        -o sasa_AB.xvg -probe 0.14 -ndots 24 -quiet \
        -surface 'group "Protein"' 2>&1 | tail -2

    # e. Summarise each metric
    local R_MEAN R_STD HB_MEAN HB_STD MD_MEAN MD_STD
    read R_MEAN  R_STD  _ < <(stats_xvg rmsd_lig.xvg)
    read HB_MEAN HB_STD _ < <(stats_xvg hbond_prot_lig.xvg)
    read MD_MEAN MD_STD _ < <(stats_xvg mindist_chains.xvg)

    local A_MEAN B_MEAN AB_MEAN BSA_MEAN
    A_MEAN=$(awk  '!/^[@#]/{s+=$2;n++}END{if(n>0)printf "%.5f\n",s/n;else print "0"}' sasa_A.xvg)
    B_MEAN=$(awk  '!/^[@#]/{s+=$2;n++}END{if(n>0)printf "%.5f\n",s/n;else print "0"}' sasa_B.xvg)
    AB_MEAN=$(awk '!/^[@#]/{s+=$2;n++}END{if(n>0)printf "%.5f\n",s/n;else print "0"}' sasa_AB.xvg)
    BSA_MEAN=$(awk -v a="$A_MEAN" -v b="$B_MEAN" -v ab="$AB_MEAN" \
        'BEGIN{printf "%.5f\n", (a+b-ab)/2}')

    echo "${CID},${REP},${R_MEAN},${R_STD},${HB_MEAN},${HB_STD},${MD_MEAN},${MD_STD},${BSA_MEAN}" \
        >> "$RAYCA_OUT/md_results.csv"
    echo "  RMSD=${R_MEAN}±${R_STD} nm  HB=${HB_MEAN}±${HB_STD}  "\
         "MinDist=${MD_MEAN}±${MD_STD} nm  BSA=${BSA_MEAN} nm²"

    # Copy xvg output files
    local OUTDIR="$RAYCA_OUT/${CID}_rep${REP}"
    mkdir -p "$OUTDIR"
    cp rmsd_lig.xvg hbond_prot_lig.xvg mindist_chains.xvg \
       sasa_A.xvg sasa_B.xvg sasa_AB.xvg \
       em.log md.log "$OUTDIR"/ 2>/dev/null || true

    cd "$SCRATCH"
}

# ── CSV header ────────────────────────────────────────────────────────────────
mkdir -p "$RAYCA_OUT"
echo "compound,replica,rmsd_mean_nm,rmsd_std_nm,hbond_mean,hbond_std,"\
"mindist_mean_nm,mindist_std_nm,bsa_mean_nm2" > "$RAYCA_OUT/md_results.csv"

# ── Main loop: 18 systems sequentially ───────────────────────────────────────
for CID in $ALL_CPDS; do
    for REP in 1 2 3; do
        run_system "$CID" "$REP" || {
            echo "ERROR: run_system failed for ${CID} rep${REP} — continuing"
            echo "${CID},${REP},FAILED,FAILED,FAILED,FAILED,FAILED,FAILED,FAILED" \
                >> "$RAYCA_OUT/md_results.csv"
        }
    done
done

# ── Analysis pass ─────────────────────────────────────────────────────────────
for CID in $ALL_CPDS; do
    for REP in 1 2 3; do
        analyse_system "$CID" "$REP" || echo "Analysis error ${CID} rep${REP}"
    done
done

# ── Print final table ─────────────────────────────────────────────────────────
echo ""
echo "============= MD RESULTS SUMMARY ============="
cat "$RAYCA_OUT/md_results.csv"
echo "==============================================="
echo "All results in: $RAYCA_OUT"
