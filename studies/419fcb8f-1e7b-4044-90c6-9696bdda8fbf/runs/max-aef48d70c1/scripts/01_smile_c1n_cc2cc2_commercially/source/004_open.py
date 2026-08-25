
with open("aizynthfinder-results.json") as f:
    azf = json.load(f)

# Print each route summary
for i, route in enumerate(azf["routes"]):
    print(f"\n=== ROUTE {i+1} | solved={route['is_solved']} | depth={route['depth']} | reactions={route['n_reactions']} | leaves={route['n_leaves']} in_stock={route['n_leaves_in_stock']} ===")
    
    def walk(node, indent=0):
        prefix = "  " * indent
        if node["type"] == "mol":
            stock = " [IN STOCK]" if node.get("in_stock") else ""
            print(f"{prefix}MOL: {node['smiles']}{stock}")
        elif node["type"] == "reaction":
            meta = node.get("metadata", {})
            print(f"{prefix}RXN: template={meta.get('template_code','?')} class={meta.get('classification','?')} prob={meta.get('policy_probability',0):.3f} occ={meta.get('library_occurence',0)}")
            print(f"{prefix}     {node['smiles'][:120]}")
        for child in node.get("children", []):
            walk(child, indent+1)
    
    walk(route["reaction_tree"])
