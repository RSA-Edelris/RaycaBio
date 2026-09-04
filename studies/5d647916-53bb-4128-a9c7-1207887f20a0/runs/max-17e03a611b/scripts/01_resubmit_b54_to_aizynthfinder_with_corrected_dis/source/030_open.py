
import json

with open("aizynthfinder-results-6.json") as f:
    b54_aiz = json.load(f)

def print_tree(node, depth=0):
    indent = "  " * depth
    ntype = node.get("type", "?")
    if ntype == "mol":
        stock = "✓" if node.get("in_stock") else "✗"
        children = node.get("children", [])
        print(f"{indent}[{stock}] {node['smiles']}")
        for ch in children:
            print_tree(ch, depth)
    elif ntype == "reaction":
        meta = node.get("metadata", {})
        cls = meta.get("classification", "?")
        prob = meta.get("policy_probability", 0)
        print(f"{indent}  → rxn: {cls} (p={prob:.3f})")
        for ch in node.get("children", []):
            print_tree(ch, depth + 1)

r1 = b54_aiz["routes"][0]
print("=== B54 Route 1 (solved, 5 steps, 5/5 in stock) ===")
print_tree(r1["reaction_tree"])
