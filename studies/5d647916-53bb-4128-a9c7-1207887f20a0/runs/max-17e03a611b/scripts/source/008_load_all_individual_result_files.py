
import json

# Load all individual result files
files = {
    "MCUF651": "aizynthfinder-results.json",
    "A317":    "aizynthfinder-results-2.json",
    "8008":    "aizynthfinder-results-3.json",
    "7977":    "aizynthfinder-results-4.json",
    "7877":    "aizynthfinder-results-5.json",
}

def show_routes(name, data):
    out = data.get("output", {})
    print(f"\n{'='*70}")
    print(f"COMPOUND: {name}")
    print(f"  is_solved={out.get('is_solved')}  n_routes={out.get('n_routes')}  "
          f"n_solved={out.get('n_solved_routes')}  top_score={out.get('top_score','?'):.4f}")
    print(f"  Summary: {out.get('summary','')}")
    routes = out.get("routes", [])
    for i, route in enumerate(routes):
        print(f"\n  --- Route {i+1} (score={route.get('score','?'):.4f}, solved={route.get('is_solved','?')}) ---")
        # Print the reaction tree
        def print_tree(node, depth=0):
            indent = "  " * (depth + 2)
            if node.get("type") == "mol":
                smiles = node.get("smiles", "?")
                in_stock = node.get("in_stock", False)
                stock_info = " [IN STOCK]" if in_stock else ""
                print(f"{indent}MOL: {smiles}{stock_info}")
            elif node.get("type") == "reaction":
                rxn = node.get("smiles", node.get("reaction_smarts", "?"))
                metadata = node.get("metadata", {})
                print(f"{indent}RXN: {rxn}")
                if metadata:
                    print(f"{indent}     meta: {metadata}")
            children = node.get("children", [])
            for child in children:
                print_tree(child, depth + 1)
        
        tree = route.get("route_tree", route.get("tree", {}))
        if tree:
            print_tree(tree)
        else:
            print("  [no tree data]")
            # Try to print reactions list if available
            rxns = route.get("reactions", route.get("reaction_tree", []))
            if rxns:
                for r in rxns:
                    print(f"    {r}")

for name, fname in files.items():
    try:
        with open(fname) as f:
            data = json.load(f)
        show_routes(name, data)
    except Exception as e:
        print(f"{name}: ERROR loading {fname}: {e}")
