
# Load gnina scores from JSON
with open(f"{ART}/gnina_all6_result.json") as f:
    gnina_data = json.load(f)

print("Gnina JSON keys:", list(gnina_data.keys()))
print("poses:", gnina_data.get('poses', [])[:3] if gnina_data.get('poses') else "")
# Try to see structure
for k, v in list(gnina_data.items())[:8]:
    print(f"  {k}: {str(v)[:120]}")
