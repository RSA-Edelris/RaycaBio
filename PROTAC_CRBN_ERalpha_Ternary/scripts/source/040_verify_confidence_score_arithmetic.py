
# Verify confidence score arithmetic
gpu_conf = 0.47777947783470154
gpu_ptm = 0.4550328850746155
gpu_iptm = 0.3133130967617035
gpu_ligand_iptm = 0.9064819812774658

cpu_conf = 0.4483930468559265
cpu_ptm = 0.42173317074775696
cpu_iptm = 0.2734520137310028
cpu_ligand_iptm = 0.7970460057258606

print("=== RAW DELTA CALCULATIONS ===")
print(f"Δconf:        {gpu_conf - cpu_conf:.10f}  → 3dp: {gpu_conf - cpu_conf:.3f}")
print(f"Δptm:         {gpu_ptm - cpu_ptm:.10f}  → 3dp: {gpu_ptm - cpu_ptm:.3f}")
print(f"Δiptm:        {gpu_iptm - cpu_iptm:.10f}  → 3dp: {gpu_iptm - cpu_iptm:.3f}")
print(f"Δligand_iptm: {gpu_ligand_iptm - cpu_ligand_iptm:.10f}  → 3dp: {gpu_ligand_iptm - cpu_ligand_iptm:.3f}")

print()
print("=== ROUNDED 4dp INTERMEDIATES ===")
gpu_ligand_iptm_4dp = 0.9065
cpu_ligand_iptm_4dp = 0.7970
print(f"Rounded GPU  : {gpu_ligand_iptm_4dp}")
print(f"Rounded CPU  : {cpu_ligand_iptm_4dp}")
print(f"Δ from rounded: {gpu_ligand_iptm_4dp - cpu_ligand_iptm_4dp:.4f}  → 3dp: {gpu_ligand_iptm_4dp - cpu_ligand_iptm_4dp:.3f}")

print()
print("=== PROTEIN_IPTM DIRECTION CHECK ===")
print("GPU model_0:")
print(f"  protein_iptm (JSON top-level): 0.16041286289691925")
print(f"  pair_chains_iptm[0][1] (ERα→CRBN): 0.16041286289691925")
print(f"  pair_chains_iptm[1][0] (CRBN→ERα): 0.15849392116069794")
print(f"  Match with [0][1]: {abs(0.16041286289691925 - 0.16041286289691925) < 1e-12}")
print(f"  Match with [1][0]: {abs(0.16041286289691925 - 0.15849392116069794) < 1e-6}")

print()
print("CPU baseline:")
print(f"  protein_iptm (JSON top-level): 0.16132786870002747")
print(f"  pair_chains_iptm[0][1] (ERα→CRBN): 0.1524539440870285")
print(f"  pair_chains_iptm[1][0] (CRBN→ERα): 0.16132786870002747")
print(f"  Match with [0][1]: {abs(0.16132786870002747 - 0.1524539440870285) < 1e-6}")
print(f"  Match with [1][0]: {abs(0.16132786870002747 - 0.16132786870002747) < 1e-12}")

print()
print("=== MAX HYPOTHESIS FOR PROTEIN_IPTM ===")
gpu_max = max(0.16041286289691925, 0.15849392116069794)
cpu_max = max(0.1524539440870285, 0.16132786870002747)
print(f"GPU max protein-prot pair: {gpu_max:.20f}")
print(f"GPU protein_iptm:          0.16041286289691925")
print(f"Match: {abs(gpu_max - 0.16041286289691925) < 1e-15}")
print(f"CPU max protein-prot pair: {cpu_max:.20f}")
print(f"CPU protein_iptm:          0.16132786870002747")
print(f"Match: {abs(cpu_max - 0.16132786870002747) < 1e-15}")
