
import json

with open("aizynthfinder-results-6.json") as f:
    b54_aiz = json.load(f)

print(f"is_solved: {b54_aiz.get('is_solved')}")
print(f"n_routes: {b54_aiz.get('n_routes')}")
print(f"n_solved_routes: {b54_aiz.get('n_solved_routes')}")
print(f"top_score: {b54_aiz.get('top_score')}")

routes = b54_aiz.get("routes", [])
for r in routes:
    leaves = []
    def collect_leaves(node):
        if node.get("type") == "mol" and not node.get("children"):
            leaves.append((node["smiles"], node.get("in_stock", False)))
        for ch in node.get("children", []):
            collect_leaves(ch)
    collect_leaves(r.get("reaction_tree", {}))
    n_in_stock = sum(1 for _, s in leaves if s)
    print(f"\nRoute {r['rank']}: solved={r.get('is_solved')} depth={r.get('depth')} "
          f"n_reactions={r.get('n_reactions')} leaves={len(leaves)} in_stock={n_in_stock}")
    for smi, stock in leaves:
        print(f"  {'[✓]' if stock else '[✗]'} {smi}")
