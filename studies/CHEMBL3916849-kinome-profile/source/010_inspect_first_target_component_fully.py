
# Inspect first target component fully
r_t = requests.get(f"{BASE}/target/CHEMBL4722.json", timeout=20)
t_data = r_t.json()
comp0 = t_data['target_components'][0]
print("Aurora A (CHEMBL4722) component fields:")
for k, v in comp0.items():
    print(f"  {k}: {str(v)[:120]}")
