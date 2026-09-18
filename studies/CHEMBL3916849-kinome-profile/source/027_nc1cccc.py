
import numpy as np
from rdkit import Chem
from rdkit.Chem import DataStructs, rdMolDescriptors

QUERY_SMILES = "O=C(Nc1cccc(Nc2ncc(Br)c(NCCc3cnc[nH]3)n2)c1)N1CCCC1"

# Compute Morgan FP for query
qmol = Chem.MolFromSmiles(QUERY_SMILES)
qfp  = rdMolDescriptors.GetMorganFingerprintAsBitVect(qmol, radius=2, nBits=2048)

# Compute Tanimoto similarity of query to all training SMILES
similarities = []
for smi in train_s:
    mol = Chem.MolFromSmiles(smi)
    if mol:
        fp = rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
        tc = DataStructs.TanimotoSimilarity(qfp, fp)
        similarities.append(tc)
    else:
        similarities.append(0.0)

sims = np.array(similarities)
print("=== CHEMICAL SPACE AD ===")
print(f"Max Tanimoto (query vs training): {sims.max():.3f}")
print(f"Mean Tanimoto: {sims.mean():.3f}")
print(f"Compounds with Tc >= 0.40: {(sims >= 0.40).sum()}")
print(f"Compounds with Tc >= 0.30: {(sims >= 0.30).sum()}")
print(f"Compounds with Tc >= 0.20: {(sims >= 0.20).sum()}")

# Sort top similar
top_idx = np.argsort(sims)[::-1][:5]
print("\nTop 5 nearest training compounds:")
for i in top_idx:
    print(f"  Tc={sims[i]:.3f}  pChEMBL={train_l[i]:.2f}  {train_s[i][:60]}")

# Protein space: check if any training sequences share identity with prediction targets
print("\n=== PROTEIN SPACE AD ===")
print(f"Unique training protein sequences: {len(set(train_sq))}")
print(f"Prediction kinases: {len(pred_sq)}")
# Check max shared kmer coverage as proxy for sequence identity
def kmer_overlap(s1, s2, k=5):
    k1 = set(s1[i:i+k] for i in range(len(s1)-k+1))
    k2 = set(s2[i:i+k] for i in range(len(s2)-k+1))
    return len(k1 & k2) / max(len(k1 | k2), 1)

train_seqs_uniq = list(set(train_sq))
max_overlaps = []
for ps in pred_sq:
    ovlps = [kmer_overlap(ps, ts) for ts in train_seqs_uniq]
    max_overlaps.append(max(ovlps))

print(f"Max k5-mer overlap (pred kinase → best training protein): {max(max_overlaps):.3f}")
print(f"Mean max overlap: {np.mean(max_overlaps):.3f}")
print(f"Pred kinases with max overlap >= 0.40: {sum(1 for v in max_overlaps if v >= 0.40)}")
print(f"Pred kinases with max overlap >= 0.20: {sum(1 for v in max_overlaps if v >= 0.20)}")
