
# Print complete mapped reaction trees for A317 and 7977 (the most data-rich)
import json

def print_tree_deep(node, depth=0):
    indent = "  " * depth
    t = node.get("type","")
    if t == "mol":
        stock = " [STOCK]" if node.get("in_stock") else ""
        print(f"{indent}MOL: {node['smiles']}{stock}")
    elif t == "reaction":
        meta = node.get("metadata", {})
        mapped = meta.get("mapped_reaction_smiles","")
        lib = meta.get("library_occurence", 0)
        prob = meta.get("policy_probability", 0)
        print(f"{indent}RXN: lib={lib} prob={prob:.3f}")
        if mapped:
            print(f"{indent}     mapped={mapped[:300]}")
    for c in node.get("children",[]):
        print_tree_deep(c, depth+1)

for fname, name in [
    ("aizynthfinder-results-2.json", "A317"),
    ("aizynthfinder-results-4.json", "7977"),
    ("aizynthfinder-results-3.json", "8008"),
]:
    with open(fname) as fh:
        raw = json.load(fh)
    print(f"\n{'#'*60}")
    print(f"# {name} - Route 1 (solved={raw['routes'][0]['is_solved']})")
    print(f"{'#'*60}")
    print_tree_deep(raw["routes"][0]["reaction_tree"])
