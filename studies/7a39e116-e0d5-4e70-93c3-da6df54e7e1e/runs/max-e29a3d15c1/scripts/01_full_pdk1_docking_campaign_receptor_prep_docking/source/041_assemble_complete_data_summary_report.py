
# Assemble the complete data summary for the report
print("=== DOCKING SCORES ===")
for i, d in enumerate(pose_data, 1):
    print(f"Pose {i}: Vina={d.get('minimizedAffinity',0):.3f}  "
          f"CNNaffinity={d.get('CNNaffinity',0):.3f}  "
          f"CNNscore={d.get('CNNscore',0):.3f}")

print("\n=== MM/GBSA (em, amber03/GAFF2/Gasteiger, 1 frame) ===")
terms = ["Van der Waals","Electrostatic","Polar Solvation","Non-Polar Solvation","Gas","TOTAL"]
for p, r in sorted(gbsa_results.items()):
    vals = "  ".join(f"{k[:4]}={r.get(k,0):.2f}" for k in terms)
    print(f"Pose {p}: {vals}")

print("\n=== H-BOND FREQUENCY (across 5 poses) ===")
for res, cnt in sorted(hbond_freq.items(), key=lambda x: -x[1]):
    print(f"  {res}: {cnt}/5")

print("\n=== HYDROPHOBIC CONTACT FREQUENCY (across 5 poses) ===")
for res, cnt in sorted(hphob_freq.items(), key=lambda x: -x[1]):
    print(f"  {res}: {cnt}/5")

print("\n=== BEST POSE ===")
best_gbsa = min(gbsa_results, key=lambda p: gbsa_results[p]["TOTAL"])
best_vina = min(range(1,6), key=lambda i: pose_data[i-1].get("minimizedAffinity", 0))
print(f"Best MM/GBSA: Pose {best_gbsa} ({gbsa_results[best_gbsa]['TOTAL']:.2f} kcal/mol)")
print(f"Best Vina: Pose {best_vina} ({pose_data[best_vina-1].get('minimizedAffinity',0):.3f} kcal/mol)")
print(f"Best CNNscore: Pose 1 ({pose_data[0].get('CNNscore',0):.3f})")
