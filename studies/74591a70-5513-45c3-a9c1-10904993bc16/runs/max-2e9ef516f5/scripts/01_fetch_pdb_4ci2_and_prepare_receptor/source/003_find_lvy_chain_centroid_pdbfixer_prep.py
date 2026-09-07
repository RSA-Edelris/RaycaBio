
# ─── find LVY chain + centroid, then PDBFixer prep ────────────────────────────
from pdbfixer import PDBFixer
from openmm.app import PDBFile
import numpy as np

# --- find LVY coords and chain ---
lvy_coords, lvy_chain = [], None
with open(raw_pdb) as f:
    for line in f:
        if line[:6].strip() == "HETATM" and line[17:20].strip() == "LVY":
            lvy_chain = line[21]
            x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            lvy_coords.append([x, y, z])

lvy_coords = np.array(lvy_coords)
centroid = lvy_coords.mean(axis=0)
print(f"LVY on chain {lvy_chain}, {len(lvy_coords)} atoms")
print(f"Centroid:  X={centroid[0]:.3f}  Y={centroid[1]:.3f}  Z={centroid[2]:.3f}")
print(f"Box centre will be: {centroid.round(2).tolist()}")

# Save LVY ligand as SDF for reference / fpocket control
lvy_lines = []
with open(raw_pdb) as f:
    for line in f:
        if line[:6].strip() == "HETATM" and line[17:20].strip() == "LVY":
            lvy_lines.append(line)
print(f"LVY PDB excerpt:\n{''.join(lvy_lines[:3])}...")

# ─── PDBFixer: chain A (CRBN), keep ZN and waters, repair, protonate pH 7.4 ──
fixer = PDBFixer(filename=raw_pdb)

# Identify all chains
chain_ids = [c.id for c in fixer.topology.chains()]
print(f"\nAll topology chains: {chain_ids}")

# Remove chain B (DDB1) - keep only CRBN (chain A)
chains_to_remove = [i for i, c in enumerate(fixer.topology.chains()) if c.id == 'B']
print(f"Removing chain indices {chains_to_remove} (DDB1)")
fixer.removeChains(chains_to_remove)

# Fill missing residues and atoms
fixer.findMissingResidues()
n_missing_res = sum(len(v) for v in fixer.missingResidues.values())
print(f"Missing residue stretches to add: {len(fixer.missingResidues)} segments ({n_missing_res} residues)")

# Remove terminal missing residues (often unresolved tails) unless they border the pocket
# Strategy: keep internal gaps only (standard practice to avoid modelling floppy termini)
chains_topology = list(fixer.topology.chains())
for key in list(fixer.missingResidues.keys()):
    chain_idx, res_idx = key
    chain = chains_topology[chain_idx]
    n_res = sum(1 for _ in chain.residues())
    # drop if at N-terminus (res_idx==0) or C-terminus (res_idx==n_res)
    if res_idx == 0 or res_idx >= n_res:
        del fixer.missingResidues[key]
n_kept = sum(len(v) for v in fixer.missingResidues.values())
print(f"After removing terminal tails: {n_kept} residues to model")

fixer.findNonstandardResidues()
print(f"Non-standard residues: {fixer.nonstandardResidues}")
fixer.replaceNonstandardResidues()

fixer.findMissingAtoms()
fixer.addMissingAtoms()
print("Missing atoms added.")

# Add H at pH 7.4 (assigns His tautomers, Asp/Glu/Lys/Arg protonation automatically)
fixer.addMissingHydrogens(7.4)
print("Hydrogens added at pH 7.4.")

# Save receptor WITH LVY and ZN and waters (full)
full_rec_path = f"{WORK}/4CI2_chainA_full.pdb"
with open(full_rec_path, 'w') as out:
    PDBFile.writeFile(fixer.topology, fixer.positions, out, keepIds=True)
print(f"Full repaired chain A → {full_rec_path}")
