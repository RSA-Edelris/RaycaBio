
import json

# Write the full inputs to a JSON file in the workspace
inputs = {
    "drug_smiles":      train_smiles,
    "target_sequences": train_seqs,
    "labels":           train_labels,
    "drug_encoding":    "CNN",
    "target_encoding":  "CNN",
    "train_epoch":      15,
    "LR":               0.001,
    "batch_size":       64,
    "frac":             [0.7, 0.1, 0.2],
    "random_seed":      42,
    "predict_smiles":   pred_smiles,
    "predict_targets":  pred_seqs
}

input_path = "/home/ubuntu/rayca-sessions/b96424ba-16ee-41cb-b71c-c27a58be87c0-8a50fbf21660/dp_inputs.json"
with open(input_path, 'w') as f:
    json.dump(inputs, f)

import os
size_kb = os.path.getsize(input_path) / 1024
print(f"Input file written: {input_path}")
print(f"Size: {size_kb:.1f} KB")

# Try dispatch with file reference
result = dispatch('deeppurpose', inputs, gpu=True, inputs_file=input_path)
print("Result:", result)
