
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.ML.Cluster import Butina
import numpy as np

# ---- Compute ECFP4 fingerprints ----
fps = []
for r in results:
    fp = AllChem.GetMorganFingerprintAsBitVect(r['mol'], radius=2, nBits=2048)
    fps.append(fp)

n = len(fps)

# ---- Pairwise Tanimoto similarity matrix ----
sim_matrix = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        sim_matrix[i, j] = DataStructs.TanimotoSimilarity(fps[i], fps[j])

print("Pairwise Tanimoto similarity (ECFP4, r=2, 2048 bits):")
ids = [r['EDS_Number'] for r in results]
header = "             " + "  ".join(f"{x[-5:]:>7}" for x in ids)
print(header)
for i, row in enumerate(sim_matrix):
    vals = "  ".join(f"{v:7.3f}" for v in row)
    print(f"{ids[i][-8:]:<13}  {vals}")
