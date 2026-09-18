
import numpy as np

# Load predictions from the output file
logits = np.load('CNN_CNN_logits.npy')
print(f"Logits shape: {logits.shape}")
print(f"Logits: {logits}")

# Read test table
with open('test_markdowntable.txt') as f:
    print("\n=== TEST TABLE ===")
    print(f.read())

with open('valid_markdowntable.txt') as f:
    print("\n=== VALID TABLE ===")
    print(f.read())
