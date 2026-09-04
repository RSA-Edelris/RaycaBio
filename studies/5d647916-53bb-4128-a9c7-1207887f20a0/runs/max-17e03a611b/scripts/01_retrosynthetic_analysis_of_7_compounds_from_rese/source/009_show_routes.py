
import json

def show_routes(name, data):
    out = data.get("output", {})
    top = out.get('top_score', 'N/A')
    print(f"\n{'='*70}")
    print(f"COMPOUND: {name}")
    print(f"  is_solved={out.get('is_solved')}  n_routes={out.get('n_routes')}  top_score={top}")

    def print_tree(node, depth=0):
        indent = "  " * (depth + 2)
        ntype = node.get("type", "")
        if ntype == "mol":
            smiles = node.get("smiles", "?")
            in_stock = node.get("in_stock", False)
            stock_info = " [STOCK]" if in_stock else ""
            print(f"{indent}MOL: {smiles}{stock_info}")
        elif ntype == "reaction":
            meta = node.get("metadata", {})
            rxn_class = meta.get("classification", meta.get("name", "?"))
            print(f"{indent}RXN [{rxn_class}]")
        for child in node.get("children", []):
            print_tree(child, depth + 1)

    for i, route in enumerate(out.get("routes", [])):
        score = route.get('score', 'N/A')
        solved = route.get('is_solved', '?')
        print(f"\n  --- Route {i+1}  score={score}  solved={solved} ---")
        tree = route.get("route_tree", {})
        if tree:
            print_tree(tree)
        else:
            print("    [no tree]")

# Use the all_results dict already in memory
names_order = ["MCUF651", "A317", "8008", "7977", "7877"]
for name in names_order:
    if name in all_results and all_results[name].get("rc") == 0:
        show_routes(name, all_results[name])
    else:
        print(f"\n{name}: not available in all_results")
