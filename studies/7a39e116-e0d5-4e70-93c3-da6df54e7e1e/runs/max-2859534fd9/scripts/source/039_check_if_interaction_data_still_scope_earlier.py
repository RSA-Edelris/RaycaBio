
# Check if interaction data still in scope from earlier session
try:
    print("hbond_freq:", hbond_freq)
    print("hphob_freq:", hphob_freq)
    print("interaction_results available:", len(interaction_results))
except NameError as e:
    print("Not in scope:", e)
