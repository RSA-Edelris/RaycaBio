
# Manually verify sol_idx and base_idx for all 8 rows
SOLVENTS = ["Dioxane", "DMF"]
BASES    = ["K₃PO₄", "Cs₂CO₃", "DBU", "DIPEA"]
ROWS     = list("ABCDEFGH")

print("Row | ri | sol_idx | base_idx | Solvent  | Base")
print("----+----+---------+----------+----------+--------")
for ri in range(8):
    sol_idx  = ri // 4
    base_idx = ri  % 4
    row_letter = ROWS[ri]
    print(f"  {row_letter} | {ri}  |   {sol_idx}     |     {base_idx}    | {SOLVENTS[sol_idx]:<8} | {BASES[base_idx]}")

print()
print("Specific checks:")
print(f"ri=0: sol={0//4} ({SOLVENTS[0//4]}), base={0%4} ({BASES[0%4]})  => expected Dioxane, K₃PO₄")
print(f"ri=3: sol={3//4} ({SOLVENTS[3//4]}), base={3%4} ({BASES[3%4]})  => expected Dioxane, DIPEA")
print(f"ri=4: sol={4//4} ({SOLVENTS[4//4]}), base={4%4} ({BASES[4%4]})  => expected DMF, K₃PO₄")
print(f"ri=7: sol={7//4} ({SOLVENTS[7//4]}), base={7%4} ({BASES[7%4]})  => expected DMF, DIPEA")
