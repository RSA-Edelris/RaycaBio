
import numpy as np
from scipy import stats
import json

# Known actives with (name, smiles, AS_ratio)
print("known_actives sample:", known_actives[:3])
print("docking_results known:", {k: docking_results[k] for k in [n for n,s,r in known_actives]})
