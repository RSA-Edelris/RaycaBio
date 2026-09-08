
import json, numpy as np, subprocess

# Load results
with open("mmgbsa_result.json") as f:
    res = json.load(f)

frames = res["per_frame"]
dGs    = [fr["dG_bind"] for fr in frames]
times  = [fr["time_ps"]  for fr in frames]

# Production window (100–1000 ps, frames 10-100)
prod = frames[10:]
dG_prod = [fr["dG_bind"] for fr in prod]
t_prod  = [fr["time_ps"]  for fr in prod]

mean_dG = np.mean(dG_prod)
std_dG  = np.std(dG_prod)
sem_dG  = std_dG / np.sqrt(len(dG_prod))

# Running average to show convergence
running = [np.mean(dG_prod[:i+1]) for i in range(len(dG_prod))]

print(f"Frames (all)    : {len(frames)}")
print(f"Frames (prod)   : {len(prod)} (100–1000 ps)")
print(f"ΔG_bind mean    : {mean_dG:.3f} kcal/mol")
print(f"ΔG_bind SD      : {std_dG:.3f} kcal/mol")
print(f"ΔG_bind SEM     : {sem_dG:.3f} kcal/mol")
print(f"ΔG range        : {min(dG_prod):.2f} – {max(dG_prod):.2f} kcal/mol")
print(f"Running mean at 500 ps: {running[40]:.3f}")
print(f"Running mean at 1000 ps: {running[-1]:.3f}")
print()

# Energy decomposition (mean values)
Ec = np.mean([fr["E_complex"]  for fr in prod])
Er = np.mean([fr["E_receptor"] for fr in prod])
El = np.mean([fr["E_ligand"]   for fr in prod])

print(f"<E_complex>  = {Ec:.1f} kcal/mol")
print(f"<E_receptor> = {Er:.1f} kcal/mol")
print(f"<E_ligand>   = {El:.1f} kcal/mol")
print(f"ΔG = Ec−Er−El = {Ec-Er-El:.3f} kcal/mol  ✓")
