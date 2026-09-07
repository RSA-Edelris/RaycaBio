#!/bin/bash
#SBATCH --job-name=abfe_missing
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --gres=gpu:4
#SBATCH --time=02:00:00
#SBATCH --partition=workq
#SBATCH --output=abfe_missing_%j.out
#SBATCH --error=abfe_missing_%j.err

# Run from the directory containing all input files.
# Collect results with:  cp *_dhdl.xvg /path/to/results/

set -euo pipefail

GMX=/projects/u6sp/software-aarch64/gromacs-2026.1-mpi/bin/gmx_mpi

run_window() {
    local label=$1 gro=$2 top=$3 mdp=$4 ndx=$5 dev=$6
    echo "=== [$label] GPU $dev starting at $(date) ==="
    if [ "$ndx" != "NONE" ]; then
        $GMX grompp -f "$mdp" -c "$gro" -p "$top" -n "$ndx" \
            -o "${label}.tpr" -po "${label}_mdout.mdp" -maxwarn 5 \
            > "${label}_grompp.log" 2>&1
    else
        $GMX grompp -f "$mdp" -c "$gro" -p "$top" \
            -o "${label}.tpr" -po "${label}_mdout.mdp" -maxwarn 5 \
            > "${label}_grompp.log" 2>&1
    fi
    CUDA_VISIBLE_DEVICES=$dev $GMX mdrun -v -deffnm "$label" \
        -nb gpu -pme gpu -ntomp 8 \
        > "${label}_mdrun.log" 2>&1
    echo "=== [$label] done at $(date) ==="
}

# 33 missing windows: label gro top mdp ndx
JOBS=(
"complex_EDS01806218_ent1_win12 EDS01806218_ent1_abfe_start.gro EDS01806218_ent1_complex_abfe.top EDS01806218_ent1_cplx_win12.mdp EDS01806218_ent1_index.ndx"
"complex_EDS01806218_ent1_win13 EDS01806218_ent1_abfe_start.gro EDS01806218_ent1_complex_abfe.top EDS01806218_ent1_cplx_win13.mdp EDS01806218_ent1_index.ndx"
"complex_EDS01806218_ent1_win14 EDS01806218_ent1_abfe_start.gro EDS01806218_ent1_complex_abfe.top EDS01806218_ent1_cplx_win14.mdp EDS01806218_ent1_index.ndx"
"complex_EDS01806218_ent1_win15 EDS01806218_ent1_abfe_start.gro EDS01806218_ent1_complex_abfe.top EDS01806218_ent1_cplx_win15.mdp EDS01806218_ent1_index.ndx"
"complex_EDS01806218_ent1_win16 EDS01806218_ent1_abfe_start.gro EDS01806218_ent1_complex_abfe.top EDS01806218_ent1_cplx_win16.mdp EDS01806218_ent1_index.ndx"
"solvent_EDS01806218_ent1_win16 EDS01806218_ent1_lig_solv.gro EDS01806218_ent1_lig_solv.top EDS01806218_ent1_solv_win16.mdp NONE"
"complex_EDS01806218_ent2_win12 EDS01806218_ent2_abfe_start.gro EDS01806218_ent2_complex_abfe.top EDS01806218_ent2_cplx_win12.mdp EDS01806218_ent2_index.ndx"
"complex_EDS01806218_ent2_win13 EDS01806218_ent2_abfe_start.gro EDS01806218_ent2_complex_abfe.top EDS01806218_ent2_cplx_win13.mdp EDS01806218_ent2_index.ndx"
"complex_EDS01806218_ent2_win14 EDS01806218_ent2_abfe_start.gro EDS01806218_ent2_complex_abfe.top EDS01806218_ent2_cplx_win14.mdp EDS01806218_ent2_index.ndx"
"complex_EDS01806218_ent2_win15 EDS01806218_ent2_abfe_start.gro EDS01806218_ent2_complex_abfe.top EDS01806218_ent2_cplx_win15.mdp EDS01806218_ent2_index.ndx"
"complex_EDS01806218_ent2_win16 EDS01806218_ent2_abfe_start.gro EDS01806218_ent2_complex_abfe.top EDS01806218_ent2_cplx_win16.mdp EDS01806218_ent2_index.ndx"
"complex_EDS01889984_win12 EDS01889984_abfe_start.gro EDS01889984_complex_abfe.top EDS01889984_cplx_win12.mdp EDS01889984_index.ndx"
"complex_EDS01889984_win13 EDS01889984_abfe_start.gro EDS01889984_complex_abfe.top EDS01889984_cplx_win13.mdp EDS01889984_index.ndx"
"complex_EDS01889984_win14 EDS01889984_abfe_start.gro EDS01889984_complex_abfe.top EDS01889984_cplx_win14.mdp EDS01889984_index.ndx"
"complex_EDS01889984_win15 EDS01889984_abfe_start.gro EDS01889984_complex_abfe.top EDS01889984_cplx_win15.mdp EDS01889984_index.ndx"
"complex_EDS01889984_win16 EDS01889984_abfe_start.gro EDS01889984_complex_abfe.top EDS01889984_cplx_win16.mdp EDS01889984_index.ndx"
"solvent_EDS01889984_win00 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win00.mdp NONE"
"solvent_EDS01889984_win01 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win01.mdp NONE"
"solvent_EDS01889984_win02 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win02.mdp NONE"
"solvent_EDS01889984_win03 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win03.mdp NONE"
"solvent_EDS01889984_win04 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win04.mdp NONE"
"solvent_EDS01889984_win05 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win05.mdp NONE"
"solvent_EDS01889984_win06 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win06.mdp NONE"
"solvent_EDS01889984_win07 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win07.mdp NONE"
"solvent_EDS01889984_win08 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win08.mdp NONE"
"solvent_EDS01889984_win09 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win09.mdp NONE"
"solvent_EDS01889984_win10 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win10.mdp NONE"
"solvent_EDS01889984_win11 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win11.mdp NONE"
"solvent_EDS01889984_win12 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win12.mdp NONE"
"solvent_EDS01889984_win13 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win13.mdp NONE"
"solvent_EDS01889984_win14 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win14.mdp NONE"
"solvent_EDS01889984_win15 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win15.mdp NONE"
"solvent_EDS01889984_win16 EDS01889984_lig_solv.gro EDS01889984_lig_solv.top EDS01889984_solv_win16.mdp NONE"
)

echo "Running ${#JOBS[@]} FEP windows on 4 GPUs (batches of 4)"

batch_pids=()
gpu_slot=0

for job_spec in "${JOBS[@]}"; do
    read -r label gro top mdp ndx <<< "$job_spec"
    run_window "$label" "$gro" "$top" "$mdp" "$ndx" "$gpu_slot" &
    batch_pids+=($!)
    gpu_slot=$(( (gpu_slot + 1) % 4 ))

    if [ ${#batch_pids[@]} -ge 4 ]; then
        echo "--- Waiting for batch of 4 (gpu_slot cycled back to 0) ---"
        for pid in "${batch_pids[@]}"; do
            wait "$pid" || echo "WARNING: pid $pid exited non-zero, check logs"
        done
        batch_pids=()
    fi
done

if [ ${#batch_pids[@]} -gt 0 ]; then
    echo "--- Waiting for final batch (${#batch_pids[@]} jobs) ---"
    for pid in "${batch_pids[@]}"; do
        wait "$pid" || echo "WARNING: pid $pid exited non-zero"
    done
fi

echo ""
echo "=== All windows complete ==="
echo "dhdl files produced:"
ls -1 *_dhdl.xvg 2>/dev/null | wc -l
ls -1 *_dhdl.xvg 2>/dev/null
